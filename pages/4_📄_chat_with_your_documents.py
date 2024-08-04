import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

import utils
import streamlit as st
from streaming import StreamHandler

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import DocArrayInMemorySearch
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

from langchain_openai import OpenAIEmbeddings
#from langchain_chroma import Chroma
from langchain.vectorstores import Chroma
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.query_constructor.base import AttributeInfo

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


st.set_page_config(page_title="Book recommendation", page_icon="📄")
st.header('Chat to get a book recommendation (Basic RAG)')
st.write('Has access to custom library about 6500 books and can respond to user queries by referring to its contents')
st.write('[![view source code ](https://img.shields.io/badge/view_source_code-gray?logo=github)](https://github.com/salimdallal/MSBA316-Project-langchain-chatbot/blob/master/pages/4_%F0%9F%93%84_chat_with_your_documents.py)')


persist_directory = './chroma_persist'

class CustomDataChatbot:

    def __init__(self):
        utils.sync_st_session()
        self.llm = utils.configure_llm()

    def save_file(self, file):
        folder = 'tmp'
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        file_path = f'./{folder}/{file.name}'
        with open(file_path, 'wb') as f:
            f.write(file.getvalue())
        return file_path

    @st.spinner('Analyzing documents..')
    def setup_qa_chain(self):   #, uploaded_files):
        # Load documents
        # # # docs = []
        # # # for file in uploaded_files:
        # # #     file_path = self.save_file(file)
        # # #     loader = PyPDFLoader(file_path)
        # # #     docs.extend(loader.load())
        
        # # # # Split documents
        # # # text_splitter = RecursiveCharacterTextSplitter(
        # # #     chunk_size=1000,
        # # #     chunk_overlap=200
        # # # )
        # # # splits = text_splitter.split_documents(docs)

        # Create embeddings and store in vectordb
        #embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        #vectordb = DocArrayInMemorySearch.from_documents(splits, embeddings)
        openai_api_key=os.environ.get("OPENAI_API_KEY")
        if not openai_api_key:
            openai_api_key=st.secrets("OPENAI_API_KEY")
        embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)




        metadata_field_info = [
            AttributeInfo(
                name="title",
                description="The title of the novel from the title metadata",
                type="string",
            ),
                AttributeInfo(
                name="category",
                description="The category or subject the novel belongs to",
                type="string",
            ),
                AttributeInfo(
                name="author",
                description="The author of the novel",
                type="string",
            ),
                AttributeInfo(
                name="published_year",
                description="The year the novel was published",
                type="integer",
            ),
                AttributeInfo(
                name="average_rating",
                description="The average rating of the novel by the readers",
                type="decimal",
            ),
                AttributeInfo(
                name="num_pages",
                description="The number of pages the novel has",
                type="integer",
            ),
                AttributeInfo(
                name="ratings_count",
                description="The number of ratings given by readers for this novel",
                type="integer",
            )
        ]


        document_content_description = "Novel in a library"

        # Setup memory for contextual conversation        
        memory = ConversationBufferMemory(
            memory_key='chat_history',
            output_key='answer',
            return_messages=True
        )



        #Define retriever
        # retriever = vectordb.as_retriever(
        #     search_type='mmr',
        #     search_kwargs={'k':2, 'fetch_k':4}
        # )
        
        retriever = SelfQueryRetriever.from_llm(
            llm=self.llm,
            vectorstore=vectordb,
            document_contents=document_content_description,
            metadata_field_info=metadata_field_info,
            verbose=True,
            #search_kwargs={'k':2, 'fetch_k':4}
           
        )



        # Setup LLM and QA chain
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=memory,
            return_source_documents=True,
            verbose=True
        )
        return qa_chain

    @utils.enable_chat_history
    def main(self):

        # User Inputs
        # uploaded_files = st.sidebar.file_uploader(label='Upload PDF files', type=['pdf'], accept_multiple_files=True)
        # if not uploaded_files:
        #     st.error("Please upload PDF documents to continue!")
        #     st.stop()

        user_query = st.chat_input(placeholder="Ask me anything!")

        # # # if uploaded_files and user_query:
        # # #     qa_chain = self.setup_qa_chain(uploaded_files)
        if user_query:
            qa_chain = self.setup_qa_chain()
            utils.display_msg(user_query, 'user')

            with st.chat_message("assistant"):
                st_cb = StreamHandler(st.empty())
                result = qa_chain.invoke(
                    {"question":user_query},
                    {"callbacks": [st_cb]}
                )
                print(result)
                response = result["answer"]
                #response = result[0]
                st.session_state.messages.append({"role": "assistant", "content": response})

                # to show references
                for idx, doc in enumerate(result['source_documents'],1):
                    title = os.path.basename(doc.metadata['title'])
                    page_num = doc.metadata['num_pages']
                    author = doc.metadata['author']
                    rating = doc.metadata['average_rating']
                    ref_title = f":blue[Book Title {idx}: *{title} - number of pages:{page_num}*]"
                    with st.popover(ref_title):
                        st.caption(doc.page_content)
                        st.caption(f"Auther: {author}")
                        st.caption(f"Average rating: {rating}")

if __name__ == "__main__":
    obj = CustomDataChatbot()
    obj.main()
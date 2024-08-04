import streamlit as st

import os
#os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"


st.set_page_config(
    page_title="Langchain Chatbot",
    page_icon='💬',
    layout='wide'
)

st.header("Chatbot Implementations with Langchain")
st.write("""
[![view source code ](https://img.shields.io/badge/GitHub%20Repository-gray?logo=github)](https://github.com/salimdallal/MSBA316-Project-langchain-chatbot)
![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fmsba316-project-langchain-chatbot.streamlit.app/&label=Visitors&labelColor=%235d5d5d&countColor=%231e7ebf&style=flat)
""")
st.write("""
Langchain is a powerful framework designed to streamline the development of applications using Language Models (LLMs). It provides a comprehensive integration of various components, simplifying the process of assembling them to create robust applications.

Leveraging the power of Langchain, the creation of chatbots becomes effortless. Here we test the chatbot in a book recommendation scenario:

- **Chat for a book recommendation**: Empower the chatbot with the ability to access custom documents, enabling it to provide answers to user queries based on the referenced information.
""")


#[![linkedin ](https://img.shields.io/badge/Salim%20Dallal-blue?logo=linkedin&color=gray)](https://www.linkedin.com/in/salimdallal/)

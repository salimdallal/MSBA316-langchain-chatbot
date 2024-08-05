# Chatbot Implementations with Langchain + Streamlit

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/salimdallal/MSBA316-langchain-chatbot?quickstart=1)


Langchain is a powerful framework designed to streamline the development of applications using Language Models (LLMs). \
It provides a comprehensive integration of various components, simplifying the process of assembling them to create robust applications.

## 💬 Sample chatbot use cases
Here are a few examples of chatbot implementations using Langchain and Streamlit:

-  **Chat with your documents** \
  Empower the chatbot with the ability to access custom documents, enabling it to provide answers to user queries based on the referenced information.


## <img src="https://streamlit.io/images/brand/streamlit-mark-color.png" width="40" height="22"> Streamlit App
Created a multi-page streamlit app containing all sample chatbot use cases. Streamlit cloud does not work well with Chroma. As such the app is not functional and only codespace works. 

## 🖥️ Running locally
```shell
# Run main streamlit app
$ streamlit run Home.py
```

## 📦 Running with Docker
```shell
# To generate image
$ docker build -t langchain-chatbot .

# To run the docker container
$ docker run -p 8501:8501 langchain-chatbot
```

## 💁 Contributing
Planning to add more chatbot examples over time. PRs are welcome.

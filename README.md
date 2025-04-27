# YouTube Video Chat Assistant

## Overview

An AI-powered assistant that allows users to ask questions and Chat about YouTube videos by asking questions and receiving detailed answers based on the video transcript. Built using **LangChain**, **FAISS**, and **OpenAI GPT-4**, this AI system Has A well Structured Document Pipeline.I have Used Streamlit for making an Interactive UI.
Currently, this project is running locally, and I have not yet published it to the cloud. Since different cloud platforms offer various deployment methods, I am actively exploring the best options to host the application. 

## Main Process 
1. Takes in a Youtube URL 
2. Converts into a Full Youtube Transcript
3. Convert The Document Into Vector Embeddings and Do a Similary search to Return 4 indivuidal Chunks And Generate a Natural Response (Entire Document Pipeline)
4. Generate a Response with memory also

## Installation 
1. Clone the repository: git clone https://github.com/your-username/youtube-chat-assistant.git
2. Install All the dependencies: pip install -r requirements.txt
3. Set Your .env File with the OpenAI Key: OPENAI_API_KEY="your_api_key"
4. Save all files and Run main.py: python -m streamlit run main.py

Thank You,
Happy coding 


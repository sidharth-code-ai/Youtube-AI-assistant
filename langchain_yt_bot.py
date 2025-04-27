from langchain.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.vectorstores import FAISS
from langchain.tools import tool
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
import os 

load_dotenv()

openai_api_key = os.getenv("OPEN_AI_API_KEY")

embeddings = OpenAIEmbeddings(api_key=openai_api_key)

memory = ConversationBufferMemory(input_key="question",return_messages=True)


def create_vector_db_from_youtube_url(video_url):
    loader = YoutubeLoader.from_youtube_url(video_url)
    transcript = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    docs = text_splitter.split_documents(transcript)

    db = FAISS.from_documents(docs,embeddings)
    return db 

## Query Answer Tool

def generate_answer_from_query(query: str, youtube_url: str,k: int=4):
    """\Generates a detailed answer to a user's query based on the content of a YouTube video transcript.

    This tool takes a natural language query and a YouTube video URL as input.
    It retrieves relevant information from the video transcript using semantic search
    and then uses a large language model to generate a comprehensive answer.

    Args:
        query (str): The question or topic the user wants to know about.
                     Example queries: "What did they talk about cryptocurrency?",
                                      "What did the speaker say about AI?",
                                      "Give me an overall summary of the video."
        youtube_url (str): The URL of the YouTube video to extract information from.
        k (int, optional and not required ): The number of relevant document chunks to retrieve
                           from the vector database. Defaults to 4.

    Returns:
        str: A detailed answer to the query, generated based on the information
             found in the YouTube video transcript. If insufficient information
             is available in the transcript to answer the question, it returns
             "I don't know".
    """
    database = create_vector_db_from_youtube_url(youtube_url)

    # Search The Doc Based On The Top K to Get Similar Chunks 
    docs = database.similarity_search(query=query,k=k)
    docs_page = "".join([d.page_content for d in docs ])



    # Steup the LLM 

    llm = ChatOpenAI(
        model="gpt-4",
        api_key=openai_api_key,
        temperature=0.4,

    )
    # Setup the prompt 
    prompt_template = PromptTemplate(
        input_variables=  ["question","docs"],
        template= """
        You are a helpful assistant that that can answer questions about youtube videos 
        based on the video's transcript.
        
        Answer the following question: {question}
        By searching the following video transcript: {docs}
        
        Only use the factual information from the transcript to answer the question.
        
        If you feel like you don't have enough information to answer the question, say "I don't know".
        
        Your answers should be verbose and detailed.
"""
    )


    # Steup the memory 
    # Setup the Chain 
    chain = LLMChain(
        llm=llm,
        prompt=prompt_template,
        verbose=True,
        memory=memory,
        output_key="answer"
    )

    # Run the Agent and Get repsonse and Return it 
    response = chain.run(question=query, docs=docs_page)
    response = response.replace("\n","")
    return response





    



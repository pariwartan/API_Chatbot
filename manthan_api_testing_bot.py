import streamlit as st
import openai as openai
import os
from langchain.chains import RetrievalQA 
import langchain
from langchain.chains import LLMChain, APIChain
from dotenv import load_dotenv, find_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from langchain.chains import ConversationalRetrievalChain
from streamlit_chat import message
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from pydantic import ( BaseModel, Field )
from langchain.tools import BaseTool
from typing import Type
from langchain.agents import create_sql_agent, AgentType
from langchain.agents import initialize_agent
from langchain.chains.openai_functions.openapi import get_openapi_chain
import json
from langchain.prompts import PromptTemplate
from constants import openai_key
from langchain_openai import OpenAI
#Local Stuffs
from manthan_prompts import manthan_assistant_bot_template, manthan_api_assistant_prompt, api_response_prompt, api_url_prompt
from langchain.memory.buffer import ConversationBufferMemory
from manthan_api_docs import project_manthan_api_docs

_ = load_dotenv(find_dotenv())

os.environ["OPENAI_API_KEY"]=openai_key

llm = ChatOpenAI(temperature=0)
#llm = OpenAI(model='gpt-3.5-turbo-instruct',temperature=0)

# DB Connection

def getDB():
    db_user = "root"
    db_password = "Admin"
    db_host = "localhost"
    db_name = "manthan"
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
    return db

def callManthanAPI(user_question):
        api_chain = APIChain.from_llm_and_api_docs(
            llm=llm,
            api_docs=project_manthan_api_docs,
            api_url_prompt=api_url_prompt,
            api_response_prompt=api_response_prompt,
            verbose=False,
            limit_to_domains=["http://127.0.0.1:5000/"]
        )
        response = api_chain.run(user_question)   
        return response

class callManthanAPIInfo(BaseModel):
            user_question: str = Field(description="user_question")
class callManthanAPIs(BaseTool):
            name = "call_Manthan_API"
            description = """"
            Useful for project Manthan APIs testing. It will be used to consume Manthan APIs.
            """
            args_schema: Type[BaseModel] = callManthanAPIInfo
            def _run(self, user_question:str):
                response = callManthanAPI(user_question)
                return response
            def _arun(self, user_question:str):
                raise NotImplementedError("error")

def getManthanAPI(user_question): 
        API_info_prompt=PromptTemplate(
        input_variables=['project_manthan_api_docs'],
        template=""""Use this API DOC: {project_manthan_api_docs} to get all availble or listed APIs or endpoints.
        list all API payload details like URI, method, header, request , response etc"""
        )
        chain=LLMChain(llm=llm,prompt=API_info_prompt,verbose=True)
        response = chain.run(project_manthan_api_docs)
        return response

class getManthanAPIInfo(BaseModel):
            user_question: str = Field(description="user_question")
class getManthanAPIs(BaseTool):
            name = "get_Manthan_API"
            description = """"
            Useful for getting all available or listed APIs or endpoints in Manthan Project.
            """
            args_schema: Type[BaseModel] = getManthanAPIInfo
            def _run(self, user_question:str):
                response = getManthanAPI(user_question)
                return response
            def _arun(self, user_question:str):
                raise NotImplementedError("error")                


def set_png_as_page_bg():
    page_bg_img = '''
    <style>
    .stApp{
    background-image: url("https://adpselect.com/login/images/backgrounds/adpSelect.png");
    background-size: 50%;
    width:100%;
    background-repeat: no-repeat;
    }
    </style>
    ''' 
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

if 'responses' not in st.session_state:
        st.session_state['responses'] = ["Hi! I am Project Manthan Testing Bot, How may i assist you?"]

if 'requests' not in st.session_state:
        st.session_state['requests'] = []

def main():
    langchain.debug = True
    load_dotenv()
    logo = 'https://images.sftcdn.net/images/t_app-icon-m/p/69c53218-c7a9-11e6-8ce5-5a990553aaad/3424445367/adp-mobile-solutions-logo'
    logo2 ='https://i.pinimg.com/736x/8b/16/7a/8b167af653c2399dd93b952a48740620.jpg'
    st.set_page_config(page_title="Ops Care",page_icon=logo) 
    set_png_as_page_bg()
    st.header("Manthan API Testing")
    if 'area_key' not in st.session_state:
     st.session_state.area_key = 1
  
    #system_message = SystemMessagePromptTemplate.from_template(template=manthan_assistant_bot_template)
    system_message = SystemMessagePromptTemplate.from_template(template="""Simply return the response as it is , do not change anything""")
    response_container = st.container()
    # container for text box
    textcontainer = st.container()
    with textcontainer:
        user_question = st.empty()
        user_question = st.chat_input("I am here to help you!", key="input")
        if user_question:
            with st.spinner("Processing"):
                tools = [ getManthanAPIs(), callManthanAPIs() ]
                agent_kwargs = {
                 #"extra_prompt_messages": [MessagesPlaceholder(variable_name="memory")],
                 "system_message": system_message
                                }
                if "memory" not in st.session_state:
                 st.session_state.memory = ConversationBufferMemory(memory_key="memory", return_messages=True)     
                agent = initialize_agent(tools , llm=llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True,
                                          agent_kwargs=agent_kwargs )

                response = agent.run(user_question)
                st.session_state.requests.append(user_question)
                st.session_state.responses.append(response) 
    with response_container:
        if st.session_state['responses']:
            for i in range(len(st.session_state['responses'])):
                message(st.session_state['responses'][i],key=str(i),logo=logo)
                if i < len(st.session_state['requests']):
                    message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user', logo=logo2 )

    
if __name__ == '__main__':
    main()        
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from app.api.logger import setup_logger

import os

from dotenv import load_dotenv, find_dotenv
from app.api.schemas.security_plan_schemas import SecurityPlan

load_dotenv(find_dotenv())

logger = setup_logger(__name__)

parser = JsonOutputParser(pydantic_object=SecurityPlan)

model = GoogleGenerativeAI(model="gemini-1.5-pro")

def read_text_file(file_path):
    # Get the directory containing the script file
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Combine the script directory with the relative file path
    absolute_file_path = os.path.join(script_dir, file_path)
    
    with open(absolute_file_path, 'r') as file:
        return file.read()

prompt = PromptTemplate(
  template=read_text_file('prompt/generate-security-plan-prompt.txt'),
  input_variables=[
    "department",
    "province",
    "district",
    "mainTopic",
    "additionalDescription"
  ],
  partial_variables={"format_instructions": parser.get_format_instructions()}
)

def compile_security_plan_chain():
    logger.info("Compilando cadena...")
    chain = prompt | model | parser
    logger.info("La cadena se ha compilado satisfactoriamente")
    return chain
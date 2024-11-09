from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_openai import ChatOpenAI
from app.api.logger import setup_logger
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
import os
from langchain.schema import (
       AIMessage,
       HumanMessage,
       SystemMessage
)
from dotenv import load_dotenv, find_dotenv

from app.api.schemas.info_agent_schemas import InfoAgentArgs, SecurityPlanDataCollection

load_dotenv(find_dotenv())

logger = setup_logger(__name__)

parser = JsonOutputParser(pydantic_object=SecurityPlanDataCollection)

model = GoogleGenerativeAI(model="gemini-1.5-pro")

def read_text_file(file_path):
    # Get the directory containing the script file
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Combine the script directory with the relative file path
    absolute_file_path = os.path.join(script_dir, file_path)
    
    with open(absolute_file_path, 'r') as file:
        return file.read()
    
chat_openai_llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)

def generate_info_agent_results(data: InfoAgentArgs):
    logger.info("Buscando información")
    search = TavilySearchResults(max_results=2)
    tools = [search]
    agent_executor = create_react_agent(chat_openai_llm, tools)
    ai_related_message = f"""
    Realiza una búsqueda exhaustiva y precisa en Tavily sobre información de seguridad real y verificada para la siguiente ubicación:

    - **Departamento**: {data.department}
    - **Provincia**: {data.province}
    - **Distrito**: {data.district}

    **Descripción adicional de la búsqueda**:
    {data.description}

    Utiliza Tavily exclusivamente para brindar información actual, relevante y basada en datos reales de seguridad para esta ubicación específica. Asegúrate de no inventar información y de basarte únicamente en datos confirmados. No proporciones contenido especulativo ni sin verificación.

    La respuesta debe seguir estrictamente el formato y los requisitos especificados en {parser.get_format_instructions()}.
    """

    messages = [
        SystemMessage(content="Eres un experto en búsqueda de información de seguridad y estrategias de diseño a través de Tavily."),
        HumanMessage(content=ai_related_message)
    ]

    result = agent_executor.invoke({'messages': messages})

    logger.info(result)

    parsed_result = parser.parse(result["messages"][-1].content)

    logger.info(f"Resultados de la Búsqueda de Información de Seguridad: {parsed_result}")

    return parsed_result
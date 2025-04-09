"""
AUTO-CONFIG PIPELINE MAIN FILE

 - called as a module in Chain.inference_endpoint.py
 - uses ollama_config.py, vector_database_configs
__________________________________________________________________

Runs and orchestrate app's auto-config operations as follows:

1 - parse_config_params():
to be implemented

1 - run_config():
calls:
    1 - config_ollama_requirements from ollama_config.py
    2 - create_chroma_vector_store_from_pdf_data from vector_database_config.py
    3 - ChatOllama constructor to create an instance with selected chat_model
"""

import langchain_chroma
from Config.ollama_config import config_ollama_requirements
from Config.vector_database_config import create_chroma_vector_store_from_pdf_data
from langchain_ollama import ChatOllama
from Config.colors import ColorText
import os

__BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
__OPS_SUCCESS_PREFIX = "[SUCCESS]"
__OPS_FAILURE_PREFIX = "[FAILURE]"
__CONFIG_PARAMS = {
    "embedding_model": "nomic-embed-text:latest",
    "chat_model": "mistral:latest",
    "data_source_path": os.path.join(__BASE_DIR, "Data"),
    "data_files_extension": "txt",
    "text_chunk_size": 1000,
    "text_chunks_overlap": 0,
    "vector_store_dir": "chatbot_vector_storage"
}


def run_config() -> (langchain_chroma.Chroma, ChatOllama):
    """
    Runs the entire auto-config pipeline by:
    1 - Checking if OLLAMA is detected in the environment (Make sure to have OLLAMA installed and added to the PATH)
    2 - Check for both embedding and chat models, if they exist in OLLAMA and installs them if not found
    3 - Create and persist a ChromaDB vector store in the chatbot_vector_storage directory (if not found, it is created)
    4 - Creates an instance of ChatOllama using the selected LLM as the APP Ai to perform Q&A tasks
    :return: vectorstore (instance of ChromaBD), model (instance of ChatOllama)
    """
    ops_prefix = f"[CONFIG][CHATBOT]"
    print(ColorText.colorize(f"{ops_prefix} Starting Chatbot Architecture configuration", ColorText.CYAN))

    config_ollama_requirements(
        embedding_model=__CONFIG_PARAMS["embedding_model"],
        chat_model=__CONFIG_PARAMS["chat_model"]
    )

    vectorstore = create_chroma_vector_store_from_pdf_data(
        data_dir_path=__CONFIG_PARAMS["data_source_path"],
        file_ext=__CONFIG_PARAMS["data_files_extension"],
        persist_directory=__CONFIG_PARAMS["vector_store_dir"],
        chunk_size=__CONFIG_PARAMS["text_chunk_size"],
        chunk_overlap=__CONFIG_PARAMS["text_chunks_overlap"],
        embedding_model=__CONFIG_PARAMS["embedding_model"],
    )

    print(ColorText.colorize(f"{ops_prefix} Attempting to instantiate ChatBot's LLM", ColorText.CYAN))
    model = ChatOllama(model=__CONFIG_PARAMS["chat_model"])

    if model:
        print(
            ColorText.colorize(
                f"{ops_prefix}{__OPS_SUCCESS_PREFIX} {model} correctly instantiated and ready to use for inference.",
                ColorText.GREEN
            )
        )
    else:
        print(
            ColorText.colorize(
                f"{ops_prefix}{__OPS_FAILURE_PREFIX} failed to instantiate {model}.",
                ColorText.RED
            )
        )

    return vectorstore, model


if __name__ == '__main__':
    run_config()

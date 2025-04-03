from Config.ollama_config import config_ollama_requirements
from Config.vector_database_config import create_chroma_vector_store_from_pdf_data
from langchain_ollama import ChatOllama
from Config.colors import ColorText
import os

__BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
__DATA_FILE_PATH = os.path.join(__BASE_DIR, "Data", "WebinarBOTData.pdf")

__OPS_SUCCESS_PREFIX = "[SUCCESS]"
__OPS_FAILURE_PREFIX = "[FAILURE]"
__CONFIG_PARAMS = {
    "embedding_model": "nomic-embed-text:latest",
    "chat_model": "mistral:latest",
    "data_source_path": __DATA_FILE_PATH,
    "text_chunk_size": 1000,
    "text_chunks_overlap": 0
}


def run_config():
    ops_prefix = f"[CONFIG][CHATBOT]"
    print(ColorText.colorize(f"{ops_prefix} Starting Chatbot Architecture configuration", ColorText.CYAN))
    config_ollama_requirements(
        embedding_model=__CONFIG_PARAMS["embedding_model"],
        chat_model=__CONFIG_PARAMS["chat_model"]
    )

    vectorstore = create_chroma_vector_store_from_pdf_data(
        pdf_file_path=__CONFIG_PARAMS["data_source_path"],
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

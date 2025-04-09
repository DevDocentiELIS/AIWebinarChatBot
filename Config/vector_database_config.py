"""
VECTOR DATABASE CONFIG OPERATIONS HANDLER
 - called as a module in config_chatbot.py
 - uses colors.py internal module to enhance log prints
__________________________________________________________________
creates a new instance of the vector storage and persists it in chatbot_vector_storage directory for future usages

Handles ChromaDB vector database configuration as follows:

1 - create_chroma_vector_store_from_pdf_data(data_dir_path: str, file_ext: str, chunk_size: int, chunk_overlap: int,
    embedding_model: str):

    creates and return a ChromaDb vector storage instance reading all files
    from a data directory with a specific extension
  - calls:
    - 1 __load_from_directory(data_dir_path: str, file_ext: str, with_example=False):
        loads all files from a data directory with a specific extension
        :return list[Document] or None
    - 2 __embed_data(text_data: str, chunk_size: int, chunk_overlap: int, embedding_model: str):
        returns a list of embeddings created using the embedding_model
        :return text chunks and embeddings
    - 3 Chroma.from_documents(documents: list[Document], embedding: Embeddings | None = None)
        creates a ChromaDb vector storage parsing documents chunks and embeddings
        :return vector store instance
"""

import langchain_chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from Config.colors import ColorText
import os

__BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
__OPS_SUCCESS_PREFIX = "[SUCCESS]"
__OPS_FAILURE_PREFIX = "[FAILURE]"


def __load_from_directory(data_dir_path: str, file_ext: str, with_example: bool = False) -> list | None:
    """
    Loads all files from a data directory with a specific extension
    :param data_dir_path: path to directory containing all files to load
    :param file_ext: extension of files to load
    :param with_example: if true, prints a small example text from loaded documents
    :return: list[Documents] or None
    """
    ops_prefix = f"[CONFIG][VECTOR_DATABASE][DATA_SOURCE]"
    print(ColorText.colorize(f"{ops_prefix} Attempting to load {file_ext} data from source: {data_dir_path}.", ColorText.CYAN))
    try:
        loader = DirectoryLoader(data_dir_path, glob=f"**/*.{file_ext}", show_progress=True, use_multithreading=True)
        data = loader.load()
        print(
            ColorText.colorize(
                f"{ops_prefix}{__OPS_SUCCESS_PREFIX} Correctly loaded n: {len(data)} - {file_ext} data from source: "
                f"{data_dir_path}.",
                ColorText.GREEN
            )
        )
        if with_example:
            print("sample data from first doc")
            print(data[0].page_content[:100])
        return data
    except FileNotFoundError:
        print(
            ColorText.colorize(
                f"{ops_prefix}{__OPS_FAILURE_PREFIX} Failed loading data from source {data_dir_path}. File not Found",
                ColorText.RED)
        )
        return None


def __embed_data(text_data: list, chunk_size: int, chunk_overlap: int,
                 embedding_model: str) -> (list, OllamaEmbeddings):
    """
    Creates and returns a list of documents chunks and embeddings created using the embedding_model
    :param text_data: documents to be split into chunks and embeddings
    :param chunk_size: dimensions in character for every chunk
    :param chunk_overlap: overlapping characters between chunks
    :param embedding_model: embedding model from OLLAMA to be used in the embeddings operations
    :return: list of documents chunks and embeddings
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_splits = text_splitter.split_documents(text_data)
    embeddings = OllamaEmbeddings(model=embedding_model)

    return all_splits, embeddings


def create_chroma_vector_store_from_pdf_data(data_dir_path: str, file_ext: str, persist_directory: str,
                                             chunk_size: int, chunk_overlap: int,
                                             embedding_model: str) -> langchain_chroma.Chroma:
    """
    Creates and returns a ChromaDb vector storage instance from selected data files
    CALLS:
    1 - __load_from_directory to load all files from a data directory with a specific extension
    2 - __embed_data to produce chunks and embeddings
    3 - Chroma.from_documents to create and persist the vector storage instance containing Chatbot additional context
    :param data_dir_path: path to directory containing all files to load
    :param file_ext: extension of files to load
    :param persist_directory: chroma db vector storage directory to persist the created db or load it
    :param chunk_size: dimensions in character for every chunk
    :param chunk_overlap: overlapping characters between chunks
    :param embedding_model: embedding model from OLLAMA to be used in the embeddings operations
    :return:
    """
    ops_prefix = f"[CONFIG][VECTOR_DATABASE][CREATING_CHROMA_VECTOR_STORAGE]"
    source_data = __load_from_directory(data_dir_path, file_ext)

    if source_data:
        print(ColorText.colorize(f"{ops_prefix} Attempting to create Chroma Vector DB", ColorText.CYAN))
        text_chunks, embeddings = __embed_data(source_data, chunk_size, chunk_overlap, embedding_model)
        print(
            ColorText.colorize(
                f"{ops_prefix}{__OPS_SUCCESS_PREFIX} Correctly created embeddings using {embedding_model}.",
                ColorText.GREEN
            )
        )
        print(ColorText.colorize(f"{ops_prefix} Creating vector storage", ColorText.CYAN))
        vectorstore = Chroma.from_documents(documents=text_chunks, embedding=embeddings,
                                            persist_directory=os.path.join(__BASE_DIR, persist_directory))
        print(
            ColorText.colorize(
                f"{ops_prefix}{__OPS_SUCCESS_PREFIX} Correctly created Chroma vector storage.",
                ColorText.GREEN
            )
        )
        return vectorstore


if __name__ == "__main__":
    pdf_path = "../Data"
    vector_store = create_chroma_vector_store_from_pdf_data(
        pdf_path,
        'txt',
        "chatbot_vector_storage",
        1000,
        0,
        "nomic-embed-text")

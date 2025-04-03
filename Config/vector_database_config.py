from langchain_community.document_loaders import PyPDFLoader  # or use PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from Config.colors import ColorText

__OPS_SUCCESS_PREFIX = "[SUCCESS]"
__OPS_FAILURE_PREFIX = "[FAILURE]"


def __load_pdf_data(file_path):
    ops_prefix = f"[CONFIG][VECTOR_DATABASE][DATA_SOURCE]"
    print(ColorText.colorize(f"{ops_prefix} Attempting to load PDF data from source: {file_path}.", ColorText.CYAN))
    try:
        loader = PyPDFLoader(file_path)
        data = loader.load()
        print(
            ColorText.colorize(
                f"{ops_prefix}{__OPS_SUCCESS_PREFIX} Correctly loaded PDF data from source: {file_path}.",
                ColorText.GREEN
                )
            )
        return data
    except FileNotFoundError:
        print(
            ColorText.colorize(
                f"{ops_prefix}{__OPS_FAILURE_PREFIX} Failed loading data from source {file_path}. File not Found",
                ColorText.RED)
        )
        return None


def __embed_data(text_data, chunk_size, chunk_overlap, embedding_model):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    all_splits = text_splitter.split_documents(text_data)
    embeddings = OllamaEmbeddings(model=embedding_model)

    return all_splits, embeddings


def create_chroma_vector_store_from_pdf_data(pdf_file_path, chunk_size, chunk_overlap, embedding_model):
    ops_prefix = f"[CONFIG][VECTOR_DATABASE][CREATING_CHROMA_VECTOR_STORAGE]"
    source_data = __load_pdf_data(pdf_file_path)

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
        vectorstore = Chroma.from_documents(documents=text_chunks, embedding=embeddings)
        print(
            ColorText.colorize(
                f"{ops_prefix}{__OPS_SUCCESS_PREFIX} Correctly created Chroma vector storage.",
                ColorText.GREEN
            )
        )
        return vectorstore


if __name__ == "__main__":
    pdf_path = "../Data/ELIS_Report-Sociale-2024.pdf"
    vector_store = create_chroma_vector_store_from_pdf_data(
        pdf_path,
        1000,
        0,
        "nomic-embed-text")

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from Config.colors import ColorText

__OPS_SUCCESS_PREFIX = "[SUCCESS]"
__OPS_FAILURE_PREFIX = "[FAILURE]"


def __load_from_directory(data_dir_path, file_ext, with_example=False):
    ops_prefix = f"[CONFIG][VECTOR_DATABASE][DATA_SOURCE]"
    print(ColorText.colorize(f"{ops_prefix} Attempting to load {file_ext} data from source: {data_dir_path}.", ColorText.CYAN))
    try:
        loader = DirectoryLoader(data_dir_path, glob=f"**/*.{file_ext}", show_progress=True, use_multithreading=True)
        data = loader.load()
        print(
            ColorText.colorize(
                f"{ops_prefix}{__OPS_SUCCESS_PREFIX} Correctly loaded n: {len(data)} - {file_ext} data from source: {data_dir_path}.",
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


def create_chroma_vector_store_from_pdf_data(data_dir_path, file_ext, chunk_size, chunk_overlap, embedding_model):
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
        vectorstore = Chroma.from_documents(documents=text_chunks, embedding=embeddings)
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
        1000,
        0,
        "nomic-embed-text")

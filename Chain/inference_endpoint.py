"""

"""

from Config.config_chatbot import run_config
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough


__prompt_template = """
Your are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, just say that you don't know.

<context>
{context}
</context>

Answer the following question in Italian:

{question}"""

__rag_prompt = ChatPromptTemplate.from_template(__prompt_template)
__vector_storage, __model = run_config()


def __format_docs(docs):
    return "\n".join(doc.page_content for doc in docs)


__retriever = __vector_storage.as_retriever(k=5)

__qa_chain = None


def llm_inference_endpoint():
    global __qa_chain
    if __qa_chain is None:
        __qa_chain = (
            {"context": __retriever | __format_docs, "question": RunnablePassthrough()}
            | __rag_prompt
            | __model
            | StrOutputParser()
        )
    return __qa_chain


if __name__ == '__main__':
   model_endpoint = llm_inference_endpoint()

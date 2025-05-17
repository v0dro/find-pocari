# Get a query from the user.
# Ask Llama 3.2 the answer to the user's question.
# Find the price from amazon for a product of that name using the RAG database.
# Return the answer to the user.

# This one runs locally. Other functions are in the cloud and can cost money.
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_ollama import OllamaLLM

def get_embedding_function():
    # Converting the text to embeddings helps the model understand the meaning of the text
    # using a measure of simiarity between the target and evaluation text using cosine similarity.
    model_name = "sentence-transformers/all-mpnet-base-v2"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': False}
    hf = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

    return hf

def add_to_chroma(docs: list[Document]):
    # Create a Chroma vector store
    embedding_function = get_embedding_function()
    vectorstore = Chroma.from_documents(
        docs, 
        embedding_function)
    
    return vectorstore

vector_store = add_to_chroma(
    [
        Document(page_content=open("pocari_details.md").read(), metadata={"source": "kakaku_data"})
    ]
)
retriever = vector_store.as_retriever()
llm = OllamaLLM(model="llama3.2")
prompt = PromptTemplate(
    template="You are an assistant in a store. Give more details about the product and tell its price from the provided documents.\n\nContext: {context}\n\nQuestion: {input}\n\nAnswer:",
    input_variables=["context", "input"]
)

document_chain = create_stuff_documents_chain(llm, prompt)
retriever_chain = create_retrieval_chain(retriever, document_chain)

out = retriever_chain.invoke({"input" : "What is Pocari Sweat and what is the price online?"})
print(out['answer'])
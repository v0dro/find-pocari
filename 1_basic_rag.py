# Get a query from the user.
# Ask Llama 3.2 the answer to the user's question.
# Find the price from amazon for a product of that name using the RAG database.
# Return the answer to the user.

# This one runs locally. Other functions are in the cloud and can cost money.
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

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
    print(embedding_function)
    vectorstore = Chroma.from_documents(
        docs, 
        embedding_function)
    
    return vectorstore

v = add_to_chroma(
    [
        Document(page_content=open("kakaku_prices.md").read(), metadata={"source": "kakuku_data"})
    ]
)
print(v)
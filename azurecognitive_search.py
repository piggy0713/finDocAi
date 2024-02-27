import os
import tempfile
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Azure Blob Service Client
conn_str = os.getenv("AZURE_CONN_STRING")
container_name = os.getenv("AZURE_CONTAINER_NAME")
blob_service_client = BlobServiceClient.from_connection_string(conn_str)
container_client = blob_service_client.get_container_client(container_name)

model: str = "text-embedding-3-small"
deployment: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
openai_key: str = os.getenv("AZURE_OPENAI_API_KEY")
openai_base: str = os.getenv("AZURE_OPENAI_API_BASE")
vector_store_address: str = os.getenv("AZURE_SEARCH_SERVICE_URL")


embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(model=model,deployment=deployment,azure_endpoint=openai_base,
                              openai_api_type='azure',
                              openai_api_key=openai_key, chunk_size=1)
index_name: str = "findoc-demo"
vector_store: AzureSearch = AzureSearch(
    azure_search_endpoint=vector_store_address,
    azure_search_key=os.environ.get("AZURE_COGNITIVE_SEARCH_API_KEY"),
    index_name=index_name,
    embedding_function=embeddings.embed_query,
)

# List and process blobs (PDF files)
blob_list = container_client.list_blobs()  # This lists all blobs in the container
docs = []
for blob in blob_list:
    blob_client = container_client.get_blob_client(blob)
    with tempfile.NamedTemporaryFile(delete=False) as temp_pdf:
        download_stream = blob_client.download_blob()
        download_stream.readinto(temp_pdf)
        temp_pdf.seek(0)  # Go to the beginning of the tempfile to read it

        # Use PyPDFLoader to read and process the PDF file
        loader = PyPDFLoader(temp_pdf.name)
        pages = loader.load_and_split()

        # Further processing
        text_splitter = CharacterTextSplitter(chunk_size=150, chunk_overlap=20)
        split_pages = text_splitter.split_documents(pages)
        docs.extend(split_pages)

# Add processed documents to vector store
vector_store.add_documents(documents=docs)

print("Data loaded into vectorstore successfully")

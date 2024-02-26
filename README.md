# Document AI Demo Application 🤖

## Prerequisites

For this project, ensure you have set up:

1. **Azure Container Registry**: To manage the Docker images.
2. **App Services**: Where the application will be hosted.
3. **Blob Storage**: For storing unstructured data.
4. **Azure Cognitive Search**: Powers the application's Q&A functionality.
5. **OpenAI API Key**: For generating natural language model responses.

## Configuration

### `.env.example`

```bash
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
AZURE_COGNITIVE_SEARCH_SERVICE_NAME=YOUR_AZURE_COGNITIVE_SEARCH_SERVICE_NAME
AZURE_COGNITIVE_SEARCH_INDEX_NAME=YOUR_AZURE_COGNITIVE_SEARCH_INDEX_NAME
AZURE_COGNITIVE_SEARCH_API_KEY=YOUR_AZURE_COGNITIVE_SEARCH_API_KEY
AZURE_CONN_STRING=YOUR_AZURE_CONN_STRING
CONTAINER_NAME=YOUR_CONTAINER_NAME
```

Replace placeholder values (`YOUR_...`) with actual values from your environment.

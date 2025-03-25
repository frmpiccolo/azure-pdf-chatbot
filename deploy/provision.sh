#!/bin/bash

# Variables
RESOURCE_GROUP="pdf-chatbot"
LOCATION="eastus"
STORAGE_ACCOUNT="pdfchatbotstorage$RANDOM"
CONTAINER_NAME="pdf-files"
SEARCH_SERVICE="pdf-chatbot-cognitivesearch"
SEARCH_INDEX="pdf-index"
OPENAI_NAME="pdf-chatbot-openai"
DEPLOYMENT_NAME="gpt35"
OPENAI_MODEL="gpt-35-turbo"
OPENAI_VERSION="2023-05-15"

echo "🔧 Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

echo "📦 Creating storage account..."
az storage account create --name $STORAGE_ACCOUNT --location $LOCATION --resource-group $RESOURCE_GROUP --sku Standard_LRS
CONNECTION_STRING=$(az storage account show-connection-string --name $STORAGE_ACCOUNT --resource-group $RESOURCE_GROUP --query connectionString -o tsv)
az storage container create --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT --public-access off

echo "🔍 Creating Azure Cognitive Search..."
az search service create --name $SEARCH_SERVICE --resource-group $RESOURCE_GROUP --location $LOCATION --sku basic

echo "📑 Creating search index with vector search..."
curl -X PUT "https://$SEARCH_SERVICE.search.windows.net/indexes/$SEARCH_INDEX?api-version=2023-07-01-Preview" \
  -H "Content-Type: application/json" \
  -H "api-key: $(az search admin-key show --resource-group $RESOURCE_GROUP --service-name $SEARCH_SERVICE --query primaryKey -o tsv)" \
  -d '{
    "name": "'"$SEARCH_INDEX"'",
    "fields": [
      { "name": "id", "type": "Edm.String", "key": true, "searchable": false, "retrievable": true },
      { "name": "content", "type": "Edm.String", "searchable": true, "retrievable": true },
      { "name": "contentVector", "type": "Collection(Edm.Single)", "searchable": true, "retrievable": true, "vectorSearchDimensions": 1536, "vectorSearchConfiguration": "default" }
    ],
    "vectorSearch": {
      "algorithmConfigurations": [
        {
          "name": "default",
          "kind": "hnsw",
          "hnswParameters": {
            "m": 4,
            "efConstruction": 400
          }
        }
      ]
    }
  }'

echo "🤖 Creating Azure OpenAI resource..."
az cognitiveservices account create \
  --name $OPENAI_NAME \
  --resource-group $RESOURCE_GROUP \
  --kind OpenAI \
  --sku S0 \
  --location $LOCATION \
  --yes \
  --custom-domain

echo "⏳ Waiting for OpenAI resource to be ready..."
sleep 30

echo "🚀 Deploying OpenAI model..."
az cognitiveservices account deployment create \
  --resource-group $RESOURCE_GROUP \
  --name $OPENAI_NAME \
  --deployment-name $DEPLOYMENT_NAME \
  --model-name $OPENAI_MODEL \
  --model-version $OPENAI_VERSION \
  --model-format OpenAI \
  --sku-name Standard

echo ""
echo "✅ Done! Save the following values to your .env file:"
echo "AZURE_OPENAI_ENDPOINT=https://$OPENAI_NAME.openai.azure.com"
echo "AZURE_OPENAI_KEY=$(az cognitiveservices account keys list --name $OPENAI_NAME --resource-group $RESOURCE_GROUP --query key1 -o tsv)"
echo "AZURE_SEARCH_ENDPOINT=https://$SEARCH_SERVICE.search.windows.net"
echo "AZURE_SEARCH_KEY=$(az search admin-key show --resource-group $RESOURCE_GROUP --service-name $SEARCH_SERVICE --query primaryKey -o tsv)"
echo "AZURE_STORAGE_CONNECTION_STRING=$CONNECTION_STRING"
echo "AZURE_STORAGE_CONTAINER=$CONTAINER_NAME"
echo "AZURE_SEARCH_INDEX=$SEARCH_INDEX"

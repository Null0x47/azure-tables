# Azure Tables

Documentation for Microsoft cloud security logging can sometimes be difficult to locate or navigate. Fortunately, Azure Log Analytics workspaces provide predefined table schemas for most (if not all) relevant security logs, enabling streamlined log ingestion. Leveraging the Azure Management API, I queried these tables and developed a lightweight frontend to make the JSON response easily searchable.

## Running Locally with Docker

To run the container use the pre-built image:

```bash
docker run -p 8080:80 --name azure-tables null0x47/azure-tables:latest
```

Alternatively, you can use the provided `docker-compose.yml` file to build and run the image locally:

```bash
docker compose up
```

Once the container is running, the frontend will be accessible at: `localhost:8080`

## Exporting Table Definitions

The exported Azure Log Analytics table definitions are included in this repository as `tables.json`, located at the project root.

### Running Your Own Export

To generate your own export, a Python script is provided. It requires a `Subscription ID`, `Resource Group` and `Workspace Name`. The script uses `DefaultAzureCredential` for authentication, so a valid Azure CLI session is required.

Run the script using uv (or adjust for your environment):

```bash
uv sync && uv run main.py
```

### Manual API Request

If you prefer to interact with the Azure Management API directly, you can use the following curl command to retrieve the LAW table definitions:

```bash
curl -X GET \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  "https://management.azure.com/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.OperationalInsights/workspaces/<WORKSPACE_NAME>/tables?api-version=2025-07-01"
```

Make sure to replace placeholders (`<ACCESS_TOKEN>`, `<SUBSCRIPTION_ID>` and `<RESOURCE_GROUP>`) with your actual values.
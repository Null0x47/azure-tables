# Azure Tables

Overview of all pre-defined tables within a Sentinel enabled Azure Log Analytics workspace

## The Problem

As a defensive security engineer, one of my biggest frustrations with Microsoft Azure, Microsoft 365, and Entra ID is the lack of consistent, centralized documentation for their security logs. While many Defender XDR-related logs are documented on learn.microsoft.com, they’re often outdated. Documentation for other logs is even more difficult to locate, as it’s scattered across various Microsoft products and platforms.

## The Solution

We can create this documentation ourselves by dumping the pre-defined tables from a Log Analytics workspace via the 
Azure management api:

```bash
curl -X GET \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  "https://management.azure.com/subscriptions/<SUBSCRIPTION_ID>/resourceGroups/<RESOURCE_GROUP>/providers/Microsoft.OperationalInsights/workspaces/<WORKSPACE_NAME>/tables?api-version=2021-12-01-preview"
```

If we run this on a fresh LAW without Sentinel enabled it returns 618 tables. Once we enable Sentinel for our LAW it adds the table definitions that are needed to support all available data connectors. If we run this after enabling Sentinel we get a total of 740 tables! In my experience this is the most complete list of (security) logs + definitions related to Microsoft cloud products.

This repository also provides a python script that does the same as the curl command mentioned above. It also updates the `tables.json` file located in the root of this project:

```bash
uv sync && uv run main.py
```

This script will ask for the `Subscription ID`, `Resource Group` and `Workspace Name`. It uses `DefaultAzureCredential` for authentication so it requires you to have a valid session on your machine. This can be acquired via the Azure CLI:

```bash
az login
```
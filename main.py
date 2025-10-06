import json

import requests
from azure.identity import DefaultAzureCredential

API_VERSION = "2025-07-01"

if __name__ == "__main__":
    subscription_id = input("Subscription ID: ")
    resource_group = input("Resource Group: ")
    workspace_name = input("Workspace Name: ")

    credential = DefaultAzureCredential()
    token = credential.get_token("https://management.azure.com/.default").token

    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.OperationalInsights/workspaces/{workspace_name}/tables?api-version={API_VERSION}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    print("Exporting tables...")
    response = requests.get(url, headers=headers)
    tables = json.loads(json.dumps(response.json())).get("value")

    # Anonymize
    for table in tables:
        table["id"] = (
            table.get("id")
            .replace(subscription_id, "<SUBSCRIPTION_ID>")
            .replace(resource_group, "<RESOURCE_GROUP>")
            .replace(workspace_name, "<WORKSPACE_NAME>")
        )

    with open("tables.json", "w", encoding="utf-8") as export:
        export.write(json.dumps(tables))

    print("Done!")

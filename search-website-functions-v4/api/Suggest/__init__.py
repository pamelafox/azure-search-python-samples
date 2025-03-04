import json
import logging

import azure.functions as func
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from shared_code import azure_config

environment_vars = azure_config()

# curl --header "Content-Type: application/json" \
#  --request POST \
#  --data '{"q":"code","top":"5", "suggester":"sg"}' \
#  http://localhost:7071/api/Suggest

# Set Azure Search endpoint and key
service_name = environment_vars["search_service_name"]
endpoint = f"https://{service_name}.search.windows.net"
key = environment_vars["search_api_key"]

# Your index name
index_name = "good-books"

# Create Azure SDK client
search_client = SearchClient(endpoint, index_name, AzureKeyCredential(key))


def main(req: func.HttpRequest) -> func.HttpResponse:

    # variables sent in body
    req_body = req.get_json()
    query = req_body.get("q")
    top = req_body.get("top", 5)
    suggester = req_body.get("suggester", "sg")

    if query:
        logging.info("/Suggest q = %s", query)
        suggestions = search_client.suggest(search_text=query, suggester_name=suggester, top=top)

        # format the React app expects
        full_response = {}
        full_response["suggestions"] = suggestions
        print(suggestions)

        return func.HttpResponse(
            body=json.dumps(full_response), mimetype="application/json", status_code=200
        )

    return func.HttpResponse("No query param found.", status_code=200)

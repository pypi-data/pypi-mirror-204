API_ROUTE="api/v1"


GRAPHMART_ENDPOINT="graphmart"
GRAPHMART_OPERATIONS_ENDPOINT = {
    "listGraphmart": {
        "endpoint": "graphmart",
        "requestType": "GET",
        "parameters":[]
        
    }
  #  "/api/v1/graphmarts/http%3A%2F%2Ftest.com%2F234'"
    
    "retrieveGraphmart": {
        "endpoint": "graphmart"
        "requestType": "POST"
        "parameters": ["graphmart_uri"]
    }
}

def with_api_request_url(self, host: str, port: str, operation:str) -> None:
    """Adds the url to the AnzoRequestBuilder.

    Raises:
        RuntimeError: If the url has already been set.
    """
    url = f'https://{host}'
    if port:
        url += f":{port}"
    url += API_ROUTE

    # if self.base_url:
    #     raise RuntimeError("Base URL has already been set")
    if operation in GRAPHMART_OPERATIONS_ENDPOINT:
        val = GRAPHMART_OPERATIONS_ENDPOINT[operation]
        request_type = val["requestType"]
        parameters = val["parameters"]
        endpoint = val["endpoint"]
    
    self.base_url = url
    
    




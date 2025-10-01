import json
from fastapi.testclient import TestClient
from solution import app

client = TestClient(app)

# Define the endpoints with methods and data if necessary
endpoints = [
    {"method": "get", "url": "/crew_path/2/Engineer"}
]

for endpoint in endpoints:
    method = endpoint["method"].lower()
    url = endpoint["url"]
    
    try:
        match method:
            case "get":
                response = client.get(url)
            case "post":
                response = client.post(url)
            case "put":
                response = client.put(url)
            case "delete":
                response = client.delete(url)
            case _:
                print(f"Unsupported method: {method}")
                continue

        response.raise_for_status()  # Raise an error for bad status codes
        response_json = response.json()
        print(f"Response from {method.upper()} {url} :")
        print(json.dumps(response_json, indent=4), "\n")
    except Exception as e:
        print(f"Error accessing {method.upper()} {url}: {e}\n")
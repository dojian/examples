from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

crew = [
    {"id": 1, "name": "Cosmo", "role": "Captain"},
    {"id": 2, "name": "Alice", "role": "Engineer"},
    {"id": 3, "name": "Bob", "role": "Scientist"}
]


# TODO: Define middleware to handle all incoming HTTP requests
# - Use try-except block to catch any unexpected exceptions.
# - Use call_next(request) within the try block to process the request.
# - In case of exception return a status code of 500 with a JSON payload containing a detail message: 
#   "Oops! Something went wrong and we caught it! Our middleware is on it!"
@app.middleware("http")
async def http_middleware_error_handler(request:Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        return JSONResponse(
            status_code = 500,
            content = {"detail":"Oops! Something went wrong and we caught it! Our middleware is on it!"}
        )

# Example endpoint with an unexpected exception
@app.get("/crew/{crew_id}")
async def read_crew_member(crew_id: int):
    # Raise 404 error if the ID is invalid
    if crew_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid crew ID. Must be a positive integer.")

    # Fetch and return the crew member details if they exist
    for member in crew:
        if member["id"] == crew_id:
            return non_existent_variable  # Intentional error in the code to test exception handler

    # Raise 404 error if the crew member is not found
    raise HTTPException(status_code=404, detail="Crew member not found")
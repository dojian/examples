from fastapi import FastAPI

# Initialize a FastAPI app instance
app = FastAPI()

# Mock database of crew members
crew = [
    {"id": 1, "name": "Cosmo", "role": "Captain"},
    {"id": 2, "name": "Alice", "role": "Engineer"},
    {"id": 3, "name": "Bob", "role": "Scientist"}
]


# TODO: Include another path parameter "role" to retrieve a crew member alongside crew_id
@app.get("/crew_path/{crew_id}/{role}")
def read_crew_member_by_path(crew_id: int,role: str):
    for member in crew:
        if member["id"] == crew_id and member["role"] == role:
            return member
    return {"message": "Crew member not found"}
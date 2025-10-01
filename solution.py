from fastapi import FastAPI

# Initialize a FastAPI app instance
app = FastAPI()

# Mock database of crew members
crew = [
    {"id": 1, "name": "Cosmo", "role": "Captain"},
    {"id": 2, "name": "Alice", "role": "Engineer"},
    {"id": 3, "name": "Bob", "role": "Scientist"}
]


# TODO: Write an endpoint to get a crew member by path parameter (Endpoint: /crew_with_path/{crew_id})
@app.get("/crew_with_path/{crew_id}")
def get_member(crew_id:int):
    for member in crew:
        if member["id"]==crew_id:
            return member
    return {"message":"Crew member not found"}
    
# TODO: Write an endpoint to get a crew member by query parameter (Endpoint: /crew_with_query/member)
@app.get("/crew_with_query/member")
def get_member_by_query(crew_id:int):
    for member in crew:
        if member["id"]==crew_id:
            return member
    return {"message":"Crew member not found"}
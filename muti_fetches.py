from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio

app = FastAPI()

user_db = {
    1:{"user_id":1, "name": "Alice"}, 
    2:{"user_id":2, "name": "Bob"}
    }

orders = {
    1: [{"id": 101, "item": "Laptop"}, {"id": 102, "item": "Mouse"}],
    2: [{"id": 103, "item": "Keyboard"}]
}

# Additional mock data for notifications
notifications = {
    1: [{"id": 201, "message": "Welcome back!"}, {"id": 202, "message": "Your order has shipped."}],
    2: [{"id": 203, "message": "New promotion available!"}]
}

async def fetch_user(user_id: int):
    await asyncio.sleep(0.2) #simulate a delay
    user = user_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def fetch_orders(user_id: int):
    order = orders.get(user_id, [])
    if not order:
        raise HTTPException(status_code=404, detail="Orders not found")
    return order

async def fetch_notifications(user_id: int):
    notification = notifications.get(user_id, [])
    if not notification:
        raise HTTPException(status_code=404, detail="Notifications not found")
    return notification

async def retry(fn, retries=2, delay=0.2, *args,**kwargs):
    for i in range(retries):
        try:
            return await fn(*args,**kwargs)
        except Exception as e:
            if i == retries - 1:
                raise e
            await asyncio.sleep(delay)
            
# Pydantic Models
class Order(BaseModel):
    id: int
    item: str
    
class Notification(BaseModel):
    id: int
    message: str

class User(BaseModel):
    id: int
    name: str

class DashboardResponse(BaseModel):
    user: User
    orders: list[Order]
    notifications: list[Notification] | None

#Main API endpoint

@app.get("/dashboard/{user_id}", response_model=DashboardResponse)
async def get_dashabord(user_id: int):
    try: 
        user_task = asyncio.create_task(fetch_user(user_id))
        orders_task = asyncio.create_task(fetch_orders(user_id))
        notifications_task = asyncio.create_task(retry(fetch_notifications,user_id=user_id))

        user, orders, notifications = await asyncio.gather(user_task, orders_task, notifications_task, return_exception = True)

        if isinstance(user,Exception):
            raise user
        if isinstance(orders,Exception):
            orders = []
        if isinstance(notifications,Exception):
            notifications = None
        return {
            "user": user,
            "orders": orders,
            "notifications": notifications
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail =str(e))



    
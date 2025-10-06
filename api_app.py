from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from typing import List
import time
import asyncio

app = FastAPI()

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for testing/demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Rate Limit Middleware ---
class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int, window_seconds: int):
        super().__init__(app)
        self.max_requests = max_requests
        self.window = window_seconds
        self.client_requests = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        now = time.time()
        request_times = self.client_requests[client_ip]
        self.client_requests[client_ip] = [t for t in request_times if now - t < self.window]

        if len(self.client_requests[client_ip]) >= self.max_requests:
            return HTTPException(status_code=429, detail="Too many requests")

        self.client_requests[client_ip].append(now)
        return await call_next(request)

# Allow 5 requests per 10 seconds
app.add_middleware(RateLimitMiddleware, max_requests=5, window_seconds=10)

# --- Fake async data fetchers ---
async def fetch_user(user_id: int):
    await asyncio.sleep(0.1)  # simulate delay
    if user_id == 1:
        return {"id": 1, "name": "Anna"}
    return None

async def fetch_orders(user_id: int) -> List[dict]:
    await asyncio.sleep(0.2)
    return [{"id": 100, "item": "Keyboard"}, {"id": 101, "item": "Mouse"}]

async def fetch_notifications(user_id: int) -> List[str]:
    await asyncio.sleep(0.15)
    return ["Welcome back!", "New discount on accessories."]

# --- Main endpoint ---
@app.get("/user-info")
async def get_user_info(user_id: int):
    # Fetch all three in parallel
    user_task = fetch_user(user_id)
    orders_task = fetch_orders(user_id)
    notifications_task = fetch_notifications(user_id)

    user, orders, notifications = await asyncio.gather(
        user_task, orders_task, notifications_task, return_exceptions=True
    )

    # Handle individual failures gracefully
    if isinstance(user, Exception) or user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if isinstance(orders, Exception):
        orders = []
    if isinstance(notifications, Exception):
        notifications = None

    return {
        "user": user,
        "orders": orders,
        "notifications": notifications
    }

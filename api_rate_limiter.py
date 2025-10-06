import time
from collections import defaultdict
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class SlidingWindowRateLimiter(BaseHTTPMiddleware):
    def __init__(self,app, limit: int, window_size: int):
        super().__init__(app)
        self.limit = limit 
        self.window_size = window_size
        self.client_requests = defaultdict(list)
        
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()
        
        # Remove timestamps outside the sliding window
        self.client_requests[client_ip] = [
            timestamp for timestamp in self.client_requests[client_ip]
            if current_time - timestamp < self.window_size
        ]
        
        if len(self.client_requests[client_ip]) < self.limit:
            self.client_requests[client_ip].append(current_time)
            response = await call_next(request)
            return response
        else:
            return Response(content="Too Many Requests", status_code=429)


class TokenBucketRateLimiter(BaseHTTPMiddleware):
    def __init__(self, app, refill_rate: int, capacity:int):
        super().__init__(app)
        self.refill_rate = refill_rate
        self.capacity = capacity
        self.buckets = defaultdict(lambda: {"tokens": capacity, "last_refill": time.time()})

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        bucket = self.buckets[client_ip]
        now = time.time()

        # Refill tokens
        elapsed = now - bucket["last_refill"]
        refill_amount = elapsed * self.refill_rate
        bucket["tokens"] = min(self.capacity, bucket["tokens"] + refill_amount)
        bucket["last_refill"] = now

        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return await call_next(request)
        else:
            return Response("Too Many Requests", status_code=429)
        

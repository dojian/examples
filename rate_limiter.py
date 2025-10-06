### **Requirements:**

## 1. **Rate Limiter Middleware:**
##    - For each unique client IP, allow **`X`** requests every **`Y`** seconds.
##    - If a request exceeds the limit, it should be rejected with an appropriate response.
###
import time
from collections import defaultdict
from fastapi import HTTPError

X=1
Y=2
client_requests = defaultdict(list)
def allow_request(client_ip:str) -> bool:
    current_time = time.time()
    # Filter out timestamps older than Y seconds
    recent_requests = [t for t in client_requests[client_ip] if current_time - t < Y]
    client_requests[client_ip] = recent_requests  # Clean up old requests
    
    if len(client_requests[client_ip]) < X:
        client_requests[client_ip].append(current_time)
        return True
    return False


def process_request(client_ip):
    if not allow_request(client_ip):
        return HTTPError(status_code = 429,detail ="Too many requests")  # Return HTTP 429 Too Many Requests.
    return 200  
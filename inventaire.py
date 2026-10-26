import json
import os
from datetime import datetime

import requests

DOCKER = os.environ.get("DOCKER_API_URL", "http://127.0.0.1:2375")
NETBOX = os.environ.get("NETBOX_URL", "http://127.0.0.1:8080")
JETON = os.environ["NETBOX_TOKEN"]
TIMEOUT = 10

session = requests.Session()

netbox = requests.Session()
netbox.headers.update({
    "Authorization": f"Bearer {JETON}",
    "Accept": "application/json",
})


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


def tout_lire(session, url):
    resultats = []
    while url:
        reponse = session.get(url, timeout=TIMEOUT)
        reponse.raise_for_status()
        page = reponse.json()
        resultats.extend(page["results"])
        url = page["next"]
    return resultats


def releve_netbox():
    reponse = netbox.get(f"{NETBOX}/api/status/", timeout=TIMEOUT)
    reponse.raise_for_status()
    version = reponse.json()["netbox-version"]

    types_objets = tout_lire(netbox, f"{NETBOX}/api/core/object-types/?limit=50")

    reponse = netbox.get(f"{NETBOX}/api/core/object-types/?limit=1", timeout=TIMEOUT)
    reponse.raise_for_status()
    count_annonce = reponse.json()["count"]

    return {
        "version": version,
        "types_objets": len(types_objets),
        "types_objets_annonces": count_annonce,
    }


reponse = session.get(f"{DOCKER}/containers/json", params={"all": "true"}, timeout=TIMEOUT)
reponse.raise_for_status()

conteneurs = []
for c in reponse.json():
    conteneur = {
        "nom": c["Names"][0].lstrip("/"),
        "image": c["Image"],
        "etat": c["State"],
        "cpu_pourcent": None,
        "memoire_mo": None,
    }
    if c["State"] == "running":
        pourcent, memoire_mo = lire_stats(c["Id"])
        conteneur["cpu_pourcent"] = round(pourcent, 2)
        conteneur["memoire_mo"] = round(memoire_mo, 1)
    conteneurs.append(conteneur)

inventaire = {
    "date_releve": datetime.now().astimezone().isoformat(timespec="seconds"),
    "conteneurs": conteneurs,
    "netbox": releve_netbox(),
}

with open("inventaire.json", "w", encoding="utf-8") as f:
    json.dump(inventaire, f, indent=2, ensure_ascii=False)

demarres = [c for c in conteneurs if c["etat"] == "running"]
print(f"Relevé du {inventaire['date_releve']}")
print(f"{len(conteneurs)} conteneurs, dont {len(demarres)} démarrés\n")
print(f"{'NOM':<20} {'IMAGE':<25} {'ÉTAT':<10} {'CPU %':>6} {'RAM Mo':>8}")
for c in conteneurs:
    cpu = f"{c['cpu_pourcent']:.1f}" if c["cpu_pourcent"] is not None else "-"
    ram = f"{c['memoire_mo']:.1f}" if c["memoire_mo"] is not None else "-"
    print(f"{c['nom']:<20} {c['image']:<25} {c['etat']:<10} {cpu:>6} {ram:>8}")
print(f"\nMémoire totale des conteneurs démarrés : {sum(c['memoire_mo'] for c in demarres):.1f} Mo")

nb = inventaire["netbox"]
print(f"\nNetBox {nb['version']} : {nb['types_objets']} types d'objets lus "
      f"(NetBox en annonce {nb['types_objets_annonces']})")
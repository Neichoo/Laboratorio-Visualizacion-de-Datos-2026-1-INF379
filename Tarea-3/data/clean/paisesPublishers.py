import pandas as pd
import requests
import time

# Archivo con una columna llamada publisher
INPUT_FILE = "publishers_unicos.csv"

publishers = pd.read_csv(INPUT_FILE)

results = []

USER_AGENT = "VideoGamePublisherCountryLookup/1.0"

def search_wikidata_entity(name):
    url = "https://www.wikidata.org/w/api.php"

    params = {
        "action": "wbsearchentities",
        "search": name,
        "language": "en",
        "format": "json",
        "limit": 1
    }

    r = requests.get(
        url,
        params=params,
        headers={"User-Agent": USER_AGENT},
        timeout=20
    )

    data = r.json()

    if data.get("search"):
        return data["search"][0]["id"]

    return None


def get_country_from_entity(qid):
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"

    r = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=20
    )

    data = r.json()

    entity = data["entities"][qid]
    claims = entity.get("claims", {})

    # País (P17)
    if "P17" in claims:
        try:
            country_qid = claims["P17"][0]["mainsnak"]["datavalue"]["value"]["id"]
            return country_qid
        except:
            pass

    # Headquarters location (P159)
    if "P159" in claims:
        try:
            hq_qid = claims["P159"][0]["mainsnak"]["datavalue"]["value"]["id"]
            return hq_qid
        except:
            pass

    return None


def get_entity_label(qid):
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"

    r = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=20
    )

    data = r.json()

    entity = data["entities"][qid]

    labels = entity.get("labels", {})

    if "en" in labels:
        return labels["en"]["value"]

    return None


for publisher in publishers["publisher"].dropna().unique():

    print(f"Buscando: {publisher}")

    country = None

    try:
        entity_qid = search_wikidata_entity(publisher)

        if entity_qid:
            country_qid = get_country_from_entity(entity_qid)

            if country_qid:
                country = get_entity_label(country_qid)

    except Exception as e:
        print("Error:", e)

    results.append({
        "publisher": publisher,
        "country": country
    })

    time.sleep(0.5)

publisher_country = pd.DataFrame(results)

publisher_country.to_csv(
    "publisher_country.csv",
    index=False,
    encoding="utf-8-sig"
)

print("Generado: publisher_country.csv")
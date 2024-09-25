"""
This module handles the extraction of possible classifications of intellectuals based 
on data retrieved via SPARQL from Wikidata. The selection of which classifications are 
of interest is done manually afterward.
"""

import os
import csv
from pathlib import Path
from dotenv import load_dotenv
from SPARQLWrapper import JSON, SPARQLWrapper

load_dotenv()
data_raw_dir = Path(os.getenv("DATA_RAW_DIR"))
output_file = data_raw_dir / "occupations.csv"

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

QUERY = """
SELECT ?occupation ?occupationLabel WHERE {
  ?occupation wdt:P31 wd:Q28640.  # Selecionar ocupações (Q28640)
  FILTER NOT EXISTS { ?occupation wdt:P279 ?subclassOf. }  # Excluir ocupações que são subclasses
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
"""

sparql.setQuery(QUERY)
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    for result in results["results"]["bindings"]:
        occupation = result["occupationLabel"]["value"]
        writer.writerow([occupation])

print(f"CSV saved at: {output_file}")

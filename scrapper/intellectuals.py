from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict

# Definir o endpoint SPARQL do Wikidata
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

# Consulta SPARQL atualizada com propriedades adicionais
query = """
SELECT ?person ?personLabel ?givenNameLabel ?familyNameLabel ?birthDate ?citizenshipLabel 
       ?languagesLabel ?occupationLabel ?educatedAtLabel ?doctoralAdvisorLabel ?doctoralStudentLabel 
       ?influencedByLabel WHERE {
  ?person wdt:P737 ?influencedBy.        # Pessoas influenciadas por alguém
  ?person wdt:P31 wd:Q5.                 # Filtrar apenas seres humanos
  ?influencedBy wdt:P31 wd:Q5.           # Influenciador também deve ser um ser humano
  
  OPTIONAL { ?person wdt:P735 ?givenName. }           # Nome próprio
  OPTIONAL { ?person wdt:P734 ?familyName. }          # Sobrenome
  OPTIONAL { ?person wdt:P569 ?birthDate. }           # Data de nascimento
  OPTIONAL { ?person wdt:P27 ?citizenship. }          # País de cidadania
  OPTIONAL { ?person wdt:P1412 ?languages. }          # Idiomas falados ou escritos
  OPTIONAL { ?person wdt:P106 ?occupation. }          # Ocupação
  OPTIONAL { ?person wdt:P69 ?educatedAt. }           # Educado em
  OPTIONAL { ?person wdt:P184 ?doctoralAdvisor. }     # Orientador de doutorado
  OPTIONAL { ?person wdt:P185 ?doctoralStudent. }     # Aluno de doutorado
  
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }  # Garantir rótulos em inglês
}
LIMIT 50
"""

# Definir a consulta no endpoint
sparql.setQuery(query)
sparql.setReturnFormat(JSON)

# Executar a consulta e obter os resultados
results = sparql.query().convert()

# Usar defaultdict para agrupar os resultados por pessoa
data_by_person = defaultdict(
    lambda: {
        "given_name": None,
        "family_name": None,
        "birth_date": None,
        "citizenship": set(),
        "languages": set(),
        "occupation": set(),
        "educated_at": set(),
        "doctoral_advisor": set(),
        "doctoral_student": set(),
        "influenced_by": set(),
    }
)

# Processar os resultados e agrupar os dados por pessoa
for result in results["results"]["bindings"]:
    person = result["personLabel"]["value"]
    given_name = result.get("givenNameLabel", {}).get("value", None)
    family_name = result.get("familyNameLabel", {}).get("value", None)
    birth_date = result.get("birthDate", {}).get("value", None)
    citizenship = result.get("citizenshipLabel", {}).get("value", None)
    languages = result.get("languagesLabel", {}).get("value", None)
    occupation = result.get("occupationLabel", {}).get("value", None)
    educated_at = result.get("educatedAtLabel", {}).get("value", None)
    doctoral_advisor = result.get("doctoralAdvisorLabel", {}).get("value", None)
    doctoral_student = result.get("doctoralStudentLabel", {}).get("value", None)
    influenced_by = result.get("influencedByLabel", {}).get("value", None)

    # Preencher o dicionário com os valores encontrados
    person_data = data_by_person[person]
    if given_name:
        person_data["given_name"] = given_name
    if family_name:
        person_data["family_name"] = family_name
    if birth_date:
        person_data["birth_date"] = birth_date
    if citizenship:
        person_data["citizenship"].add(citizenship)
    if languages:
        person_data["languages"].add(languages)
    if occupation:
        person_data["occupation"].add(occupation)
    if educated_at:
        person_data["educated_at"].add(educated_at)
    if doctoral_advisor:
        person_data["doctoral_advisor"].add(doctoral_advisor)
    if doctoral_student:
        person_data["doctoral_student"].add(doctoral_student)
    if influenced_by:
        person_data["influenced_by"].add(influenced_by)

# Imprimir os resultados agrupados
for person, details in data_by_person.items():
    print(f"Person: {person}")
    print(f"Given Name: {details['given_name']}")
    print(f"Family Name: {details['family_name']}")
    print(f"Date of Birth: {details['birth_date']}")
    print(f"Country of Citizenship: {list(details['citizenship'])}")
    print(f"Languages: {list(details['languages'])}")
    print(f"Occupation: {list(details['occupation'])}")
    print(f"Educated at: {list(details['educated_at'])}")
    print(f"Doctoral Advisor: {list(details['doctoral_advisor'])}")
    print(f"Doctoral Student: {list(details['doctoral_student'])}")
    print(f"Influenced by: {list(details['influenced_by'])}")
    print("-" * 50)

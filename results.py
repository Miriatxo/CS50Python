BY RUNNING...

import requests
import json

url = 'https://api.euskadi.eus/culture/events/v1.0/eventType'
headers = {'accept': 'application/json'}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print(json.dumps(data, indent=4))  # Imprime la estructura JSON de manera legible
else:
    print(f"Error: {response.status_code}")

... I GOT EVENT TYPES FROM 1 TO 16:

[
    {
        "id": "1",
        "nameEs": "Concierto",
        "nameEu": "Kontzertua"
    },
    {
        "id": "2",
        "nameEs": "Teatro",
        "nameEu": "Antzerkia"
    },
    {
        "id": "3",
        "nameEs": "Exposici\u00f3n",
        "nameEu": "Erakusketa"
    },
    {
        "id": "4",
        "nameEs": "Danza",
        "nameEu": "Dantza"
    },
    {
        "id": "6",
        "nameEs": "Conferencia",
        "nameEu": "Hitzaldia"
    },
    {
        "id": "7",
        "nameEs": "Bertsolarismo",
        "nameEu": "Bertsolaritza"
    },
    {
        "id": "8",
        "nameEs": "Feria",
        "nameEu": "Azoka"
    },
    {
        "id": "9",
        "nameEs": "Cine y audiovisuales",
        "nameEu": "Zinema eta ikus-entzunezkoak"
    },
    {
        "id": "10",
        "nameEs": "Eventos/jornadas",
        "nameEu": "Ekitaldiak/jardunaldiak"
    },
    {
        "id": "11",
        "nameEs": "Formaci\u00f3n",
        "nameEu": "Formakuntza"
    },
    {
        "id": "12",
        "nameEs": "Concurso",
        "nameEu": "Lehiaketa"
    },
    {
        "id": "13",
        "nameEs": "Festival",
        "nameEu": "Jaialdia"
    },
    {
        "id": "14",
        "nameEs": "Actividad Infantil",
        "nameEu": "Haur jarduera"
    },
    {
        "id": "15",
        "nameEs": "Otro",
        "nameEu": "Bestelakoa"
    },
    {
        "id": "16",
        "nameEs": "Fiestas",
        "nameEu": "Jaiak"
    }
]

... WITH THIS INFO, RUNNING THIS:

import requests
import json


url = 'https://api.euskadi.eus/culture/events/v1.0/eventType'
headers = {'accept': 'application/json'}
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    event_types = {event['nameEs'].lower(): event['id'] for event in data}
    print(event_types)
else:
    print(f"Error: {response.status_code}")

... I GOT THIS DICTIONARY THAT MAPS EVENT TYPES ONTO TYPE NUMBERS:

{'concierto': '1', 'teatro': '2', 'exposición': '3', 'danza': '4', 'conferencia': '6', 'bertsolarismo': '7',
 'feria': '8', 'cine y audiovisuales': '9', 'eventos/jornadas': '10', 'formación': '11', 'concurso': '12',
 'festival': '13', 'actividad infantil': '14', 'otro': '15', 'fiestas': '16'}

import datetime
import re
from datetime import timedelta

import requests
from bs4 import BeautifulSoup

# URL à la racine de vlr.gg
url = 'https://www.vlr.gg'
# URL listant les différentes competitions
url_events = 'https://www.vlr.gg/events'

links = []

# Requête GET à l'url
response = requests.get(url)
response_events = requests.get(url_events)

# Verification de la reussite de la requête
if response.status_code == 200 and response_events.status_code == 200:

    # Analyse du contenu HTML de la page d'évenements
    soup_events = BeautifulSoup(response_events.text, 'html.parser')

    # Sauvegarde des liens d'événements EMEA
    for link in soup_events.find_all(href=re.compile("emea")):
        if not link.find('span', class_='mod-completed'):
            links.append(url + link.get('href'))

    # Parcours des différentes competitions en EMEA
    for comp in links:
        # if not comp.__contains__('kickoff'):
        teams = []
        print('\n'+comp)
        r = requests.get(comp)
        soup_r = BeautifulSoup(r.text, 'html.parser')

        # Parcours des différentes équipes de la ligue
        for teamlist in soup_r.find_all(href=re.compile("/team/")):
            compteamslist = teamlist.find_parent('div', class_='event-teams-container')
            if compteamslist:
                teams.append(url + teamlist.get('href'))

        # Parcours des différents membres par équipe
        for url_team in teams:
            print(url_team)
            t = requests.get(url_team)
            soup_t = BeautifulSoup(t.text, 'html.parser')
            player = []
            staff = []


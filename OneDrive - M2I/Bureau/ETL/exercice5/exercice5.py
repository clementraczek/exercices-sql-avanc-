import requests
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()

BASE_URL = os.getenv("BASE_URL")
FILE_NAME = "meteo_villes.csv"
API_KEY = os.getenv("API_KEY")
# 1
VILLES = ["Lille", "Armentières", "Maubeuge", "Dunkerque", "Calais", "Bailleul", "Tourcoing", "Cambrai", "Comines", "Lens", "Arras"]

meteo_data = []

#2

print("Récupération des données..")

for city in VILLES: 
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric', 
        'lang': 'fr'      
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
        
    temperature = data['main']['temp']
    ressentie = data['main']['feels_like']
    humidite = data['main']['humidity']
    description = data['weather'][0]['description']
        
    meteo_data.append({
            'Ville': city,
            'Temperature_C': temperature,
            'Ressentie_C': ressentie,
            'Humidite_Pourcent': humidite,
            'Description': description
    })
    print(f"Données récupérées pour : {city}")
        


#3
df_meteo = pd.DataFrame(meteo_data)
print("DataFrame cétéo créé")
print(df_meteo)

#4
ville_chaude = df_meteo.loc[df_meteo['Temperature_C'].idxmax()]
print(f"Ville la plus chaude : {ville_chaude}")                            
ville_froide = df_meteo.loc[df_meteo['Temperature_C'].idxmin()]

print(f"Ville la plus froide : {ville_froide}")

#5
temp_moyenne = df_meteo['Temperature_C'].mean().__round__(2)
print(f"Température moyenne des villes : {temp_moyenne}°C")

# 6
df_meteo.to_csv(FILE_NAME, index=False, encoding='utf-8')
print(f"Résultats ont été sauvegardés dans le fichier {FILE_NAME}")

import requests
import pandas as pd


API = "https://restcountries.com/v3.1"

# 1
print(f"Récupération des données")
response = requests.get(f"{API}/region/europe?")
data = response.json()
print(f"Données récupérées")


#2
liste = []
for country in data:
    name = country.get('name', {}).get('common')
    capital= country.get('capital')
    population = country.get('population', 0)
    area = country.get('area', 0)
    liste.append({
        'Nom': name,
        'Capitale': capital,
        'Population': population,
        'Superficie': area
        })

df_europe = pd.DataFrame(liste)
df_europe['Superficie'] = df_europe['Superficie']

print("DataFramecréé")
print(df_europe)

#3
df_europe['Densite_hab_km2'] = df_europe['Population'] / df_europe['Superficie']
df_europe['Densite_hab_km2'] = df_europe['Densite_hab_km2'].round(2)

print("DataFrame après calcul de densité")
print(df_europe.head())

#4
top_5 = df_europe.sort_values(by='Population', ascending=False).head(5)
print(f"Top 5 pays par population : \n{top_5}")

#5
population_totale = df_europe['Population'].sum()
print(f"Population totale enrope : {population_totale} habitants")

#6
top_1_densite = df_europe.sort_values(by='Densite_hab_km2', ascending=False).head(1)
print(f"Pays le plus dense : \n{top_1_densite}")

#7
nom_fichier = "pays_europe.xlsx"
df_europe.to_excel(nom_fichier, index=False)
print(f"Résultats sauvegardés dans le fichier {nom_fichier}")

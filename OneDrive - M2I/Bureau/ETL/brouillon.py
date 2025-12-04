
# --- 2. Créer un DataFrame avec : nom, capitale, population, superficie ---
processed_data = []
for country in data:
    # On gère le cas où un pays pourrait avoir plusieurs noms (commun et officiel)
    name = country.get('name', {}).get('common', 'N/A')
    
    # La capitale est un tableau, on prend le premier élément s'il existe
    capital_list = country.get('capital')
    capital = capital_list[0] if capital_list else 'N/A'
    
    # La population et la superficie (area) peuvent être manquantes ou nulles
    population = country.get('population', 0)
    area = country.get('area', 0)
    
    processed_data.append({
        'Nom': name,
        'Capitale': capital,
        'Population': population,
        'Superficie_km2': area
    })

df_europe = pd.DataFrame(processed_data)
# On s'assure que 'Superficie_km2' est supérieur à zéro pour éviter la division par zéro
df_europe['Superficie_km2'] = df_europe['Superficie_km2'].replace(0, np.nan) 

print("\n--- DataFrame initial créé ---")
print(df_europe.head())

# --- 3. Calculer la densité de population (population / superficie) ---
df_europe['Densite_hab_km2'] = df_europe['Population'] / df_europe['Superficie_km2']
# On arrondit la densité à 2 décimales pour une meilleure lisibilité
df_europe['Densite_hab_km2'] = df_europe['Densite_hab_km2'].round(2)

# On retire la colonne temporaire créée pour la gestion du cas de division par zéro
df_europe['Superficie_km2'] = df_europe['Superficie_km2'].replace(np.nan, 0)
df_europe['Superficie_km2'] = df_europe['Superficie_km2'].astype(int)

# --- 4. Identifier les 5 pays les plus peuplés d'Europe ---
top_5_popules = df_europe.sort_values(by='Population', ascending=False).head(5)

# --- 5. Calculer la population totale de l'Europe ---
population_totale = df_europe['Population'].sum()

# --- 6. Trouver le pays avec la plus grande densité ---
# On ignore les pays avec une densité NaN (superficie nulle) pour ce classement
plus_grande_densite = df_europe.sort_values(
    by='Densite_hab_km2', 
    ascending=False, 
    na_position='last' # Met les NaN (superficie nulle) à la fin
).iloc[0]

# --- Affichage des résultats ---
print("\n--- Résultats de l'Analyse ---")
print(f"Population Totale de l'Europe : **{population_totale:,} habitants**")
print("\n**Pays avec la plus grande densité de population :**")
print(f"Pays: **{plus_grande_densite['Nom']}** (Densité: **{plus_grande_densite['Densite_hab_km2']:,} hab/km²**)")
print("\n**Les 5 pays les plus peuplés d'Europe :**")
print(top_5_popules[['Nom', 'Population']].to_markdown(index=False))

# --- 7. Sauvegarder les résultats dans pays_europe.xlsx ---
try:
    df_europe.to_excel(FILE_NAME, index=False)
    print(f"\n✅ Succès : Les résultats ont été sauvegardés dans le fichier **{FILE_NAME}**.")
except Exception as e:
    print(f"Erreur lors de la sauvegarde du fichier Excel : {e}")
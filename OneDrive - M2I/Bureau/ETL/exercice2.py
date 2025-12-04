import pandas as pd

#1
print("Lecture de la première feuille (par défaut)")
df = pd.read_excel('ventes_janvier.xlsx')
print(df)

#2
print("Suppression des doublons sur toutes les colonnes (drop_duplicates()) ---")
df = df.drop_duplicates()
print(df)

print("Remplacer les valeurs manquantes de 'region' par 'non spécifié' ---")
df['region'] = df['region'].fillna('non spécifié')
print(df['region'])

print("Conversion des types")
df['date'] = pd.to_datetime(df['date'])
print(df.dtypes)

# Sauvegarde des données nettoyées (fin de la partie 2)
df_nettoyees = df.copy()

#3 (analyse, mais PAS dans les outputs Excel)
print("Création de montant_total")
df['montant_total'] = df['prix_unitaire'] * df['quantite']

df['jour_semaine'] = df['date'].dt.dayofweek
df['jour'] = df['date'].dt.day

print("Écriture basique dans 'ventes_janvier.xlsx'")
df.to_excel('ventes_janvier.xlsx', index=False)

#4
print("Total des ventes par région")
ventes_par_region = df.groupby('region')['montant_total'].sum().sort_values(ascending=False)
print(ventes_par_region)

produits_quantites = df.groupby('produit')['quantite'].sum().sort_values(ascending=False)
print("Produit le plus vendu :", produits_quantites.idxmax())

ventes_par_jour_semaine = df.groupby('jour_semaine')['montant_total'].sum().sort_values(ascending=False)
print("Jour de la semaine avec le plus de ventes :", ventes_par_jour_semaine.idxmax())

#5 

par_region = df.groupby('region')['quantite'].sum().reset_index()
par_region = par_region.sort_values(by='quantite', ascending=False)

par_produit = df.groupby('produit')['quantite'].sum().reset_index()
par_produit = par_produit.sort_values(by='quantite', ascending=False)

with pd.ExcelWriter("ventes_analysées.xlsx", engine="openpyxl") as writer:
    df_nettoyees.to_excel(writer, sheet_name="Données nettoyées", index=False)
    par_region.to_excel(writer, sheet_name="Par région", index=False)
    par_produit.to_excel(writer, sheet_name="Par produit", index=False)

print("Fichier 'ventes_analysées.xlsx' créé avec succès !")

import csv
import pandas as pd


data = [
    ['date','produit','quantite','prix_unitaire','vendeur'],
['2024-01-15','Laptop',2,899.99,'Alice'],
['2024-01-15','Souris',5,29.99,'Bob'],
['2024-01-16','Clavier',3,79.99,'Alice'],
['2024-01-16','Laptop',1,899.99,'Charlie'],
['2024-01-17','Souris',10,29.99,'Alice']
]

with open('output.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)       # Création du writer
    writer.writerows(data) 


df = pd.read_csv("output.csv")

print("\n--- DataFrame de départ ---")
print(df)

print("\Ajout d'une colonne montant total")
df["montant_total"] = df["quantite"] * df["prix_unitaire"]
print(df)

df.to_csv('output.csv', index=False, encoding='utf-8')
print("\nLe fichier 'output.csv' a été mis à jour avec le montant total")

print("\n Total des ventes par vendeur")
par_produit = df.groupby("vendeur")["quantite"].sum()
print(par_produit)

print("\n Total des ventes par produit")
par_produit = df.groupby("produit")["quantite"].sum()
print(par_produit)

print("\n Top 3 des ventes")
top_3 = df.groupby("produit")["montant_total"].sum().nlargest(3)
print(top_3)





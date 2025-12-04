# ## TP 1 - Pipeline CSV vers Excel

# #**Objectif** : Créer un pipeline de traitement automatisé

# **Contexte** : Vous recevez quotidiennement des fichiers CSV de différentes sources (magasins) et devez les consolider dans un rapport Excel.

# **Fichiers d'entrée** : `magasin_A.csv`, `magasin_B.csv`, `magasin_C.csv`

# **Colonnes** : date, produit, quantite, prix_unitaire, vendeur

# **Pipeline à construire** :
# 1. Charger tous les fichiers CSV
# 2. Ajouter une colonne `magasin` (A, B ou C)
# 3. Concaténer tous les DataFrames
# 4. Nettoyer (doublons, valeurs manquantes)
# 5. Calculer `montant_total`
# # # 6. Créer un rapport Excel avec :
#    - Feuille "Consolidé" : Toutes les données
#    - Feuille "Par magasin" : Totaux par magasin
#    - Feuille "Par vendeur" : Performance des vendeurs
#    - Feuille "Top produits" : 10 produits les plus vendus"

import pandas as pd

# 1
fichiers = {
    "A": "magasin_A.csv",
    "B": "magasin_B.csv",
    "C": "magasin_C.csv"}

dfs = []

for code_magasin, fichier in fichiers.items():
    df = pd.read_csv(fichier)
    
# 2
    df["magasin"] = code_magasin
    dfs.append(df)

# 3

df_all = pd.concat(dfs)

# 4

df_all.drop_duplicates(inplace=True)
df_all.dropna(inplace=True)

# 5

df_all["montant_total"] = df_all["quantite"] * df_all["prix_unitaire"]

# 6
   # Totaux par magasin
df_magasin = (df_all.groupby("magasin")[["quantite", "montant_total"]].sum().reset_index())

   # Performance des vendeurs
df_vendeur = (df_all.groupby("vendeur")[["quantite", "montant_total"]].sum().reset_index())

   # Top 10 produits

df_produits_top = (
    df_all.groupby("produit")["quantite"].sum().reset_index().sort_values("quantite", ascending=False).head(10))


# 7

with pd.ExcelWriter("rapport_consolide.xlsx", engine="openpyxl") as writer:
    df_all.to_excel(writer, sheet_name="Consolidé", index=False)
    df_magasin.to_excel(writer, sheet_name="Par magasin", index=False)
    df_vendeur.to_excel(writer, sheet_name="Par vendeur", index=False)
    df_produits_top.to_excel(writer, sheet_name="Top produits", index=False)

print("Rapport généré : rapport_consolide.xlsx")

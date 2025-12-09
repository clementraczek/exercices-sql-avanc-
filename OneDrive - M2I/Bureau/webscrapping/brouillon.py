import requests
import time
import csv
from pathlib import Path

# --- Configuration ---
URL_BASE = "http://quotes.toscrape.com"
NOMBRE_PAGES = 3
CHEMIN_SORTIE = Path("scraper_output")
CHEMIN_SORTIE.mkdir(exist_ok=True)
FICHIER_RAPPORT = CHEMIN_SORTIE / "rapport_scraping.csv"

# --- 1. Fonction de Récupération avec Gestion d'Erreurs ---

def fetch_page(session, url, delay=1):
    """
    Récupère une page en utilisant une session.
    Applique un délai *avant* la requête pour des raisons de courtoisie.
    """
    time.sleep(delay) # Délai de courtoisie (Contrainte)
    
    result = {
        'URL': url,
        'Statut HTTP': 'N/A',
        'Taille en octets': 0,
        'Temps de réponse (s)': 0.0,
        'html_content': None
    }
    
    try:
        start_time = time.time()
        # Envoi de la requête
        reponse = session.get(url, timeout=10)
        temps_reponse = time.time() - start_time
        
        result['Temps de réponse (s)'] = round(temps_reponse, 3)
        result['Statut HTTP'] = reponse.status_code
        
        # Vérification du statut pour extraire le contenu
        if reponse.status_code == 200:
            # 3. Extraire le HTML brut & 4. Compter la taille en octets
            result['html_content'] = reponse.content  # .content est en bytes
            result['Taille en octets'] = len(reponse.content)
            print(f"   -> OK: Statut 200, Taille: {result['Taille en octets']} octets.")
        else:
            print(f"   -> ATTENTION: Échec de la requête, Statut {reponse.status_code}")

    # Gestion des erreurs réseau (connexion, DNS, timeout, etc.) (Contrainte)
    except requests.exceptions.RequestException as e:
        result['Statut HTTP'] = f"Exception ({type(e).__name__})"
        print(f"   -> ERREUR: {e}")
        
    return result

# --- Fonction Principale (Main) ---

def run_scraper():
    report_data = []
    
    # Utilisation d'une session (Contrainte)
    with requests.Session() as session:
        print("Scraping en cours...")
        
        # 2. Scraper les 3 premières pages
        for i in range(1, NOMBRE_PAGES + 1):
            url = f"{URL_BASE}/page/{i}/"
            print(f"\nTraitement de la page n°{i} : {url}")
            
            page_data = fetch_page(session, url, delay=1 if i > 1 else 0)
            
            # 6. Préparer les données pour le rapport CSV
            report_row = {k: page_data[k] for k in ['URL', 'Statut HTTP', 'Taille en octets', 'Temps de réponse (s)']}
            report_data.append(report_row)

            # 5. Sauvegarder chaque page dans un fichier HTML
            if page_data['html_content'] is not None:
                nom_fichier = CHEMIN_SORTIE / f"page_{i}.html"
                with open(nom_fichier, 'wb') as f: # 'wb' pour l'écriture binaire (bytes)
                    f.write(page_data['html_content'])
                print(f"   -> Fichier sauvegardé : {nom_fichier.name}")
            
        print("\nProcessus de récupération terminé.")

    # 6. Créer le rapport CSV final
    if report_data:
        fieldnames = ['URL', 'Statut HTTP', 'Taille en octets', 'Temps de réponse (s)']
        try:
            with open(FICHIER_RAPPORT, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
                writer.writeheader()
                writer.writerows(report_data)
            print(f"RAPPORT CSV généré : {FICHIER_RAPPORT.name}")
        except Exception as e:
            print(f"ÉCHEC de la génération du rapport CSV : {e}")


if __name__ == "__main__":
    run_scraper()
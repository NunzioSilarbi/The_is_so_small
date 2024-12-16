import requests
import pandas as pd
import os

# URL de l'API
API_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php"


def fetch_and_save_cards_data(csv_file="all_cards_data.csv"):
    """
    Récupère les données de l'API et les sauvegarde dans un fichier CSV.
    """
    try:
        # Envoyer une requête GET
        response = requests.get(API_URL)
        response.raise_for_status()  # Vérifie si la requête a réussi

        # Récupérer les données en format JSON
        data = response.json()

        # Extraire les informations des cartes
        all_cards = []
        for card in data["data"]:
            all_cards.append({
                "Nom": card.get("name", "N/A"),
                "Type général": card.get("type", "N/A"),
                "Type spécifique": card.get("race", "N/A"),
                "Attribut": card.get("attribute", "N/A"),
                "Niveau/Rank": card.get("level", card.get("linkval", "N/A")),
                "Attaque": card.get("atk", "N/A"),
                "Défense": card.get("def", "N/A"),
            })

        # Convertir en DataFrame et sauvegarder dans un fichier CSV
        df = pd.DataFrame(all_cards)
        df.to_csv(csv_file, index=False, encoding="utf-8")
        return df

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Erreur lors de la récupération des données : {e}")

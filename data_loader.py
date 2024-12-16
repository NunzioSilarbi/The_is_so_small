import requests
import pandas as pd
import os

API_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
CSV_FILE = "all_cards_data.csv"

def filter_card_types(card):
    """
    Filtre les cartes pour ne conserver que :
    - Monstres à effet
    - Monstres normaux
    - Magies
    - Pièges
    """
    valid_types = ["Effect Monster", "Normal Monster"]
    if card["type"] in valid_types:
        return True
    if "Spell" in card["type"]:
        return True
    if "Trap" in card["type"]:
        return True
    return False

def fetch_and_save_cards():
    """
    Récupère les données de l'API et les sauvegarde dans un fichier CSV.
    """
    print("Fetching cards from API...")
    response = requests.get(API_URL)
    response.raise_for_status()  # Lève une erreur si la requête échoue
    data = response.json()

    # Extraire uniquement les cartes pertinentes
    cards = data["data"]
    filtered_cards = [card for card in cards if filter_card_types(card)]

    # Préparer les données pour le CSV
    rows = []
    for card in filtered_cards:
        rows.append({
            "Nom": card.get("name", ""),
            "Type": card.get("type", ""),
            "Attribut": card.get("attribute", ""),
            "ATK": card.get("atk", ""),
            "DEF": card.get("def", ""),
            "Niveau": card.get("level", ""),
        })

    # Sauvegarder dans un DataFrame
    df = pd.DataFrame(rows)

    # Sauvegarder dans un fichier CSV
    df.to_csv(CSV_FILE, index=False, encoding="utf-8")
    print(f"Cards saved to {CSV_FILE}")

def load_cards_from_csv():
    """
    Charge les cartes depuis un fichier CSV. Si le fichier n'existe pas,
    les données sont récupérées depuis l'API.
    """
    if not os.path.exists(CSV_FILE):
        print(f"{CSV_FILE} not found. Fetching data from API...")
        fetch_and_save_cards()
    return pd.read_csv(CSV_FILE)

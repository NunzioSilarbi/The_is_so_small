import tkinter as tk
from tkinter import Scrollbar, Listbox, messagebox
from data_loader import load_cards_from_csv

# Tableau de 60 éléments (initialisé avec des valeurs vides)
tableau = []

def ajouter_au_tableau(carte):
    """
    Ajoute une carte au début du tableau Python (60 éléments max),
    en s'assurant qu'il n'y a pas plus de 3 exemplaires de la même carte.
    """
    global tableau
    if len(tableau) >= 60:
        messagebox.showinfo("Limite atteinte", "Vous avez déjà 60 cartes. Impossible d'ajouter d'autres cartes.")
        return
    # Vérifier si la carte est déjà présente 3 fois
    if tableau.count(carte) >= 3:
        print(f"La carte '{carte}' a déjà 3 exemplaires dans le tableau. Non ajoutée.")
        return

    # Ajouter la carte au début
    tableau.insert(0, carte)
    if len(tableau) > 60:
        tableau.pop()  # Supprimer le dernier élément si tableau > 60

    # Trier le tableau par ordre alphabétique
    tableau.sort()

    print(tableau)  # Affiche le tableau mis à jour dans la console

def retirer_du_tableau(carte):
    """
    Retire une carte du tableau.
    """
    global tableau
    if carte in tableau:
        tableau.remove(carte)
        print(f"La carte '{carte}' a été retirée du tableau.")
    else:
        print(f"La carte '{carte}' n'est pas dans le tableau.")

    # Trier le tableau par ordre alphabétique après retrait
    tableau.sort()

def create_fullscreen_window():
    """
    Crée une fenêtre Tkinter avec la liste des cartes à droite
    et l'affichage des éléments du tableau à gauche.
    """
    try:
        # Charger les données
        df = load_cards_from_csv()

        # Créer la fenêtre principale
        root = tk.Tk()
        root.title("Liste des Cartes Yu-Gi-Oh!")
        root.attributes("-fullscreen", True)  # Mettre en plein écran

        # Ajout d'un bouton pour quitter la fenêtre
        quit_button = tk.Button(root, text="Quitter", command=root.destroy, font=("Arial", 14))
        quit_button.pack(pady=10)

        # Cadre principal pour diviser la fenêtre en deux colonnes
        frame = tk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True)

        # Cadre de gauche pour afficher le tableau
        left_frame = tk.Frame(frame, bg="lightgray", width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        tableau_label = tk.Label(left_frame, text="Tableau (60 éléments) :", font=("Arial", 14), bg="lightgray")
        tableau_label.pack(pady=10)

        tableau_text = tk.Text(left_frame, font=("Arial", 12), width=40, height=30)
        tableau_text.pack(padx=10, pady=10)

        # Cadre de droite pour afficher la liste des cartes
        right_frame = tk.Frame(frame, bg="white", width=300)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        scrollbar = Scrollbar(right_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = Listbox(right_frame, yscrollcommand=scrollbar.set, font=("Arial", 12), width=50, height=30)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=listbox.yview)

        # Remplir la liste des cartes
        for card_name in df["Nom"]:
            listbox.insert(tk.END, card_name)

        # Fonction pour gérer la sélection d'une carte
        def on_select(event):
            # Récupérer la sélection
            selected_index = listbox.curselection()
            if selected_index:
                card_name = listbox.get(selected_index)
                ajouter_au_tableau(card_name)  # Ajouter la carte au tableau
                # Mettre à jour l'affichage du tableau
                tableau_text.delete("1.0", tk.END)
                tableau_text.insert(tk.END, "\n".join(tableau))

        # Fonction pour gérer un clic sur le tableau et retirer une carte
        def on_tableau_click(event):
            # Récupérer l'index du clic
            index = tableau_text.index(tk.CURRENT)
            line_number = int(index.split('.')[0]) - 1  # Extraire le numéro de ligne (les lignes commencent à 1)
            if line_number < len(tableau):
                carte = tableau[line_number]
                retirer_du_tableau(carte)  # Retirer la carte du tableau
                # Mettre à jour l'affichage du tableau
                tableau_text.delete("1.0", tk.END)
                tableau_text.insert(tk.END, "\n".join(tableau))

        # Associer la sélection à l'événement
        listbox.bind("<<ListboxSelect>>", on_select)

        # Associer le clic sur le tableau à la fonction de retrait
        tableau_text.bind("<Button-1>", on_tableau_click)

        # Lancer la boucle principale
        root.mainloop()

    except Exception as e:
        messagebox.showerror("Erreur", str(e))

if __name__ == "__main__":
    create_fullscreen_window()

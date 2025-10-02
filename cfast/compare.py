import pandas as pd

df_customers = pd.read_csv('customers.csv', sep=';')
df_cfast = pd.read_csv('liste_clients_cfast.csv', sep=';')

def normalize(text):
    if isinstance(text, str):
        return text.lower().replace(" ", "")
    return ""

liste_sewan = df_customers['Raison sociale'].dropna().tolist()
liste_cfast = df_cfast["Nom Client"].dropna().tolist()
liste_sewan_norm = [normalize(nom) for nom in liste_sewan]
liste_nom_cfast_norm = [normalize(nom) for nom in liste_cfast]

# Créer un DataFrame de correspondance
df_correspondance = pd.DataFrame({
    "Nom Sewan": liste_sewan,
    "Nom CFAST": [nom if normalize(nom) in liste_nom_cfast_norm else "" for nom in liste_sewan],
    "Nom Normalisé": liste_sewan_norm
})

# Filtrer les correspondances
correspondances = set(liste_sewan_norm) & set(liste_nom_cfast_norm)

# Retirer les correspondances des deux listes
liste_sewan_sans_corresp = [nom for nom, norm in zip(liste_sewan, liste_sewan_norm) if norm not in correspondances]
liste_cfast_sans_corresp = [nom for nom, norm in zip(liste_cfast, liste_nom_cfast_norm) if norm not in correspondances]

# print("DataFrame de correspondance :")
# print(df_correspondance.head())

# print("\nClients Sewan sans correspondance :", liste_sewan_sans_corresp)
# print("\nClients CFAST sans correspondance :", liste_cfast_sans_corresp)


df_correspondance.to_csv("correspondance_clients.csv", index=False)

max_len = max(len(liste_sewan_sans_corresp), len(liste_cfast_sans_corresp))
liste_sewan_sans_corresp += [""] * (max_len - len(liste_sewan_sans_corresp))
liste_cfast_sans_corresp += [""] * (max_len - len(liste_cfast_sans_corresp))

df_non_corresp = pd.DataFrame({
    "Sewan sans correspondance": liste_sewan_sans_corresp,
    "CFAST sans correspondance": liste_cfast_sans_corresp
})

df_non_corresp.to_csv("clients_non_correspondants.csv", index=False)

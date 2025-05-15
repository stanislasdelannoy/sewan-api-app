# Application de Facturation pour N'CO Services

### Mise en place de l'application

1. Arborescence

| Chemin                       | Rôle                                                                   |
| ---------------------------- | ---------------------------------------------------------------------- |
| `app.py`                     | Interface Streamlit, appelle les fonctions de `services` et `utils`.   |
| `requirements.txt`           | Dépendances : `streamlit`, `requests`, `pandas`, `openpyxl`, etc.      |
| `config/settings.py`         | Contient ton `API_KEY`, base URL, etc. (à exclure du git si sensible). |
| `services/sewan_api.py`      | Se charge de faire les appels à l'API Sewan, retourne des dict/list.   |
| `utils/exporter.py`          | Prend les données et les transforme en CSV/Excel.                      |
| `outputs/`                   | Emplacement où seront écrits les fichiers téléchargeables.             |
| `data/example_response.json` | (optionnel) Te permet de tester l'export sans taper l’API.             |



### Logique backend

1. **Récuperer le nom et l'ids des clients :**

On utilise la fonction *sophia.service.Billing.get_all_billing_information()*. On récupère toutes les infos sur les factures émises pour une période, et on en sort uniquement le nom et l'id des clients facturés.

2. **Récupérer le détail de la facture pour un client :**

On utilise la fonction *sophia.service.Billing.get_fixed_costs()*. On garde uniquement les factures récurentes et facturés.

3. **Boucler cette fonction pour tout les clients :**

4. **Nettoyer le dataframe et l'exporter en csv**



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


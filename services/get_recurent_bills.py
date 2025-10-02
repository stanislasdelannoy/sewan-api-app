import requests
import sys
import json
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# ############################
# Variables d'environnements
# ############################

API_URL = os.getenv("API_URL")
USER_AGENT = os.getenv("USER_AGENT")
TOKEN_API = os.getenv("TOKEN_API")
PERSON_ID = int(os.getenv("PERSON_ID", 0))

CUSTOMMER_ID = 902143
BILL_ID = 25013101
SEARCH_ID =2

headers = {
    'Authorization': f'bearer {TOKEN_API}',
    'User-Agent': USER_AGENT,
    'Accept-Language': 'fr_FR'
}

# ############################
# Check Date Format
# ############################

def validate_date(input_date):

    """
    Valide et formate une date saisie par l'utilisateur.
    Retourne la date au format 'YYYY-MM-DD' si elle est valide.
    """

    try:
        valid_date = datetime.strptime(input_date, "%Y-%m-%d")
        return valid_date.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError("Veuillez rentrer une date minimum. Vérifiez que la date utilise le format 'YYYY-MM-DD'.")

# ############################
# Get a dataframe of all customers name and ids
# ############################

def get_billing_informations(person_id, date):

    """
    Obtenir une liste de tous les clients facturables sur une période.
    Retourne un tableau de la forme : [{"id": 1, "client": "client1"}]
    """

    # Vérification de la date
    try:
        date = validate_date(date)
    except ValueError as e:
        print(e)
        return pd.DataFrame()

    print("Appel à (sophia.service.Billing.get_all_billing_information())... ")

    post_data = {
        "service": "sophia.service.Billing",
        "method": "get_all_billing_information",
        'reseller_id': person_id,
        "filter_date": date,
        'bill_type': 'REGULAR'
    }

    # Call API
    response = requests.post(
        url=API_URL, data=post_data, headers=headers, timeout=10
    )

    # Vérification de la répones
    if response.status_code != 200:
        sys.stderr.write(
            f"  => HTTP error {response.status_code} pour récupérer les infos\n"
        )
        sys.stderr.write(f"  => Body {response.content}\n")
        sys.exit(2)
    rjson = response.json()

    # print(f"  * Webservice response: {rjson}")

    # Explication en cas d'erreur
    code = int(rjson["code"])
    if code < 200 or code >= 300:
        # Search failed
        sys.stderr.write(
            f"  => Webservice failed with code {rjson['code']} : {rjson['msg']}\n"
            "(see Webservice response for more details)\n"
        )
        sys.exit(2)

    # Extraire les résultats
    first_results_array = rjson["result_object1"]
    if not first_results_array:
        print("No results found.")
        return pd.DataFrame()

    # Convert the results to a pandas DataFrame
    df = pd.DataFrame(first_results_array)
    print(f"  => DataFrame created with {len(df)} rows.")

    df = df[df['status_code'] == 204]
    print(f"  => Filtered DataFrame with {len(df)} rows where 'status_code' == 204.")
    #

    if 'payer_per_id' not in df.columns or 'payer_per_fullname' not in df.columns:
        raise ValueError("Les colonnes 'payer_per_id' et 'payer_per_fullname' sont manquantes dans le DataFrame.")

    payer_info = df[['payer_per_id', 'payer_per_fullname']].to_dict(orient='records')

    return payer_info


# ############################
# Get fixed costs for 1 customer
# ############################

def get_fixed_costs(custommer_id):

    """
    Obtenir la liste des coûts fixes pour les client donné dans une période donnée
    Retourne un tableau de chaque cout fixé pour chaque client
    """

    post_data = {
        "service": "sophia.service.Billing",
        "method": "get_fixed_costs",
        'per_id': custommer_id,
        'only_to_punctual_bill': 0,
        'get_punctual': False,
        'get_recurrent': True,
    }

    # Call API
    response = requests.post(
        url=API_URL, data=post_data, headers=headers, timeout=10
    )

    # Vérification de la réponse
    if response.status_code != 200:
        sys.stderr.write(
            f"  => HTTP error {response.status_code} "
            "on getting all persons\n"
        )
        sys.stderr.write(f"  => Body {response.content}\n")
        sys.exit(2)
    rjson = response.json()

    # Explication en cas d'erreur
    code = int(rjson["code"])
    if code < 200 or code >= 300:
        # Search failed
        sys.stderr.write(
            f"  => Webservice failed with code {rjson['code']} : {rjson['msg']}\n"
            "(see Webservice response for more details)\n"
        )
        sys.exit(2)

    # Extraire les résultats
    first_results_array = rjson["result_object2"]
    if not first_results_array:
        print("No results found.")
        return pd.DataFrame()

    return first_results_array


# ############################
# Get a dataframe of all fixed costs for a period
# ############################

def get_all_fixed_costs(person_id, min_date=''):

    """
    Obtenir la liste des coûts fixes pour les clients donnés dans une période donnée
    Retourne un dataframe de tout les couts fixes de tout les clients
    """

    all_fixed_costs = []

    # Obtenir les ids des clients facturables
    custommers = get_billing_informations(person_id, min_date)
    custommers_df = pd.DataFrame(custommers)


    # Extraire les IDs et les noms des clients
    custommers_ids = custommers_df['payer_per_id'].tolist()

    print("Appel au service (sophia.service.Billing.get_fixed_costs()) ...")
    for custommer_id in custommers_ids:
        fixed_costs_list = get_fixed_costs(custommer_id)

        fixed_costs_df = pd.DataFrame(fixed_costs_list)

        if not fixed_costs_df.empty:
            # Ajouter le nom de la société en utilisant une correspondance avec 'billed_person_id'
            fixed_costs_df['customer_name'] = fixed_costs_df['billed_person_id'].map(
                custommers_df.set_index('payer_per_id')['payer_per_fullname']
            )
            all_fixed_costs.append(fixed_costs_df)

    if all_fixed_costs:
        all_fixed_costs_df = pd.concat(all_fixed_costs, ignore_index=True)
        print(f"  => DataFrame created with {len(all_fixed_costs_df)} rows.")
        return all_fixed_costs_df
    else    :
        print("No fixed costs found for any customer.")
        return pd.DataFrame()

# ############################
# Clean the DataFrame and export
# ############################

def clean_df(df, min_date='', max_date=''):

    """
    Nettoie le DataFrame en supprimant les colonnes inutiles et en transformant la colonne 'family'.
    """

    # Colonnes à supprimer
    columns_to_drop = [
        'product_ref', 'creator_login', 'product_code', 'id', 'localized',
        'vat_category_name', 'priority', 'cost_total_vat', 'vat_rate_id',
        'cost_vat_included', 'vat_rate_name', 'sophia_class_name', 'family_name', 'locales',
        'family_id', 'vat_rate', 'order', 'date', 'punctual_bill_sbg_id',
    ]

    df = df.drop(columns=columns_to_drop, axis=1)

    # Combiner les colonnes 'family' et 'priority'
    df['family_combined'] = df['family'].apply(
        lambda x: f"{x.get('priority')} - {x.get('name')}" if isinstance(x, dict) else None
    )

    df = df.drop(columns=['family'], axis=1)

    if min_date and max_date:
        df = df[(df['creation_date'] >= min_date) & (df['creation_date'] < max_date)]

    # Preparer le nouvel ordre des colonnes
    new_order = ['family_combined', 'name', 'cost_unit', 'qtt', 'cost', 'description', 'creation_date', 'modification_date', 'billed_person_id', 'customer_name']
    df = df[new_order]

    # Forcer le retour d'un DataFrame
    if isinstance(df, pd.Series):
        df = df.to_frame()

    # Export csv
    df.to_csv('./fixed_costs.csv', index=False)

    return df

def main():
    """
    Point d'entrée principal pour tester le script.
    """
    print("=== Début des tests du script ===")

    person_id = PERSON_ID

    # Tester la récupération des coûts fixes
    print("\nTest : Récupération des coûts fixes")
    try:
        min_date = input("Entrez une date minimale (YYYY-MM-DD) : ")
        max_date = input("Entrez une date maximale (YYYY-MM-DD) ou laissez vide : ")
        all_fixed_costs = get_all_fixed_costs(person_id, min_date)

        if isinstance(all_fixed_costs, pd.DataFrame) and not all_fixed_costs.empty:
            print(f"Coûts fixes récupérés : {len(all_fixed_costs)} lignes.")

            # Exporter les coûts fixes en CSV
            clean_df(all_fixed_costs, min_date, max_date)
            print("Les coûts fixes ont été exportés dans 'fixed_costs.csv'.")
        else:
            print("Aucun coût fixe trouvé.")
    except Exception as e:
        print(f"Erreur lors de la récupération des coûts fixes : {e}")

    print("\n=== Fin des tests du script ===")



if __name__ == "__main__":
    main()

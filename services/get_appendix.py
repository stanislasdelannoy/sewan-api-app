import requests
import sys
import json
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from services.get_recurent_bills import validate_date
import os
import base64
import zipfile
import glob
import xml.etree.ElementTree as ET

load_dotenv()

API_URL = os.getenv("API_URL")
USER_AGENT = os.getenv("USER_AGENT")
TOKEN_API = os.getenv("TOKEN_API")
PERSON_ID = int(os.getenv("PERSON_ID", 0))

CUSTOMMER_ID = 902143
BILL_ID = 5715446
SEARCH_ID = 2

headers = {
    'Authorization': f'bearer {TOKEN_API}',
    'User-Agent': USER_AGENT,
    'Accept-Language': 'fr_FR'
}

def get_bill_appendix():
    """
    Récupère le PDF encodé en base64, le décode et le sauvegarde en fichier PDF.
    """
    print("Get bill PDF (sophia.service.Billing.get_bill_pdf())")

    post_data = {
        "service": "sophia.service.Billing",
        "method": "get_bill_appendix",
        "bill_id": BILL_ID
    }

    print(f"  * URL: {API_URL}")
    print(f"  * post parameters: {post_data}")

    response = requests.post(
        url=API_URL, data=post_data, headers=headers, timeout=10
    )

    if response.status_code != 200:
        sys.stderr.write(
            f"  => HTTP error {response.status_code} on getting bill appendix\n"
        )
        sys.stderr.write(f"  => Body {response.content}\n")
        sys.exit(2)
    rjson = response.json()

    code = int(rjson["code"])
    if code < 200 or code >= 300:
        sys.stderr.write(
            f"  => Webservice failed with code {rjson['code']} : {rjson['msg']}\n"
            "(see Webservice response for more details)\n"
        )
        sys.exit(2)

    # Récupère le zip encodé en base64
    zip_base64 = rjson["result_object1"]
    zip_filename = rjson.get("result_object2", "appendix.zip")
    zip_path = os.path.join(os.path.dirname(__file__), "..", zip_filename)
    zip_path = os.path.abspath(zip_path)

    # Décode et sauvegarde le zip
    with open(zip_path, "wb") as f:
        f.write(base64.b64decode(zip_base64))
    print(f"ZIP sauvegardé dans {zip_path}")

    # Dézippe le fichier dans un dossier du même nom (sans .zip)
    extract_dir = zip_path[:-4]
    os.makedirs(extract_dir, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    print(f"ZIP extrait dans {extract_dir}")

def concat_abonnements_csvs(folder_path=".."):
    """
    Cherche tous les CSV contenant 'abonnements' dans leur nom dans le dossier donné,
    les concatène et sauvegarde le résultat dans 'abonnements_concat.csv'.
    """
    # Recherche tous les fichiers CSV contenant 'abonnements' dans leur nom
    pattern = os.path.join(folder_path, "**", "*abonnements*.csv")
    csv_files = glob.glob(pattern, recursive=True)
    print(f"Fichiers trouvés : {csv_files}")

    if not csv_files:
        print("Aucun fichier CSV 'abonnements' trouvé.")
        return

    df_list = []
    for file in csv_files:
        try:
            # Essaye d'5644447abord en utf-8
            try:
                df = pd.read_csv(file, encoding="utf-8")
            except UnicodeDecodeError:
                # Si ça échoue, essaye en latin1
                df = pd.read_csv(file, encoding="latin1")
            df_list.append(df)
        except Exception as e:
            print(f"Erreur lors de la lecture de {file} : {e}")

    if not df_list:
        print("Aucun fichier CSV valide à concaténer.")
        return

    big_df = pd.concat(df_list, ignore_index=True)
    output_path = os.path.join(folder_path, "abonnements_concat.csv")
    big_df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"CSV concaténé sauvegardé dans {output_path}")

if __name__ == "__main__":
    get_bill_appendix()

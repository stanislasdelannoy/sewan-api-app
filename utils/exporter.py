from datetime import datetime
import pandas as pd

def _parse_date(date_str: str) -> datetime.date:
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def _ensure_df(obj) -> pd.DataFrame:
    if isinstance(obj, pd.DataFrame):
        return obj
    if isinstance(obj, list):
        return pd.DataFrame(obj)
    if isinstance(obj, dict):
        # supporte soit {"rows":[...]}, soit mapping colonnes->listes
        if "rows" in obj and isinstance(obj["rows"], list):
            return pd.DataFrame(obj["rows"])
        return pd.DataFrame(obj)
    return pd.DataFrame()

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path
from services.get_recurrent_bills import build_fixed_costs_df
import pandas as pd
import os

# ENVS
API_URL = os.getenv("API_URL")
USER_AGENT = os.getenv("USER_AGENT")
TOKEN_API = os.getenv("TOKEN_API")
PERSON_ID = int(os.getenv("PERSON_ID", 0))

#UTILS

app = FastAPI(title = "Sewan Bills")

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

def _check_date(s):
    try:
        datetime.strptime(s, '%Y-%m-%d')
    except Exception:
        raise HTTPException(status_code=400, detail="Format attendu: YYYY-MM-DD")

@app.get("/api/recurrent-bill")
def api_recurrent_bill(date_min, date_max: str | None = None):

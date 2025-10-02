from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
from pathlib import Path
import services.get_recurent_bills
import pandas as pd
import os

API_URL = os.getenv("API_URL")
USER_AGENT = os.getenv("USER_AGENT")
TOKEN_API = os.getenv("TOKEN_API")
PERSON_ID = int(os.getenv("PERSON_ID", 0))

def get_recurrent_bill(date_min, date_max):
    return 'cool'

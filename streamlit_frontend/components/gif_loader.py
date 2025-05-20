import os
import random

def get_random_gif(directory="./streamlit_frontend/gifs"):
    try:
        gif_files = [f for f in os.listdir(directory) if f.endswith(".gif")]
        if not gif_files:
            return None
        return os.path.join(directory, random.choice(gif_files))
    except Exception as e:
        return None

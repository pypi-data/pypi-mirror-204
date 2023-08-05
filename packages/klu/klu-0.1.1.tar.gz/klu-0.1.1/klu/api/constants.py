import os

ENV = os.getenv("KLU_ENV", "prod")
API_KEY = os.getenv("KLU_API_KEY")
API_ENDPOINT = (
    "http://localhost:4000/api" if ENV == "dev" else "https://engine.klu.ai/api"
)

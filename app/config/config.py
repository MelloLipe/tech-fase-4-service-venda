import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME: str = "Revenda Veiculos - Servico de Vendas"
    VERSION: str = "1.0.0"

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sales_service.db")
    MAIN_SERVICE_URL: str = os.getenv("MAIN_SERVICE_URL", "http://localhost:8000")


settings = Settings()

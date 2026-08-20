import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./servicehub.db")
JWT_SECRET = os.getenv("JWT_SECRET", "local-demo-secret-change-me")
QA_BUG_MODE = os.getenv("QA_BUG_MODE", "false").lower() == "true"
ACCESS_TOKEN_MINUTES = 60

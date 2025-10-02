from config.env import env

CORS_ALLOWED_ORIGINS = env.list(
    "DJANGO_CORS_ALLOWED_ORIGINS", default=["http://localhost", "http://127.0.0.1"]
)

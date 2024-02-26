import dotenv
import os

DEV_ENV_PATH: str = os.path.join(os.getcwd(), ".env.dev")
PROD_ENV_PATH: str = os.path.join(os.getcwd(), ".env.prod")


def load_env() -> None:
    dotenv.load_dotenv()
    environment: str = os.getenv("ENVIRONMENT")

    match environment:
        case "dev":
            dotenv.load_dotenv(DEV_ENV_PATH)
        case "prod":
            dotenv.load_dotenv(PROD_ENV_PATH)

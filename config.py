import os
from typing import Union
from dotenv import load_dotenv


class ProductionConfig:
    """Production config"""

    def __init__(self):

        raise Exception("It's necessary set environment production params")


class DevelopmentConfig:
    """Developer config"""

    def __init__(self):

        super().__init__()

        load_dotenv(dotenv_path=".env")

        self.api_version = os.getenv("API_VERSION")
        self.api_key = os.getenv("API_KEY")
        self.port_api = os.getenv("PORT_API")
        self.host_api = os.getenv("HOST_API")
        self.bucketpath = os.getenv("FILEPATH")


def get_config() -> Union[DevelopmentConfig, ProductionConfig]:
    """Get config setup"""

    setup = {
        "DEVELOPMENT": DevelopmentConfig, 
        "PRODUCTION": ProductionConfig
    }

    environment = os.environ.get("ENVIRONMENT", "DEVELOPMENT").upper()

    print(f"\nEnvironment: {environment}\n\n")

    if not environment:
        raise Exception("Environment variable environment is not populated")

    class_config = setup.get(environment)

    if not class_config:
        raise Exception(
            f"Unexpected value of environment variable environment: {environment}"
        )

    return class_config()


config = get_config()

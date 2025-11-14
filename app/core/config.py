import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # PostgreSQL configuration
    postgres_host: str = os.getenv("POSTGRES_HOST")
    postgres_port: int = os.getenv("POSTGRES_PORT")
    postgres_user: str = os.getenv("POSTGRES_USER")
    postgres_password: str = os.getenv("POSTGRES_PASSWORD")
    postgres_db: str = os.getenv("POSTGRES_DB")

    # MongoDB configuration
    mongodb_host: str = os.getenv("MONGODB_HOST")
    mongodb_port: int = os.getenv("MONGODB_PORT")
    mongodb_db: str = os.getenv("MONGODB_DB")
    mongodb_username: str = os.getenv("MONGODB_USERNAME")
    mongodb_password: str = os.getenv("MONGODB_PASSWORD")
    # MongoDB Atlas configuration
    mongodb_atlas_connection_string: str = os.getenv("MONGODB_ATLAS_CONNECTION_STRING")

    # JWT Configuration
    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM")
    access_token_expire_minutes: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

    @property
    def postgres_url(self) -> str:
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def mongodb_url(self) -> str:
        # If Atlas connection string is provided, use it
        if self.mongodb_atlas_connection_string:
            return self.mongodb_atlas_connection_string

        # Otherwise, use local MongoDB configuration
        if self.mongodb_username and self.mongodb_password:
            return f"mongodb://{self.mongodb_username}:{self.mongodb_password}@{self.mongodb_host}:{self.mongodb_port}/{self.mongodb_db}"
        return f"mongodb://{self.mongodb_host}:{self.mongodb_port}/{self.mongodb_db}"

    model_config = {"env_file": ".env"}


settings = Settings()

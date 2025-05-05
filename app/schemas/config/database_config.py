from pydantic import BaseModel, PostgresDsn


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    username: str
    password: str
    name: str
    host: str
    port: int

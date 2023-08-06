from pydantic import BaseSettings, SecretStr, ByteSize, BaseModel


class StoreSettings(BaseModel):
    auto_start: bool = False

    db_path: str = './db'
    mem_budget: ByteSize = '2 GiB'
    write_port: int = 5555
    write_workers: int = 8
    max_snapshots: int = 24
    snapshot_freq: float = 3600 # every hour by default
    


class Settings(BaseSettings):
    debug: bool = False
    session_secret: SecretStr

    store: StoreSettings

    class Config:
        env_prefix = 'SHAPELETS_'
        case_sensitive = False
        env_nested_delimiter = '__'
        env_file = '.env'
        env_file_encoding = 'utf-8'

from pydantic import BaseSettings


class Settings(BaseSettings):

    NAME: str = "governance"
    NETWORK_NAME: str = "mainnet"

    # Ports
    PORT: int = 8000
    HEALTH_PORT: int = 8180
    METRICS_PORT: int = 9400

    METRICS_ADDRESS: str = "localhost"

    # Prefix
    REST_PREFIX: str = "/api/v1"
    HEALTH_PREFIX: str = "/heath"
    METRICS_PREFIX: str = "/metrics"
    DOCS_PREFIX: str = "/api/v1/governance/docs"

    # Monitoring
    HEALTH_POLLING_INTERVAL: int = 60

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_TO_FILE: str = "false"
    LOG_FILE_NAME: str = "governance.log"
    LOG_FORMAT: str = "string"

    # ICON Nodes
    ICON_NODE_URL = "https://api.icon.geometry.io/api/v3"
    BACKUP_ICON_NODE_URL = "https://ctz.solidwallet.io/api/v3"

    # ICON Peers - Used to discover nodes across the network
    PEER_SEED_IP: str = "52.196.159.184"
    PEER_SEED_ADDRESS: str = "hx9c63f73d3c564a54d0eed84f90718b1ebed16f09"

    CRON_SLEEP_SEC: int = 600

    class Config:
        case_sensitive = True


settings = Settings()

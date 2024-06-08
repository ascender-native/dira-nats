from pydantic import Field
from pydantic_settings import BaseSettings

class NatsConfig(BaseSettings):
    url: str|None = Field(alias='nats_url', default=None)
    host: str = Field(alias='nats_host', default='127.0.0.1')
    port: str = Field(alias='nats_port', default='4222')
    
    def __init__(self, **values):
        super().__init__(**values)
        if self.url is None:
            self.url = f"nats://{self.host}:{self.port}"

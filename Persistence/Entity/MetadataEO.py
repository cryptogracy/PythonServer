
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
import Persistence.Alchemy.AlchemyConfig as AlchemyConfig


class MetadataEO(AlchemyConfig.Base):

    __tablename__ = "Metadata"

    sha_hash = Column(String, primary_key=True)
    timestamp = Column(DateTime)
    lifespan = Column(Integer)

    def __init__(self, sha_hash, timestamp, lifespan):
        self.sha_hash = sha_hash
        self.timestamp = timestamp
        self.lifespan = lifespan

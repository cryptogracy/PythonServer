from Persistence.Entity.MetadataEO import *
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
import Persistence.Alchemy.AlchemyConfig as AlchemyConfig


class MetadataPersistenceService:

    def __init__(self):
        self.session = AlchemyConfig.Session()

    def load(self, sha_hash):
        try:
            return self.session.query(MetadataEO).filter_by(sha_hash = sha_hash).one()
        except NoResultFound:
            raise FileNotFoundError("No file was found for provided hash.")


    def save(self, metadata):
        try:
            self.session.add(metadata)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise FileExistsError("File with provided hash already exists.")
        except Exception:
            self.session.rollback()
            raise


    def save_values(self, sha_hash, timestamp, lifespan):
        metadata = MetadataEO(sha_hash, timestamp, lifespan)
        self.save(metadata)

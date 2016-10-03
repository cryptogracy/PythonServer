from Persistence.Entity.MetadataEO import *
import time


class MetadataPersistenceService:

    def load(self, sha_hash):
        if sha_hash == "test_hash":
            result = MetadataEO(sha_hash, time.time(), 1000000)
        elif sha_hash == "test_hash_expired":
            result = MetadataEO(sha_hash, time.time()-100, 50)
        else:
            raise FileNotFoundError("File for the provided hash not found.")
        return result

    def save(self, metadata):
        pass

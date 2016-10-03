
import time


class ApiService:

    def __init__(self, file_service, metadata_service):
        self.file_service = file_service
        self.metadata_service = metadata_service

    def load_file(self, sha_hash):
        metadata = self.metadata_service.load(sha_hash)
        if metadata.timestamp + metadata.lifespan < time.time():
            raise FileExpiredError("The requested file is expired.")
        file = self.file_service.load(sha_hash)
        return metadata, file

    def save_file(self, file, sha_hash, lifespan):
        pass


class FileExpiredError(Exception):

    def __init__(self, args):
        self.args = args

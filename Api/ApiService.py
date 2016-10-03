
import datetime


class ApiService:

    def __init__(self, file_service, metadata_service):
        self.file_service = file_service
        self.metadata_service = metadata_service

    def load_file(self, sha_hash):
        metadata = self.metadata_service.load(sha_hash)
        if metadata.timestamp + datetime.timedelta(minutes=metadata.lifespan) < datetime.datetime.now():
            raise FileExpiredError("The requested file is expired.")
        file_content = self.file_service.load(sha_hash)
        return metadata, file_content

    def save_file(self, sha_hash, file_content, lifespan):
        # TODO: test whether hash fits to file
        now = datetime.datetime.now()
        self.metadata_service.save_values(sha_hash, now, lifespan)
        try:
            self.file_service.save(sha_hash, file_content)
        except:
            self.metadata_service.delete_by_hash(sha_hash)
            raise


class FileExpiredError(Exception):

    def __init__(self, args):
        self.args = args

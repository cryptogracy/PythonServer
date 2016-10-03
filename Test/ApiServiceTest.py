
import unittest
from Api.ApiService import *
from Persistence.Services.MetadataPersistenceService import *
from Persistence.Services.FilePersistenceService import *


class ApiServiceTest(unittest.TestCase):

    def setUp(self):
        AlchemyConfig.create_schema()
        self.metadata_service = MetadataPersistenceService()
        self.file_service = FilePersistenceService()
        self.service = ApiService(self.file_service, self.metadata_service)
        self.set_up_test_data()

    def set_up_test_data(self):
        now = datetime.datetime.now()
        try:
            self.metadata_service.save_values("test_hash", now, 100)
        except FileExistsError:
            pass
        try:
            self.metadata_service.save_values("test_hash_expired", now - datetime.timedelta(minutes=10), 5)
        except FileExistsError:
            pass

        self.file_service.save("test_hash", "some test content")
        self.file_service.save("test_hash_expired", "some more test content")

    def tearDown(self):
        test_hashes = ["test_hash", "test_hash_expired", "test_hash_for_save"]
        for test_hash in test_hashes:
            try:
                self.metadata_service.delete(test_hash)
            except FileNotFoundError:
                pass
            try:
                self.file_service.delete(test_hash)
            except FileNotFoundError:
                pass

    def test_load_file(self):
        metadata, file_content = self.service.load_file("test_hash")
        assert metadata.sha_hash == "test_hash"
        assert metadata.timestamp is not None
        assert metadata.lifespan == 100
        assert file_content == "some test content"

    def test_load_expired_file(self):
        self.assertRaises(FileExpiredError, lambda: self.service.load_file("test_hash_expired"))

    def test_load_not_existing_file(self):
        self.assertRaises(FileNotFoundError, lambda: self.service.load_file("test_hash_not_existing"))

    def test_save_file(self):
        self.service.save_file("test_hash_for_save", "test content for save", 200)
        metadata, file_content = self.service.load_file("test_hash_for_save")
        assert metadata.sha_hash == "test_hash_for_save"
        assert metadata.timestamp is not None
        assert metadata.lifespan == 200
        assert file_content == "test content for save"


if __name__ == "__main__":
    unittest.main()

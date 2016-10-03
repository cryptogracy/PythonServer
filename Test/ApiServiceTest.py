
import unittest
from Api.ApiService import *
from Persistence.Services.MetadataPersistenceService import *
from Persistence.Services.Test.FilePersistenceTestService import *


class ApiServiceTest(unittest.TestCase):

    def setUp(self):
        AlchemyConfig.create_schema()
        self.metadata_service = MetadataPersistenceService()
        self.file_service = FilePersistenceService()
        self.service = ApiService(self.file_service, self.metadata_service)
        self.set_up_test_database()

    def set_up_test_database(self):
        try:
            self.metadata_service.save_values("test_hash", time.time(), 1000000)
        except FileExistsError:
            pass
        try:
            self.metadata_service.save_values("test_hash_expired", time.time() - 100, 50)
        except FileExistsError:
            pass

    def tearDown(self):
        pass

    def test_load_file(self):
        metadata, file = self.service.load_file("test_hash")
        assert metadata.sha_hash == "test_hash"
        assert metadata.timestamp is not None
        assert metadata.lifespan == 1000000
        assert file == "test"

    def test_load_expired_file(self):
        self.assertRaises(FileExpiredError, lambda: self.service.load_file("test_hash_expired"))

    def test_load_not_existing_file(self):
        self.assertRaises(FileNotFoundError, lambda: self.service.load_file("test_hash_not_existing"))

    def test_save_file(self):
        pass



if __name__ == "__main__":
    unittest.main()

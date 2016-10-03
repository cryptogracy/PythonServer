import os


class FilePersistenceService:

    def load(self, file_name):
        fo = open(file_name, "r")
        content = fo.read()
        fo.close()
        return content

    def save(self, file_name, file_content):
        fo = open(file_name, "w")
        fo.write(file_content)
        fo.close()

    def delete(self, file_name):
        os.remove(file_name)

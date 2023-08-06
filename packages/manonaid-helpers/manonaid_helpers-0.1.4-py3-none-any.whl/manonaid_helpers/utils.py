from azure.storage.blob import BlobServiceClient
from manonaid_helpers.core import Base


class Utils(Base):
    def __init__(
        self,
        container,
        name_starts_with=None,
    ):
        super(Utils, self).__init__(
            folder=name_starts_with,
        )
        self.container = container
        self.name_starts_with = name_starts_with
        self.connection_string = self._check_connection_credentials()[0]
        self._blob_service_client = BlobServiceClient.from_connection_string(
            self.connection_string
        )
        self._container_client = self._blob_service_client.get_container_client(
            self.container
        )

    ###################
    # private methods #
    ###################

    def _get_files(self):
        files = self._container_client.list_blobs(
            name_starts_with=self.name_starts_with
        )
        return files

    @staticmethod
    def _get_file_names_simple(files):
        return [file.get("name") for file in files]

    def _list_blobs_not_extended(self, files):
        file_names = self._get_file_names_simple(files)
        return file_names

    ##################
    # public methods #
    ##################

    def list_blobs(self):
        files = self._get_files()
        return self._list_blobs_not_extended(files)

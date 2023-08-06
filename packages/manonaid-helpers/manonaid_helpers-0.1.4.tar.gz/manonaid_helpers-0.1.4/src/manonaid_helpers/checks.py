import os
import re


class Checks:
    def __init__(self, directory):
        self.directory = directory

    @staticmethod
    def _create_connection_string():
        """
        When AZURE_STORAGE_ACCOUNT and AZURE_STORAGE_KEY are given,
        create an AZURE_STORAGE_CONNECTION_STRING

        Returns
        -------
        connection_string
        """
        base_string = (
            "DefaultEndpointsProtocol=https;AccountName={account_name};"
            "AccountKey={account_key};"
            "EndpointSuffix=core.windows.net"
        )
        connection_string = base_string.format(
            account_name=os.environ.get("AZURE_STORAGE_ACCOUNT", None),
            account_key=os.environ.get("AZURE_STORAGE_KEY", None),
        )

        return connection_string

    def _check_connection_credentials(self):
        """
        If connection string is given as env variable return it,
        else the connection string is generated from storage key and name.

        If none of the above are given, raise.

        Returns
        -------
        AZURE_STORAGE_CONNECTION_STRING
        """
        connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING", None)
        account_name = os.environ.get("AZURE_STORAGE_ACCOUNT", None)
        account_key = os.environ.get("AZURE_STORAGE_KEY", None)

        if connection_string:
            account_name, account_key = self._parse_connection_string(connection_string)
            return (
                os.environ.get("AZURE_STORAGE_CONNECTION_STRING"),
                account_name,
                account_key,
            )
        elif all([account_name, account_key]):
            return self._create_connection_string(), account_name, account_key
        else:
            # check for env variables else raise
            raise ValueError(
                "If AZURE_STORAGE_CONNECTION_STRING is not set as env variable"
                " AZURE_STORAGE_KEY and AZURE_STORAGE_ACCOUNT have to be set."
            )

    @staticmethod
    def _parse_connection_string(connection_string):
        account_name = re.search(r"AccountName=(.*?);", connection_string).group(1)
        account_key = re.search(r"AccountKey=(.*?);", connection_string).group(1)

        return account_name, account_key

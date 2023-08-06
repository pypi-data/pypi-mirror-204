from manonaid_helpers.checks import Checks


class Base(Checks):
    def __init__(
        self,
        folder,
        extension=None,
        list_files=None,
    ):
        super().__init__(directory=folder)

        self.folder = folder
        self.extension = extension
        self.list_files = list_files
        credentials = self._check_connection_credentials()
        self.connection_string = credentials[0]
        self.account_name = credentials[1]
        self.account_key = credentials[2]

    def checks(self):
        if self.list_files and not isinstance(self.list_files, list):
            raise ValueError(
                (
                    "Argument list_files was set, but is not of type list,"
                    f" but type {type(self.list_files)}"
                )
            )

    @staticmethod
    def create_not_case_sensitive_extension(extension):
        """
        We create in-case sensitive fnmatch
        .pdf -> .[Pp][Dd][Ff]
        .csv -> .[Cc][Ss][Vv]
        """
        new_extension = ""
        for letter in extension:
            if not letter.isalpha():
                new_extension += letter
            else:
                new_extension += f"[{letter.upper()}{letter}]"

        if not new_extension.startswith("*"):
            new_extension = "*" + new_extension

        return new_extension

    def define_pattern(self):
        self.extension = self.create_not_case_sensitive_extension(self.extension)
        if self.folder and not self.extension:
            if self.folder.endswith("/"):
                pattern = self.folder + "*"
            else:
                pattern = self.folder + "/*"
        elif self.folder and self.extension:
            pattern = self.folder.rstrip("/") + "/" + "*" + self.extension
        elif not self.folder and self.extension:
            pattern = "*" + self.extension
        else:
            pattern = None

        return pattern

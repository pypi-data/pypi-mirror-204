import os
from io import BytesIO
import pandas as pd

from azure.storage.blob import BlobServiceClient

from manonaid_helpers.core import Base


class Download(Base):
    def __init__(
        self,
        source,
        folder=None,
        extension=None,
        list_files=None,
        type_correct_date_time_cols=False,
        delimitter=",",
    ):
        super(Download, self).__init__(
            folder=folder,
            extension=extension,
            list_files=list_files,
        )
        self.checks()
        self.source = source
        self.type_correct_date_time_cols = type_correct_date_time_cols
        self.delimitter = delimitter

    def returnAsDataFrameDict(self):
        blob_service_client = BlobServiceClient.from_connection_string(
            self.connection_string
        )
        container_client = blob_service_client.get_container_client(
            container=self.source
        )
        blob_list = container_client.list_blobs(name_starts_with=self.folder)
        bs_dict = {}
        empty_frames_list = []
        for blob in blob_list:
            if self.extension and not blob.name.lower().endswith(
                self.extension.lower()
            ):
                continue

            file_path, file_name = os.path.split(blob.name)

            if self.list_files and file_name not in self.list_files:
                continue
            blob_client = container_client.get_blob_client(blob=blob.name)
            try:
                blob_as_data_frame = pd.read_csv(
                    BytesIO(blob_client.download_blob().readall()),
                    sep=self.delimitter,
                    engine="python",
                )
                if self.type_correct_date_time_cols:
                    date_col_names = blob_as_data_frame.columns[
                        blob_as_data_frame.columns.str.lower().str.contains(pat="date")
                    ]
                    time_col_names = blob_as_data_frame.columns[
                        blob_as_data_frame.columns.str.lower().str.contains(pat="time")
                    ]
                    blob_as_data_frame[
                        date_col_names.union(time_col_names)
                    ] = blob_as_data_frame[date_col_names.union(time_col_names)].apply(
                        pd.to_datetime, format="%Y-%m-%dT%H:%M:%S", axis=1
                    )
                bs_dict[file_name] = blob_as_data_frame
            except pd.errors.EmptyDataError:
                print(file_path + "/" + file_name + " is EMPTY!!")
                empty_frames_list.append(file_name)

        bs_dict["empty_frames_list"] = empty_frames_list
        return bs_dict

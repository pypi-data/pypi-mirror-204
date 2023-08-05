# Copyright (C) 2021 Bosutech XXI S.L.
#
# nucliadb is offered under the AGPL v3.0 and as commercial software.
# For commercial licensing, contact us at info@nuclia.com.
#
# AGPL:
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from dataclasses import dataclass
from typing import Optional

from nucliadb.writer.settings import settings as writer_settings
from nucliadb.writer.tus.dm import FileDataMangaer, RedisFileDataManager
from nucliadb.writer.tus.exceptions import ManagerNotAvailable
from nucliadb.writer.tus.gcs import GCloudBlobStore, GCloudFileStorageManager
from nucliadb.writer.tus.local import LocalBlobStore, LocalFileStorageManager
from nucliadb.writer.tus.s3 import S3BlobStore, S3FileStorageManager
from nucliadb.writer.tus.storage import BlobStore, FileStorageManager
from nucliadb_utils.settings import storage_settings

TUSUPLOAD = "tusupload"
UPLOAD = "upload"


@dataclass
class TusStorageDriver:
    backend: BlobStore
    manager: FileStorageManager


DRIVER: Optional[TusStorageDriver] = None
FDM: Optional[FileDataMangaer] = None


async def initialize():
    global DRIVER

    if storage_settings.file_backend == "gcs":
        storage_backend = GCloudBlobStore()

        await storage_backend.initialize(
            json_credentials=storage_settings.gcs_base64_creds,
            bucket=storage_settings.gcs_bucket,
            location=storage_settings.gcs_location,
            project=storage_settings.gcs_project,
            bucket_labels=storage_settings.gcs_bucket_labels,
            object_base_url=storage_settings.gcs_endpoint_url,
        )

        storage_manager = GCloudFileStorageManager(storage_backend)

        DRIVER = TusStorageDriver(backend=storage_backend, manager=storage_manager)

    if storage_settings.file_backend == "s3":
        storage_backend = S3BlobStore()

        await storage_backend.initialize(
            client_id=storage_settings.s3_client_id,
            client_secret=storage_settings.s3_client_secret,
            ssl=storage_settings.s3_ssl,
            verify_ssl=storage_settings.s3_verify_ssl,
            max_pool_connections=storage_settings.s3_max_pool_connections,
            endpoint_url=storage_settings.s3_endpoint,
            region_name=storage_settings.s3_region_name,
            bucket=storage_settings.s3_bucket,
        )

        storage_manager = S3FileStorageManager(storage_backend)

        DRIVER = TusStorageDriver(backend=storage_backend, manager=storage_manager)

    if storage_settings.file_backend == "local":
        storage_backend = LocalBlobStore(storage_settings.local_files)

        await storage_backend.initialize()

        storage_manager = LocalFileStorageManager(storage_backend)

        DRIVER = TusStorageDriver(backend=storage_backend, manager=storage_manager)


async def finalize():
    global DRIVER
    global FDM

    if DRIVER is not None:
        await DRIVER.backend.finalize()
        DRIVER = None

    if FDM is not None:
        await FDM.finalize()
        FDM = None


def get_dm() -> FileDataMangaer:  # type: ignore
    global FDM
    if FDM is None:
        if writer_settings.dm_enabled:
            FDM = RedisFileDataManager(
                f"redis://{writer_settings.dm_redis_host}:{writer_settings.dm_redis_port}"
            )
        else:
            FDM = FileDataMangaer()

    return FDM


def get_storage_manager() -> FileStorageManager:
    global DRIVER

    if DRIVER is None:
        raise ManagerNotAvailable()
    return DRIVER.manager


def clear_storage():
    global DRIVER
    global FDM

    DRIVER = None
    FDM = None

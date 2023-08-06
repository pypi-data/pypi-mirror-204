import os
import posixpath
import signal
import sys
import typing
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import active_children

from mlflow.entities import FileInfo, SignedURL
from mlflow.store.artifact.artifact_repo import ArtifactRepository
from mlflow.tracking import MlflowClient
from mlflow.utils.file_utils import (
    download_file_using_http_uri,
    relative_path_to_artifact_path,
)
from mlflow.utils.rest_utils import cloud_storage_http_request

from mlfoundry.exceptions import MlFoundryException
from mlfoundry.tracking.entities import ArtifactCredential
from mlfoundry.tracking.truefoundry_rest_store import TruefoundryRestStore


def sigterm_handler(sig, frame):
    print("Handling SIGTERM...")
    try:
        active = active_children()
        # terminate all active children
        for child in active:
            child.terminate()
    finally:
        # terminate the process
        sys.exit(0)


def sighup_handler(sig, frame):
    print("Handling SIGHUP...")
    try:
        active = active_children()
        # terminate all active children
        for child in active:
            child.terminate()
    finally:
        # terminate the process
        sys.exit(0)


class TruefoundryArtifactRepository(ArtifactRepository):
    def __init__(
        self,
        artifact_uri,
        rest_store: TruefoundryRestStore,
        credentials=None,
        storage_integration_id=None,
    ):
        self.artifact_uri = artifact_uri
        super().__init__(artifact_uri)

        self.rest_store: TruefoundryRestStore = rest_store

    @staticmethod
    def _extract_run_id(artifact_uri) -> str:
        # artifact_uri will be something like,
        # s3://<BUCKET>/<PATH>/<EXP_ID>/<RUN_ID>/artifacts
        run_id = artifact_uri.rstrip("/").split("/")[-2]
        return run_id

    def list_artifacts(self, path=None) -> typing.List[FileInfo]:
        run_id = self._extract_run_id(self.artifact_uri)
        artifacts = self.rest_store.list_artifacts(run_id=run_id, path=path)
        return artifacts

    def _signed_uri_upload_file(
        self, artifact_credential: ArtifactCredential, local_file: str
    ):
        if os.stat(local_file).st_size == 0:
            with cloud_storage_http_request(
                "put",
                artifact_credential.signed_uri,
                data="",
            ) as response:
                response.raise_for_status()
        else:
            with open(local_file, "rb") as file:
                with cloud_storage_http_request(
                    "put",
                    artifact_credential.signed_uri,
                    data=file,
                ) as response:
                    response.raise_for_status()

    def log_artifacts(self, local_dir, artifact_path=None):
        dest_path = artifact_path or ""
        dest_path = dest_path.lstrip(posixpath.sep)
        for (root, _, file_names) in os.walk(local_dir):
            upload_path = dest_path
            if root != local_dir:
                rel_path = os.path.relpath(root, local_dir)
                rel_path = relative_path_to_artifact_path(rel_path)
                upload_path = posixpath.join(dest_path, rel_path)
            for file_name in file_names:
                local_file = os.path.join(root, file_name)
                self.log_artifact(local_file=local_file, artifact_path=upload_path)

    def log_artifact(self, local_file, artifact_path=None):
        dest_path = artifact_path or ""
        dest_path = dest_path.lstrip(posixpath.sep)
        dest_path = posixpath.join(dest_path, os.path.basename(local_file))
        artifact_credential = self.rest_store.get_artifact_write_credential(
            run_id=self._extract_run_id(self.artifact_uri), path=dest_path
        )
        self._signed_uri_upload_file(artifact_credential, local_file)

    def _download_file(self, remote_file_path: str, local_path: str):
        if not remote_file_path:
            raise MlFoundryException(
                f"remote_file_path cannot be None or empty str {remote_file_path}"
            )

        artifact_credential = self.rest_store.get_artifact_read_credentials(
            run_id=self._extract_run_id(self.artifact_uri), path=remote_file_path
        )
        download_file_using_http_uri(
            http_uri=artifact_credential.signed_uri, download_path=local_path
        )


def _signed_uri_upload_file(signed_url: SignedURL, local_file: str):
    if os.stat(local_file).st_size == 0:
        with cloud_storage_http_request("put", signed_url.url, data="") as response:
            response.raise_for_status()
    else:
        with open(local_file, "rb") as file:
            with cloud_storage_http_request(
                "put", signed_url.url, data=file
            ) as response:
                response.raise_for_status()


class MlFoundryArtifactsRepository(ArtifactRepository):
    def __init__(self, version_id: uuid.UUID, mlflow_client: MlflowClient):
        self.version_id = version_id
        self._tracking_client = mlflow_client
        super().__init__(artifact_uri=None)

    # these methods should be named list_files, log_directory, log_file, etc

    def list_artifacts(self, path=None) -> typing.List[FileInfo]:
        return self._tracking_client.list_files_for_artifact_version(
            version_id=self.version_id, path=path
        )

    def get_write_signed_url(self, local_file, artifact_path=None) -> str:
        dest_path = artifact_path or ""
        dest_path = dest_path.lstrip(posixpath.sep)
        dest_path = posixpath.join(dest_path, os.path.basename(local_file))

        return self._tracking_client.get_signed_urls_for_artifact_version_write(
            version_id=self.version_id, paths=[dest_path]
        )[0]

    def _signed_uri_upload_file(self, signed_url: SignedURL, local_file: str):
        _signed_uri_upload_file(signed_url=signed_url, local_file=local_file)

    def log_artifacts(self, local_dir, artifact_path=None):
        dest_path = artifact_path or ""
        dest_path = dest_path.lstrip(posixpath.sep)
        files = []

        for (root, _, file_names) in os.walk(local_dir):
            upload_path = dest_path
            if root != local_dir:
                rel_path = os.path.relpath(root, local_dir)
                rel_path = relative_path_to_artifact_path(rel_path)
                upload_path = posixpath.join(dest_path, rel_path)
            for file_name in file_names:
                local_file = os.path.join(root, file_name)
                files.append((upload_path, local_file))

        files.sort(
            key=lambda x: os.stat(x[1]).st_size
        )  # sort on the basis of file size

        # finally block doesn't execute when SIGTERM, SIGHUP, SIGKILL are received
        # Handle SIGTERM, SIGHUP signals to avoid zombie processes
        signal.signal(signal.SIGTERM, sigterm_handler)
        signal.signal(signal.SIGHUP, sighup_handler)

        # Log artifacts in parallel using ProcessPoolExecutor
        with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = []

            for upload_path, local_file in files:
                signed_url = self.get_write_signed_url(
                    local_file=local_file, artifact_path=upload_path
                )
                future = executor.submit(
                    _signed_uri_upload_file, signed_url, local_file
                )
                futures.append(future)

            try:
                for future in as_completed(futures):
                    future.result()
            except Exception as e:
                raise e
            finally:
                [f.cancel() for f in futures]
                # Accessing protected member of a class here (could fail in future versions)
                for pid, proc in executor._processes.items():
                    if proc.is_alive():
                        proc.terminate()

    def log_artifact(self, local_file, artifact_path=None):
        # TODO (chiragjn): Re-implement log_artifacts to take advantage of getting multiple signed urls at once
        #                  However care also needs to be taken to expose and pass in proper expiry because the user
        #                  user might be on slow connections or downloading many files sequentially might eat up time
        signed_url = self.get_write_signed_url(
            local_file=local_file, artifact_path=artifact_path
        )
        self._signed_uri_upload_file(signed_url, local_file)

    def _download_file(self, remote_file_path: str, local_path: str):
        if not remote_file_path:
            raise MlFoundryException(
                f"remote_file_path cannot be None or empty str {remote_file_path}"
            )
        # TODO (chiragjn): Re-implement download from parent to take advantage of getting multiple signed urls at once
        #                  However care also needs to be taken to expose and pass in proper expiry because the user
        #                  user might be on slow connections or downloading many files sequentially might eat up time
        signed_url = self._tracking_client.get_signed_urls_for_artifact_version_read(
            version_id=self.version_id, paths=[remote_file_path]
        )[0]
        download_file_using_http_uri(http_uri=signed_url.url, download_path=local_path)

"""Package for wtt02."""

from pathlib import Path
from typing import Optional, Union
import os
import logging

import platform
import zipfile
import tempfile

import urllib.request

import duckdb

from wtt02.__about__ import __version__, EXTENSION_NAME


__all__ = ["get_connection", "run_query_file", "__version__"]

logger = logging.getLogger(__name__)


class WTTException(Exception):
    """Base exception for wtt02."""


class WTT02ConfigurationException(WTTException):
    """Exception for wtt02 configuration."""


def run_query_file(
    con: duckdb.DuckDBPyConnection, file_path: Union[Path, str]
) -> duckdb.DuckDBPyConnection:
    """Run a query from a file."""
    if isinstance(file_path, str):
        file_path = Path(file_path)

    return con.execute(file_path.read_text())


def get_connection(
    database: str = ":memory:",
    read_only: bool = False,
    config: Optional[dict] = None,
    s3_uri: Optional[str] = None,
    file_path: Optional[Path] = None,
) -> duckdb.DuckDBPyConnection:
    """Return a connection with wtt02 loaded."""
    if "WTT_02_LICENSE" not in os.environ:
        raise WTT02ConfigurationException(
            "WTT_02_LICENSE environment variable not set. "
            "Check the docs or email at help@wheretrue.com"
        )

    if config is None:
        config = {"allow_unsigned_extensions": True}
    else:
        config["allow_unsigned_extensions"] = True

    con = duckdb.connect(
        database=database,
        read_only=read_only,
        config=config,
    )

    try:
        con.load_extension(EXTENSION_NAME)
        return con
    except duckdb.IOException:
        logger.info("Extension not found, installing. This only happens once per version/matchine.")
        extension_path = os.getenv("WTT02_EXTENSION_PATH")

        if extension_path:
            extension_path = Path(extension_path).absolute()
            con.install_extension(str(extension_path), force_install=True)
            con.load_extension(EXTENSION_NAME)

        elif file_path is not None and file_path.exists():
            con.install_extension(str(file_path.absolute()), force_install=True)
            con.load_extension(EXTENSION_NAME)

        elif s3_uri is not None:
            # download
            pass

        else:
            platform_uname = platform.uname()
            operating_system = platform_uname.system
            architecture = platform_uname.machine
            version = __version__

            from wtt02._env import ENVIRONMENT

            name = "wtt02"
            bucket = f"wtt-02-dist-{ENVIRONMENT}"
            filename = f"{name}-{version}-{operating_system}-{architecture}.zip"

            full_s3_path = (
                f"http://{bucket}.s3.amazonaws.com/extension/{name}/{filename}"
            )
            logger.info("Downloading extension from %s", full_s3_path)

            with tempfile.TemporaryDirectory() as temp_dir:
                temp_dir_path = Path(temp_dir)
                temp_file_name = temp_dir_path / filename

                try:
                    urllib.request.urlretrieve(full_s3_path, temp_file_name)
                except Exception as exp:
                    raise WTTException(
                        f"Unable to download extension from {full_s3_path}"
                    ) from exp

                with zipfile.ZipFile(temp_file_name, "r") as zip_ref:
                    zip_ref.extract(f"{name}.duckdb_extension", temp_dir)

                output_file = temp_dir_path / f"{name}.duckdb_extension"
                if not output_file.exists():
                    raise WTTException(
                        f"Unable to find extension file at {output_file}"
                    )

                logging.info("Installing extension from %s", output_file)
                con.install_extension(output_file.as_posix(), force_install=True)

                con.load_extension(EXTENSION_NAME)

    return con

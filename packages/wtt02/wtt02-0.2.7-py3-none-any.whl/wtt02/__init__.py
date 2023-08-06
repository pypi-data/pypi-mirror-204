"""Package for wtt02."""

from wtt02.__about__ import __version__
from wtt02.main import get_connection, run_query_file

__all__ = ["get_connection", "run_query_file", "__version__"]

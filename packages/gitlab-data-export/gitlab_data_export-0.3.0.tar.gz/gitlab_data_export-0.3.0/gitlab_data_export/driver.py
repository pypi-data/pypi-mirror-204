"""Executable module to drive data export functionality."""
import logging
import os
from enum import Enum
from typing import Callable

from .api.bigquery import BigQuery
from .api.datastore import Datastore
from .api.gitlab_export import Gitlab
from .checkpointing import Checkpoint

DATASTORE_ENV_VAR = 'GDE_DATASTORE'


class DatastoreType(Enum):
    """Datastore implementations.
    """
    BIGQUERY = 1


def get_datastore_factory() -> Callable[[], Datastore]:
    """Constructs a Datastore implementation from the current environment.

    Raises:
        ValueError: if the configured datastore doesn't match a known type

    Returns:
        Datastore: the Datastore implementation used to persist GitLab data
    """
    datastore = os.getenv(DATASTORE_ENV_VAR, 'bigquery').lower()
    logging.info('Initializing configured datastore: %s' % datastore)
    if datastore == DatastoreType.BIGQUERY.name.lower():
        return BigQuery

    raise ValueError(f'Unknown datastore type {datastore}')


def debug():
    import dotenv
    dotenv.load_dotenv()
    logging.basicConfig(level=logging.DEBUG)
    main()


def main():
    logging.basicConfig(level=logging.INFO)
    datastore = get_datastore_factory()()
    checkpoint = Checkpoint.load_previous()
    gl = Gitlab()
    gl.export_data(datastore, checkpoint).ensure()


if __name__ == '__main__':
    main()

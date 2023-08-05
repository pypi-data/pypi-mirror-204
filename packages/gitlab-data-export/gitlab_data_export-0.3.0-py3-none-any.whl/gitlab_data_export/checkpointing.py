"""Persistence of checkpointed state between export invocations.

When gitlab-data-export runs within a pipeline, it persists information about
its previous invocation. This information is used by subsequent invocations to
export only data that has changed since the prior invocation. Combined with the
materialized `data_date` field available within all exported data, this design
ensures that previously written data need never be updated while also providing
historical analytic capabilities to users of the exported data.
"""
from __future__ import annotations
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from .util import TIMESTAMP_FORMAT, format_time

CHECKPOINT_ENV_VAR = 'GDE_CHECKPOINT_PATH'


def checkpoint_path() -> Path:
    """Retrieves the configured Path for checkpoint persistence.

    Returns:
        Path: the checkpoint location
    """
    return Path(os.getenv(CHECKPOINT_ENV_VAR, 'gde_checkpoint.json'))


class Checkpoint:
    """A persisted checkpoint from a previous data export invocation.
    """

    def __init__(self, previous=None):
        self.previous = previous or datetime.utcnow()

    def _to_dict(self) -> dict:
        return {
            'previous': self.previous.strftime(TIMESTAMP_FORMAT)
        }

    def serialize(self) -> str:
        """Serializes the current checkpoint to a format compatible with on-disk storage.

        Returns:
            str: the serialized format
        """
        return json.dumps(self._to_dict())

    @staticmethod
    def deserialize(serialized: str) -> Checkpoint:
        """Deserializes a previously persisted checkpoint.

        Args:
            serialized: a serialized checkpoint as previously written by serialize.

        Returns:
            Checkpoint: the deserialized checkpoint
        """
        raw = json.loads(serialized)
        return Checkpoint(previous=datetime.strptime(raw['previous'], TIMESTAMP_FORMAT))

    def persist(self):
        """Persists the current checkpoint to disk."""
        path = checkpoint_path()
        logging.debug(
            'Persisting checkpoint to disk; CheckpointPath=%s' % path)
        with path.open(mode='w') as checkpoint_file:
            checkpoint_file.write(self.serialize())

    @classmethod
    def load_previous(cls) -> Optional[Checkpoint]:
        """Attempts to read and deserialize the previously persisted checkpoint for
        export invocation.

        Returns:
            Optional[Checkpoint]: the previously persisted checkpoint, or None if no such
            checkpoint could be found
        """
        try:
            path = checkpoint_path()
            logging.debug(
                'Attempting to load checkpoint from disk; CheckpointPath=%s' % path)
            with path.open() as checkpoint_file:
                checkpoint = Checkpoint.deserialize(checkpoint_file.read())
                logging.info('Previous checkpoint found; PreviousTimestamp=%s' % format_time(
                    checkpoint.previous))
                return checkpoint
        except FileNotFoundError:
            logging.info(
                'No checkpoint found; defaulting to historical backfill; CheckpointPath=%s' % path)
            return None

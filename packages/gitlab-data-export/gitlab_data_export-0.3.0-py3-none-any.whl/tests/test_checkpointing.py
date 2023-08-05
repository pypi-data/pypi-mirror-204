import os
import unittest
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from gitlab_data_export.checkpointing import Checkpoint, checkpoint_path


class TestPersistence(unittest.TestCase):

    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        os.environ['GDE_CHECKPOINT_PATH'] = os.path.join(
            self.temp_dir.name, 'checkpoint.json')
        self.checkpoint_file = Path(os.environ['GDE_CHECKPOINT_PATH'])
        self.checkpoint = Checkpoint(previous=datetime(2022, 4, 7, 0, 0, 0))

    def tearDown(self):
        self.temp_dir.cleanup()
        del os.environ['GDE_CHECKPOINT_PATH']

    def test_checkpoint_path(self):
        path = checkpoint_path()
        self.assertIsInstance(path, Path)

    def test_serialize_checkpoint(self):
        serialized = self.checkpoint.serialize()
        self.assertEqual(serialized, '{"previous": "2022-04-07 00:00:00"}')

    def test_deserialize_checkpoint(self):
        deserialized = Checkpoint.deserialize(
            '{"previous": "2022-04-07 00:00:00"}')
        self.assertEqual(deserialized.previous, datetime(2022, 4, 7))

    def test_load_previous_checkpoint(self):
        # No checkpoint should exist
        checkpoint = Checkpoint.load_previous()
        self.assertIsNone(checkpoint)

        # Write a checkpoint to disk
        self.checkpoint.persist()

        # Attempt to load the previous checkpoint
        checkpoint = Checkpoint.load_previous()
        self.assertIsNotNone(checkpoint)
        self.assertEqual(checkpoint.previous, datetime(2022, 4, 7))

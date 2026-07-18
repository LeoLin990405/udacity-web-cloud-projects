"""Tests for the composed MemeEngine image pipeline."""

import os
import sys
import tempfile
import unittest

from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))

from MemeEngine import MemeEngine  # noqa: E402


class MemeEngineTests(unittest.TestCase):
    """Verify supported inputs, resizing, output, and validation."""

    def setUp(self):
        """Create isolated source and output directories for each test."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.engine = MemeEngine(self.temp_dir.name)

    def tearDown(self):
        """Remove generated images."""
        self.temp_dir.cleanup()

    def _image_path(self, name, mode='RGB', size=(800, 400)):
        """Create a source image and return its path."""
        path = os.path.join(self.temp_dir.name, name)
        color = (40, 90, 140, 180) if mode == 'RGBA' else (40, 90, 140)
        Image.new(mode, size, color).save(path)
        return path

    def test_make_meme_composes_pipeline_and_caps_width(self):
        """A large JPEG is captioned, resized, and saved as an RGB JPEG."""
        source = self._image_path('source.jpg')

        output = self.engine.make_meme(source, 'Keep going', 'Ada', 700)

        self.assertTrue(os.path.isfile(output))
        with Image.open(output) as generated:
            self.assertEqual(generated.size, (500, 250))
            self.assertEqual(generated.mode, 'RGB')

    def test_make_meme_accepts_transparent_png(self):
        """An RGBA PNG is normalized before the generated JPEG is saved."""
        source = self._image_path('source.png', mode='RGBA', size=(300, 200))

        output = self.engine.make_meme(source, 'PNG works', 'Grace')

        with Image.open(output) as generated:
            self.assertEqual(generated.size, (300, 200))
            self.assertEqual(generated.format, 'JPEG')

    def test_make_meme_rejects_invalid_width(self):
        """Invalid width values fail with a human-readable exception."""
        source = self._image_path('source.jpg')

        with self.assertRaisesRegex(ValueError, 'positive integer'):
            self.engine.make_meme(source, 'Hello', 'Author', 0)


if __name__ == '__main__':
    unittest.main()

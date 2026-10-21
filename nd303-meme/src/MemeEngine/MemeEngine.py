"""MemeEngine module for generating image memes with overlaid text."""

import os
import random

from PIL import Image, ImageDraw, ImageFont


class MemeEngine:
    """Engine for creating memes by overlaying quotes onto images.

    Loads an image, resizes it to a maximum width, draws quote text
    and author onto the image, and saves the result.
    """

    def __init__(self, output_dir: str):
        """Initialize MemeEngine with the given output directory.

        Args:
            output_dir: Directory where generated memes will be saved.
        """
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    @staticmethod
    def _load_image(img_path: str) -> Image.Image:
        """Load a JPEG or PNG image and normalize it for JPEG output."""
        try:
            with Image.open(img_path) as source:
                return source.convert('RGB')
        except FileNotFoundError:
            raise
        except (OSError, ValueError) as exc:
            raise RuntimeError(
                f"Unable to open image '{img_path}': {exc}"
            ) from exc

    @staticmethod
    def _resize_image(image: Image.Image, width: int) -> Image.Image:
        """Resize an image proportionally to at most 500 pixels wide."""
        if isinstance(width, bool) or not isinstance(width, int) or width <= 0:
            raise ValueError('width must be a positive integer')

        target_width = min(width, 500)
        if image.width <= target_width:
            return image

        target_height = round(image.height * target_width / image.width)
        return image.resize(
            (target_width, target_height),
            Image.Resampling.LANCZOS,
        )

    @staticmethod
    def _load_font() -> ImageFont.ImageFont:
        """Load a readable TrueType font, with a portable fallback."""
        try:
            return ImageFont.truetype('arial.ttf', 20)
        except OSError:
            return ImageFont.load_default()

    @classmethod
    def _draw_caption(cls, image: Image.Image, text: str,
                      author: str) -> None:
        """Draw a quote and its author at a random valid image location."""
        if not isinstance(text, str) or not text.strip():
            raise ValueError('text must be a non-empty string')
        if not isinstance(author, str) or not author.strip():
            raise ValueError('author must be a non-empty string')

        draw = ImageDraw.Draw(image)
        font = cls._load_font()
        caption = f'{text.strip()}\n- {author.strip()}'
        bounds = draw.multiline_textbbox((0, 0), caption, font=font,
                                         spacing=4, stroke_width=2)
        caption_width = bounds[2] - bounds[0]
        caption_height = bounds[3] - bounds[1]
        max_x = max(image.width - caption_width - 10, 0)
        max_y = max(image.height - caption_height - 10, 0)
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)

        draw.multiline_text(
            (x, y),
            caption,
            fill='white',
            font=font,
            spacing=4,
            stroke_width=2,
            stroke_fill='black',
        )

    def _save_image(self, image: Image.Image) -> str:
        """Save a generated meme and return its path."""
        filename = f'meme_{random.randint(0, 1_000_000_000)}.jpg'
        out_path = os.path.join(self.output_dir, filename)
        try:
            image.save(out_path, format='JPEG', quality=90)
        except OSError as exc:
            raise RuntimeError(
                f"Unable to save meme to '{out_path}': {exc}"
            ) from exc
        return out_path

    def make_meme(self, img_path: str, text: str, author: str,
                  width: int = 500) -> str:
        """Generate a meme from the given image and quote.

        Args:
            img_path: Path to the source image file.
            text: Quote body text to overlay on the image.
            author: Quote author to overlay below the body text.
            width: Maximum width for the output image (default 500).

        Returns:
            Path to the saved meme image.

        Raises:
            FileNotFoundError: If img_path does not exist.
            RuntimeError: If the image cannot be opened or saved.
            ValueError: If width, text, or author is invalid.
        """
        image = self._load_image(img_path)
        image = self._resize_image(image, width)
        self._draw_caption(image, text, author)
        return self._save_image(image)

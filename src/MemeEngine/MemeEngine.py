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
        """
        try:
            img = Image.open(img_path)
        except FileNotFoundError:
            raise
        except Exception as e:
            raise RuntimeError(f"Unable to open image '{img_path}': {e}")

        target_width = min(width, 500)
        if img.width > target_width:
            ratio = target_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((target_width, new_height))

        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except OSError:
            font = ImageFont.load_default()

        x = random.randint(10, max(img.width // 4, 11))
        y = random.randint(20, max(img.height - 80, 30))

        draw.text((x, y), text, fill="white", font=font)
        draw.text((x, y + 25), f"- {author}", fill="white", font=font)

        filename = f"meme_{random.randint(0, 1_000_000_000)}.jpg"
        out_path = os.path.join(self.output_dir, filename)
        try:
            img.save(out_path)
        except Exception as e:
            raise RuntimeError(f"Unable to save meme to '{out_path}': {e}")

        return out_path

from PIL import Image
from io import BytesIO
import requests


# =========================================================
# IMAGE COLOR FUNCTIONS
# =========================================================

def get_dom_color(image_url):
    """
    Get the most common color from an album cover.
    """

    # Handle images stored locally in the static folder.
    if image_url.startswith("/static/"):
        image_path = image_url.lstrip("/")

        with open(image_path, "rb") as f:
            image = Image.open(f)
            image = image.resize((50, 50))

    # Handle images loaded from an external URL.
    else:
        response = requests.get(image_url)

        image = Image.open(BytesIO(response.content))
        image = image.convert("RGB")
        image = image.resize((50, 50))

    # Get every pixel's color.
    colors = list(image.getdata())

    # Find the most common color.
    most_common = max(set(colors), key=colors.count)

    return most_common
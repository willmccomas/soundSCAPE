from PIL import Image
from io import BytesIO
import requests

def get_dom_color(image_url):
    if image_url.startswith("/static/"):
        image_path = image_url.lstrip("/")

        with open(image_path, "rb") as f:
            image = Image.open(f)
            image = image.resize((50, 50))

    else:
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))
        image = image.convert('RGB')
        image = image.resize((50, 50))

    colors = list(image.getdata())
    most_common = max(set(colors), key = colors.count)
    return most_common
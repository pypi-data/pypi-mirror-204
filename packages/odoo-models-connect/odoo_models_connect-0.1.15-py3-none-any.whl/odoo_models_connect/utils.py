from PIL import Image
from io import BytesIO
import base64


def convert_pil_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()
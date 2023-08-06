import io
import base64

def image_to_base64(image):
    bytesIO = io.BytesIO()
    try:
        image.save(bytesIO, "JPEG")
    except:
        image.save(bytesIO, "PNG")
    b64encoded = base64.b64encode(bytesIO.getvalue())
    base64_str = b64encoded.decode("utf-8")
    return base64_str

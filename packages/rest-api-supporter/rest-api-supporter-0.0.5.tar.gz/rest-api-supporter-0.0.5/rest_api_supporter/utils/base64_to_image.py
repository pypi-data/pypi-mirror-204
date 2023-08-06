import base64
from PIL import Image
import re

def base64_to_image(value):
    #print(value) #data:image/jpeg;base64,/9j/4TT...
    value = value.replace("data:", "") #data url 부분 제거
    value = re.sub('^.+,', '', value)
    #print(value) #/9j/4TT...
    bytes = base64.b64decode(value)
    bytesIO = io.BytesIO(bytes)
    value = Image.open(bytesIO)
    return value

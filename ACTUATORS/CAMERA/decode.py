import base64

def convertImageToBase64(name):
    try:  
        with open(name, "rb") as image_file:
            encoded = base64.b64encode(image_file.read())
            return encoded
        pass
    finally:
        print("decoded successfully")
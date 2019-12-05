import decode, camera, send
import sys

def main(argv):
    hostname = "129.69.209.70"
    image_name = argv[0]
    camera.takePic(image_name)
    encoded = decode.convertImageToBase64(image_name)
    send.publishEncodedImage(encoded, hostname, 1883)
    
if __name__ == "__main__":
   main(sys.argv[1:])
#All the stuff behind
import pyzbar.pyzbar as QR
from PIL import Image

#Plan to use a json loader here, But ended up cancel

def Decoder(file_path):
    try:
        return_string = QR.decode(Image.open(file_path))
        print(return_string)
        return(return_string[0].data.decode())
    except SystemError:
        #raise SystemError
        return None

def Encoder():
    print('Placeholder')
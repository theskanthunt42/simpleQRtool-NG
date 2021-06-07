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

def Config_Loader(config_path):
    try:
        with open(config_path) as f:
            loaded_json = json.load(f)
            return loaded_json
    except SystemError:
        return None



#All the stuff behind
import pyzbar.pyzbar as QR
from PIL import Image
import qrcode
import tempfile

#Plan to use a json loader here, But ended up cancel
#7.June update: Done as Config_Loader
def Decoder(file_path):
    try:
        return_string = QR.decode(Image.open(file_path))
        print(return_string)
        return(return_string[0].data.decode())
    except SystemError:
        #raise SystemError
        return None

def Encoder(conf, image_size, text, encoding):
    #print('Placeholder')
    qr_object = qrcode.QRCode(
        version=image_size, error_correction=conf['error_correction'], box_size=conf['box_size'], border=conf['border']
        )
    qr_object.add_data(text.encode(encoding))
    qr_object.make(fit=True)
    image_object = qr_object.make_image(fill_color=conf['color'], back_color=conf['background_color'])
    saved_filename = tempfile.mktemp('.png')
    open(saved_filename, 'wb').close()
    image_object.save(saved_filename)
    return saved_filename

def Config_Loader(config_path):
    try:
        with open(config_path) as f:
            loaded_json = json.load(f)
            return loaded_json
    except SystemError:
        return None

def Copy(original, desire, platform):
    if platform == 'linux' or 'linux2' or 'darwin' or 'freebsd' or 'openbsd' or 'macos':
        try:
            os.system(f'cp {original} {desire}')
            outputs = f'PNG exported to {desire}'
        except SystemError:
            outputs = f"Can't export due to couldn't copy the PNG to the desire path."
    elif platform == 'win32' or 'win64' or 'cygwin' or 'msys':
        try:
            os.system(f'copy {original} {desire}')
            outputs = f'PNG exported to {filepath}'
        except SystemError:
            outputs = "Can't export due to couldn't copy the PNG to the desire path."
    else:
        outputs = "Can't copy file."
    return outputs


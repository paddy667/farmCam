from time import sleep
from cStringIO import StringIO
import SimpleCV as scv

def handle_websocket(ws):
    cam = scv.Camera(0)
    while True:
        fp = StringIO()
        image = cam.getImage().getPIL()
        image.save(fp, 'JPEG')
        ws.send(fp.getvalue().encode("base64"))
        #fp.close() << benchmark and memory tests needed
        sleep(0.05)

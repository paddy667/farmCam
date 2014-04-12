from time import sleep
from cStringIO import StringIO
import SimpleCV as scv
import cv

def handle_websocket(ws):
    cam = scv.Camera(0)
    #cv.NamedWindow("w1", cv.CV_WINDOW_AUTOSIZE)
    #capture = cv.CaptureFromCAM(0)
    
    #while True:
    #    frame = cv.QueryFrame(capture)
    #    cv.ShowImage("w1", frame)
        
    while True:
        fp = StringIO()
        image = cam.getImage().getPIL()
        image.save(fp, 'JPEG')
        print fp.getvalue().encode("base64")
        ws.send(fp.getvalue().encode("base64"))
        #fp.close() << benchmark and memory tests needed
        sleep(0.05)

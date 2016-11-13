import Tkinter
import cv2
from PIL import Image, ImageTk


class CanvasAndWebcamApp(object):
    """
    This is a base class for an application that uses an OpenCV window to display data from
    a webcam as well as a Tkinter window to display a Canvas.
    This class was written for the OpenCV module info session on Nov. 16, 2013, for 15-112 at CMU.
    You may use it for your term project but you must cite it appropriately.
    """
    def __init__(self, title="Video", delay_ms=100, camera=0, canvasDimensions = (500,500)):
        self.title = title
        self.delay = delay_ms
        self.camera = camera
        self.canvasDimensions = canvasDimensions
        self.webcamActive = False
    def _startCanvas(self, startWebcam):
        self.root = Tkinter.Tk()
        width, height = self.canvasDimensions
        self.canvas = Tkinter.Canvas(self.root, width=width, height=height)
        self.bindEventListeners()
        self.canvas.pack()
        self.canvas.after(self.delay, self._timerFiredWrapper)
        if startWebcam:
            self.startWebcam()
        self.root.mainloop()
    def _getCapture(self):
        return cv2.VideoCapture(self.camera)
    def _timerFiredWrapper(self):
        if self.webcamActive and self.cap.isOpened():
            ret, frame = self.cap.read()
            if frame is not None:
                img = self.processFrame(frame)
                cv2.imshow(self.title, img)
            k = cv2.waitKey(0xA) & 0xFF
            if k != (~0 & 0xFF):
                self.keyPressedWebcamWrapper(k)
        self.timerFired()
        self._redrawAllWrapper()
        self.canvas.after(self.delay, self._timerFiredWrapper)
    def _redrawAllWrapper(self):
        self.canvas.delete(Tkinter.ALL)
        self.redrawAll()
    def _mouseEvent(self, event, x, y, flags, param):
        """Relays a mouse event to the method corresponding to its event code."""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouseLeftDownWebcam(x, y, flags, param)
        elif event == cv2.EVENT_LBUTTONUP:
            self.mouseLeftUpWebcam(x, y, flags, param)
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.mouseRightDownWebcam(x, y, flags, param)
        elif event == cv2.EVENT_RBUTTONUP:
            self.mouseRightUpWebcam(x, y, flags, param)
        elif event == cv2.EVENT_MOUSEMOVE:
            self.mouseMoveWebcam(x, y, flags, param)
    def _keyPressedWebcamWrapper(self, k):
        if k == 27: # Esc
            self.closeWebcam()
        else:
            self.keyPressedWebcam(k) 
    
    def run(self, startWebcam=True):
        self.init()
        self._startCanvas(startWebcam)
    def bindEventListeners(self):
        """Override this method to subscribe to more events."""
        self.canvas.bind('<Button-1>', self.leftMouseClickCanvas)
        self.canvas.bind('<Button-2>', self.rightMouseClickCanvas)
        self.canvas.bind('<Key>', self.keyPressedCanvas)
    def startWebcam(self):
        cv2.namedWindow(self.title, cv2.CV_WINDOW_AUTOSIZE)
        cv2.setMouseCallback(self.title,self._mouseEvent)
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onCloseWrapper)
        self.cap = self._getCapture()
        self.webcamActive = True
    def close(self):
        self.root.destroy()
    def onCloseWrapper(self):
        self.closeWebcam()
        self.onClose()
        self.close()
    def closeWebcam(self):
        cv2.destroyAllWindows()
        self.cap.release()
    def keyPressedWebcam(self, k): pass
    def onClose(self): pass
    def processFrame(self, frame): return frame
    def mouseLeftDownWebcam(self, x, y, flags, param): pass
    def mouseLeftUpWebcam(self, x, y, flags, param): pass
    def mouseRightDownWebcam(self, x, y, flags, param): pass
    def mouseRightUpWebcam(self, x, y, flags, param): pass
    def mouseMoveWebcam(self, x, y, flags, param): pass
    def leftMouseClickCanvas(self, event): pass
    def rightMouseClickCanvas(self, event): pass
    def keyPressedCanvas(self, event): pass
    def redrawAll(self):
        self.canvas.create_rectangle(20,30,40,50,color="blue")
    def timerFired(self): pass
    def init(self): pass

app = CanvasAndWebcamApp("My awesome app")
app.run()
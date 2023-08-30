import cv2
import numpy as np
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, ListProperty
from kivy.event import EventDispatcher

a = []
b = []
#automated cell counting//////////////////////////////////////////////////////////////////
def cell_counting():
    pic = cv2.imread("img.png")
    print("mainpic", pic.shape)
    #cv2.namedWindow("cell", cv2.WINDOW_NORMAL)
    #cv2.imshow("cell", pic)
    pic_gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(pic_gray, (5, 5), 3)
    edge = cv2.Canny(blur, 20, 30, L2gradient=True)
    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(blur, kernel)
    edge_erosion = cv2.Canny(erosion, 20, 30, L2gradient=True)
    opening = cv2.morphologyEx(pic_gray, cv2.MORPH_OPEN, kernel)
    edge_opening = cv2.Canny(opening, 20, 30, L2gradient=True)
    closing = cv2.morphologyEx(blur, cv2.MORPH_CLOSE, kernel)
    edge_closing = cv2.Canny(closing, 20, 30, L2gradient=True)
    gradient = cv2.morphologyEx(blur, cv2.MORPH_GRADIENT, kernel)
    blackhat = cv2.morphologyEx(blur, cv2.MORPH_BLACKHAT, kernel)
    blackhat2 = cv2.morphologyEx(pic_gray, cv2.MORPH_BLACKHAT, kernel)
    # Find circles
    # Read image as gray-scale
    # img = cv2.imread('circles.png', cv2.IMREAD_COLOR)
    # Convert to gray-scale
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Blur the image to reduce noise
    # img_blur = cv2.medianBlur(gray, 5)
    # Apply hough transform on the image
    circles = cv2.HoughCircles(opening, cv2.HOUGH_GRADIENT, 1,pic.shape[0]/64, param1=200, param2=10, minRadius=1, maxRadius=15)
    # Draw detected circles
    if circles is not None:
        circles = np.uint16(np.around(circles))
        count = 0
        for i in circles[0, :]:
            count += 1
            # Draw outer circle
            cv2.circle(pic, (i[0], i[1]), i[2], (0, 255, 0), 2)
            # Draw inner circle
            cv2.circle(pic, (i[0], i[1]), 2, (0, 0, 255), 3)

    print("count", count)
    #cv2.namedWindow("count circle", cv2.WINDOW_NORMAL)
    #cv2.imshow("count circle", pic)
    a.append(count)
    #cv2.waitKey()
    if len(a) == 4:
        s = 0
        for i in range(0,4):
            s = s + a[i]
        b.append(s)

#/////////////////////////////////////////////////////////////////////////////////////////////////////////
#kivy codes//////////////////////////////////////////////////////////////////////////////////////////////
class Mycell(ScreenManager):
    pass

class FirstScreen(Screen):
    ti_concentration_range = ObjectProperty(0)
    ti_result = ObjectProperty(None)
    def click(self):
        number = self.ti_concentration_range.text
        javab = int(number) * b[0]
        self.ti_result.text = str(javab)
        self.ti_concentration_range = ""
        self.ti_result = ""

class SecondScreen(Screen):
    pass

class ThirdScreen(Screen):
    ti_concentration_range = ObjectProperty(None)
    ti_result = ObjectProperty(None)
    def click(self):
        self.ti_result.text = self.ti_concentration_range.text + "\n" + "input opencv"
        print(self.ti_result.text)
        self.ti_concentration_range = ""
        self.ti_result = ""

class FourthScreen(Screen):
    ti_result = ObjectProperty(None)
    def click(self):
        self.ti_result.text = self.ti_result.text + "\n" + "input opencv"
        print(self.ti_result.text)
        self.ti_result = ""

#  CAMERA  //////////////////////////////////////////////////////////////
class CameraClick(Screen):
    def capture(self):
        camera = self.ids.camera
        camera.export_to_png("img.png")
        print("Captured")
        cell_counting()

#////////////////////////////////////////////////////////////////////////
style = Builder.load_file("MyApp.kv")
class MyyApp(App):
    def build(self):
        Window.size = (Window.width, Window.height)
        return style

if __name__ == "__main__":
    MyyApp().run()

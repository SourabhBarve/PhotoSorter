import eel
from tkinter import filedialog, Tk
from constants import Constants
import os
import base64

import cv2

from faceDetector import getFaces

print(Constants)
eel.init("./frontend")
context = None

def showInInfo(text):
    eel.showInfo(text)

class Context():
    def __init__(self):
        self.preprocessor = Constants.Preprocessors.none
        self.sourceDir = ""

    def setPreprocessor(self, preprocessor):
        print(f"Setting preprocessor: {preprocessor}/ {type(self).__name__}")
        self.preprocessor = preprocessor
        showInInfo(f"Preprocessor: {preprocessor}")

    def setSourceDirectory(self, dir):
        print(f"Setting dir: {dir}/ {type(self).__name__}")
        self.sourceDir = dir
        for root, dirs, files in os.walk(self.sourceDir):
            imgFiles = 0
            imgExts = ["png", "jpg", "jpeg"]
            for f in files:
                if (x in f for x in imgExts):
                    imgFiles += 1
            showInInfo(f"Path: {self.sourceDir}; Contains: {len(dirs)} Directories, {len(files)} Files ({imgFiles} Images)")
    
    def getImgFilePaths(self, recursive=False):
        if self.sourceDir != "":
            imgFiles = []
            for root, dirs, files in os.walk(self.sourceDir):
                imgExts = ["png", "jpg", "jpeg"]
                if recursive == False:
                    for f in files:
                        if (x in f for x in imgExts):
                            imgFiles.append(self.sourceDir + "/" + f)
                else:
                    print("Recursive is not yet supported")
            return imgFiles

        

class Labeller(Context):
    def __init__(self):
        super().__init__()
        self.currentImage = None
        self.currentSubImage = None
        self.generator = None
        self.previousYield = None
        self.labels = []
        self.dataDir = os.path.join(os.getcwd(), "labelledData")
        os.mkdir(self.dataDir)

    def generatorFunction(self):
        filePaths = self.getImgFilePaths()[:10]
        for f in filePaths:
            faces = getFaces(f)
            pixels =  cv2.imread(f)
            self.currentImage = pixels
            success, encoded_image = cv2.imencode('.jpg', pixels)
            content = encoded_image.tobytes()
            eel.setOriginalImage(base64.b64encode(content).decode('ascii'))
            eel.setPreviewImage("")()
            for face in faces:
                print(face)
                x1, y1, width, height = face['box']
                x2, y2 = x1 + width, y1 + height
                if(x1<0):
                    x1 = 0
                if(y1<0):
                    y1 = 0
                self.currentSubImage = pixels[y1:y2, x1:x2]
                success, encoded_imageFace = cv2.imencode('.jpg', pixels[y1:y2, x1:x2])
                content = encoded_imageFace.tobytes()
                eel.setPreviewImage(base64.b64encode(content).decode('ascii'))()
                yield 1
                # print(f"Label received: {label}")
                # showInInfo(f"Label received: {label}")
            yield 0
        yield -1

    def proceedToNext(self):
        self.previousYield = next(self.generator)
        if self.previousYield == 1:
            return 0
        elif self.previousYield == 0:
            self.currentSubImage = None
            return self.proceedToNext()
        elif self.previousYield == -1:
            self.indicateFinishedAllImages()
            return 1

    def startLabelling(self):
        print("Labeller: Labelling triggered")
        self.generator = self.generatorFunction()
        self.proceedToNext()

    def setLabelAndProceed(self, label):
        # Process current subimage
        print(f"Label received: {label}")
        showInInfo(f"Label received: {label}")

        if label not in self.labels:
            self.createNewLabel(label)
        
        self.addToLabelFolder(label)
        # clean the state
        if self.previousYield == 1:
            self.currentSubImage = None
            self.proceedToNext()

    def indicateFinishedAllImages(self):
        print("All images labelled")
        # TODO: Add stop code

    def createNewLabel(self, label):
        labelDir = os.path.join(self.dataDir, label)
        if not os.path.isdir(labelDir):
            os.mkdir(labelDir)

    def addToLabelFolder(self, label):
        labelDir = os.path.join(self.dataDir, label)
        cwd = os.getcwd()
        os.chdir(labelDir)
        noOfFiles = len(os.listdir(labelDir))
        fName = label + "_" + str(noOfFiles + 1) + ".jpg"
        cv2.imwrite(fName, self.currentSubImage)
        os.chdir(cwd)



class Sorter(Context):
    def __init__(self):
        super().__init__()
        
@eel.expose
def setContext(ctxt):
    global context
    if(ctxt == Constants.Contexts.Labeller):
        context = Labeller()
        showInInfo("Labeller")
    elif(ctxt == Constants.Contexts.Sorter):
        context = Sorter()
        showInInfo("Sorter")
    else:
        context = None

@eel.expose
def setPreprocessor(preprocessor):
    global context
    if context != None:
        context.setPreprocessor(preprocessor)

@eel.expose
def openSourceDirectorySelector():
    global context
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    root.update()
    dirname = filedialog.askdirectory()
    root.destroy()
    if context != None:
        context.setSourceDirectory(dirname)

@eel.expose
def startLabelling():
    global context
    print(f"Labelling triggered of {type(context).__name__}")
    if type(context).__name__ == "Labeller":
        context.startLabelling()

@eel.expose
def setLabel(label):
    global context
    print(f"setLabel triggered of {type(context).__name__}")
    if type(context).__name__ == "Labeller":
        context.setLabelAndProceed(label)


eel.start('index.html', size=(1000, 600))
#NO 1 Hari ke1
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from os import *
from PIL import Image
from PIL.ImageFilter import *
#no 2
app = QApplication([])
window = QWidget()
window.resize(500,500)
window.setWindowTitle("Aplikasi Easy Editor")

#no 3
btn_folder =QPushButton("Folder")
folder_list =QListWidget()
picture = QLabel("Image")
btn_right = QPushButton("Right")
btn_left = QPushButton("Left")
btn_mirror = QPushButton("Mirror")
btn_sharpness = QPushButton("Sharpness")
btn_bnw = QPushButton("B/W")

#no 4
main_layout = QHBoxLayout()
L1 = QVBoxLayout()
L2 = QVBoxLayout()
L3 = QHBoxLayout()
#pengisian L1
L1.addWidget(btn_folder)
L1.addWidget(folder_list)
#Pengisian L3
L3.addWidget(btn_right)
L3.addWidget(btn_left)
L3.addWidget(btn_mirror)
L3.addWidget(btn_sharpness)
L3.addWidget(btn_bnw)
#pengisian L2
L2.addWidget(picture)
L2.addLayout(L3)
#pengisian main_layout
main_layout.addLayout(L1)
main_layout.addLayout(L2)
#setting window ke layoutnya
window.setLayout(main_layout)

def filter(files,extension):
    result = []
    for filename in files:
        for ext in extension:
            if filename.endswith(ext):
                result.append(filename)
    return result

workdir = ""

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showsFilenamelist():
    extension = [".jpg",".png",".jpeg",".bmp",".gif",".jfif"]
    chooseWorkdir()
    filenames = filter(listdir(workdir), extension)
    folder_list.clear()
    for filename in filenames:
        
        folder_list.addItem(filename)

btn_folder.clicked.connect(showsFilenamelist)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified"
    
    def loadimage(self,dir,filename):
        self.dir = dir
        self.filename = filename
        image_path = path.join(dir,filename)
        self.image = Image.open(image_path)

    def showimage(self,path):
            picture.hide()
            pixmapimage = QPixmap(path)
            w,h = picture.width(), picture.height()
            pixmapimage = pixmapimage.scaled(w,h,Qt.KeepAspectRatio)
            picture.setPixmap(pixmapimage)
            picture.show()

    def saveImage(self):
        image_path = path.join(workdir, self.save_dir)
        if not (path.exists(image_path) or path.isdir(image_path)):
            mkdir(image_path)
        fullname = path.join(image_path, self.filename)
        self.image.save(fullname)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = path.join(workdir,self.save_dir, self.filename)
        self.showimage(image_path)

    def DO_MIRROR(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = path.join(workdir,self.save_dir, self.filename)
        self.showimage(image_path)

    def DO_LEFT(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = path.join(workdir,self.save_dir, self.filename)
        self.showimage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = path.join(workdir,self.save_dir, self.filename)
        self.showimage(image_path)

    def do_sharp(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = path.join(workdir,self.save_dir, self.filename)
        self.showimage(image_path)

workimage = ImageProcessor()
def showchosenimage():
    if folder_list.currentRow() >= 0:
        filename = folder_list.currentItem().text()
        workimage.loadimage(workdir,filename)
        image_path = path.join(workimage.dir,workimage.filename)
        workimage.showimage(image_path)

btn_bnw.clicked.connect(workimage.do_bw)
btn_mirror.clicked.connect(workimage.DO_MIRROR)
btn_left.clicked.connect(workimage.DO_LEFT)
btn_right.clicked.connect(workimage.do_right)
btn_sharpness.clicked.connect(workimage.do_sharp)

folder_list.currentRowChanged.connect(showchosenimage)

window.show()
app.exec_()

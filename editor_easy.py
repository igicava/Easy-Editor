from PyQt5.QtWidgets import(
    QApplication,QWidget,
    QLabel,QPushButton,QListWidget,
    QHBoxLayout,QVBoxLayout,QFileDialog
)
import os
from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import ImageFilter
from PIL.ImageFilter import SHARPEN

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenameList():
    extensions = ['.jpg','.jpeg','.png','.gif','.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir),extensions)
    list_files.clear()
    for filename in filenames:
        list_files.addItem(filename)

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result
       
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified/'

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage(image_path)
    
    def saveImage(self):
        path = os.path.join(self.dir,self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path,self.filename)
        self.image.save(image_path)

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir,filename)
        self.image = Image.open(image_path)

    def showImage(self,path):
        btn_image.hide()
        pixmapimage =QPixmap(path)
        w,h = btn_image.width(),btn_image.height()
        pixmapimage = pixmapimage.scaled(w,h,Qt.KeepAspectRatio)
        btn_image.setPixmap(pixmapimage)
        btn_image.show()
    
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path) 
    
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path) 
    
    def do_sharpen(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

def showChosenImage():
    if list_files.currentRow() >= 0:
        filename = list_files.currentItem().text()
        workimage.loadImage(workdir,filename)
        image_path = os.path.join(workimage.dir,workimage.filename)
        workimage.showImage(image_path)

app = QApplication([])
win = QWidget()
win.setWindowTitle('Easy Editor')
win.resize(700, 400)
btn_image = QLabel('Картинка')
btn_dir = QPushButton('Папка')
list_files = QListWidget()

btn_left = QPushButton('Лево')
btn_right = QPushButton('Право')
btn_flip = QPushButton('Зеркало')
btn_sharp = QPushButton('Резкость')
btn_bw = QPushButton('Ч/Б')

line = QHBoxLayout()
colling1 = QVBoxLayout()
colling2 = QVBoxLayout()
colling1.addWidget(btn_dir)
colling1.addWidget(list_files)
colling2.addWidget(btn_image,95)
line_tools = QHBoxLayout()
line_tools.addWidget(btn_left)
line_tools.addWidget(btn_right)
line_tools.addWidget(btn_flip)
line_tools.addWidget(btn_sharp)
line_tools.addWidget(btn_bw)
colling2.addLayout(line_tools)
line.addLayout(colling1,20)
line.addLayout(colling2,80)
win.setLayout(line)

workimage = ImageProcessor()

workdir = ''

list_files.currentRowChanged.connect(showChosenImage)

btn_bw.clicked.connect(workimage.do_bw)

btn_flip.clicked.connect(workimage.do_flip)

btn_left.clicked.connect(workimage.do_left)

btn_right.clicked.connect(workimage.do_right)

btn_sharp.clicked.connect(workimage.do_sharpen)

btn_dir.clicked.connect(showFilenameList)

win.show()
app.exec()
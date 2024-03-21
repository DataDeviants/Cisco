from PyQt5 import QtWidgets
import pyqtgraph as pg
import numpy as np
from PIL import Image

img_path = 'res/floor1.png'
image = Image.open(img_path)
image = image.rotate(-90)
image_np = np.array(image)

length = 228.30688
width = 346.92673
height = 13.0
offsetX = 14.67
offsetY = 21.18
imageWidth = 4162
imageHeight = 2739

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Setting up the matplotlib widget
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        self.index = 0
        self.x = []
        self.y = []

        img = pg.ImageItem(image_np)
        self.graphWidget.addItem(img)
        
        self.scatter = pg.ScatterPlotItem(self.x, self.y, pen=pg.mkPen(width=10, color='y'))
        self.graphWidget.addItem(self.scatter)
        
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start(1000)  # Refresh rate ( in this case its 1 sec)

    def update_plot_data(self):
        with open ('res/pos.csv', 'r') as f:
            try:
                data = f.readlines()[-1].split(',')
            except:
                return
            x = [float(data[0])]
            y = [float(data[1])]
              
            datax = [(x[0] + offsetX) / (width + 2 * offsetX) * imageWidth]
            datay = [(y[0] + offsetY) / (length + 2 * offsetY) * imageHeight]
            print(x, y, datax, datay)
            self.scatter.setData(datay, datax)
            

app = QtWidgets.QApplication([])
w = MainWindow()
w.show()
app.exec_()

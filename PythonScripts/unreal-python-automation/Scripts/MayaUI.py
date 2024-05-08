

import maya.cmds as cmds
import maya.mel as mel
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtUiTools, QtCore, QtGui, QtWidgets
from functools import partial # optional, for passing args during signal function calls
import sys

class MayaUI(QtWidgets.QWidget):
    """
    Create a default tool window.
    """
    window = None
    
    def __init__(self, parent = None):
        """
        Initialize class.
        """
        super(MayaUI, self).__init__(parent = parent)
        self.setWindowFlags(QtCore.Qt.Window)
        self.widgetPath = 'D:\\GameDevelopment\\msccavepipelineandtdproject24-RahulChandra99\\'
        self.widget = QtUiTools.QUiLoader().load(self.widgetPath + 'mainWidget.ui')
        self.widget.setParent(self)
        # set initial window size
        self.resize(400, 100) 

        # locate UI widgets
        self.btn_makegeo = self.widget.findChild(QtWidgets.QPushButton, 'btn_makeGeo')  
        self.btn_close = self.widget.findChild(QtWidgets.QPushButton, 'btn_close')   
        self.radio_sphere = self.widget.findChild(QtWidgets.QRadioButton, 'radioBtn_sphere') 
        self.radio_cube = self.widget.findChild(QtWidgets.QRadioButton, 'radioBtn_cube') 
        self.radio_cylinder = self.widget.findChild(QtWidgets.QRadioButton, 'radioBtn_cylinder') 

        # assign functionality to buttons
        self.btn_makegeo.clicked.connect(self.makegeometry)
        self.btn_close.clicked.connect(self.closeWindow)
    
    """
    Your code goes here
    """
    def makegeometry(self):
        if self.radio_sphere.isChecked():
            cmds.polySphere()   
        if self.radio_cube.isChecked():
            cmds.polyCube() 
        if self.radio_cylinder.isChecked():
            cmds.polyCylinder() 

    def resizeEvent(self, event):
        """
        Called on automatically generated resize event
        """
        self.widget.resize(self.width(), self.height())
        
    def closeWindow(self):
        """
        Close window.
        """
        print ('closing window')
        self.destroy()
    
def openWindow():
    """
    ID Maya and attach tool window.
    """
    # Maya uses this so it should always return True
    if QtWidgets.QApplication.instance():
        # Id any current instances of tool and destroy
        for win in (QtWidgets.QApplication.allWindows()):
            if 'myToolWindowName' in win.objectName(): # update this name to match name below
                win.destroy()

    #QtWidgets.QApplication(sys.argv)
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QtWidgets.QWidget)
    MayaUI.window = MayaUI(parent = mayaMainWindow)
    MayaUI.window.setObjectName('myToolWindowName') # code above uses this to ID any existing windows
    MayaUI.window.setWindowTitle('Maya UI')
    MayaUI.window.show()
    
openWindow()
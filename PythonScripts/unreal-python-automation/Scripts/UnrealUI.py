import unreal
import sys
from functools import partial  # if you want to include args with UI method calls
from PySide2 import QtUiTools, QtWidgets



class UnrealWidget(QtWidgets.QWidget):
    """
    Create a default tool window.
    """
    # store ref to window to prevent garbage collection
    window = None

    def __init__(self, parent=None):
        """
        Import UI and connect components
        """
        super(UnrealWidget, self).__init__(parent)

        # load the created UI widget
        self.widgetPath = 'D:\\GameDevelopment\\Pipeline-Project\\msccavepipelineandtdproject24-RahulChandra99\\unreal-automation\\GUI\\'
        self.widget = QtUiTools.QUiLoader().load(self.widgetPath + 'unrealWidget.ui')  # path to PyQt .ui file

        # attach the widget to the instance of this class (aka self)
        self.widget.setParent(self)

        # find interactive elements of UI
        self.btn_rename = self.widget.findChild(QtWidgets.QPushButton, 'btn_rename')
        self.btn_export = self.widget.findChild(QtWidgets.QPushButton, 'btn_export')
        self.btn_import = self.widget.findChild(QtWidgets.QPushButton, 'btn_import')
        self.btn_close = self.widget.findChild(QtWidgets.QPushButton, 'btn_close')

        # assign clicked handler to buttons
        self.btn_rename.clicked.connect(self.renameAssets)
        self.btn_import.clicked.connect(self.importAssets)
        self.btn_export.clicked.connect(self.exportSelectedAssets)
        self.btn_close.clicked.connect(self.closewindow)

    """
    Your code goes here.
    """

    def renameAssets(self):
        # instances of unreal classes
        system_lib = unreal.SystemLibrary()
        editor_util = unreal.EditorUtilityLibrary()
        string_lib = unreal.StringLibrary()

        # get the selected assets
        selected_assets = editor_util.get_selected_asset_data()
        num_assets = len(selected_assets)
        replaced = 0

        unreal.log("Selected {} asssets".format(num_assets))

        search_pattern = "New"
        use_case = True
        replace_pattern = "Old"

        #loop over each asset and rename
        for asset_data in selected_assets:
            # Extract the Object from AssetData
            asset = asset_data.get_asset()
            asset_name = system_lib.get_object_name(asset)

            #check if the asset name contains the text to be replaced text
            if string_lib.contains(asset_name, search_pattern, use_case=use_case):
                search_case = unreal.SearchCase.CASE_SENSITIVE if use_case else unreal.SearchCase.IGNORE_CASE
                replaced_name = string_lib.replace(asset_name, search_pattern, replace_pattern, search_case=search_case)
                editor_util.rename_asset(asset, replaced_name)

                replaced += 1;
                unreal.log("Replaced {} with {}".format(asset_name, replaced_name))

            else:
                unreal.log("{} did not match the search pattern, was skipped".format(asset_name))

        unreal.log("Replaced {} of {} assets".format(replaced, num_assets))

    def exportSelectedAssets(self):
        """
        Export Selected Assets
        :return:
        """
        selectedAssets = unreal.EditorUtilityLibrary.get_selected_assets()
        for selectedAsset in selectedAssets:
            assetName = selectedAsset.get_name()

            exportTask = unreal.AssetExportTask()
            exportTask.automated = True
            exportTask.filename = 'D:\\' + assetName + '.fbx'
            exportTask.object = selectedAsset
            exportTask.options = unreal.FbxExportOption()
            exportTask.prompt = False

            fbxExporter = unreal.StaticMeshExporterFBX()
            exportTask.exporter = fbxExporter
            fbxExporter.run_asset_export_task(exportTask)

    def importAssets(self):
        """
        Import assets into project.
        """
        # list of files to import
        fileNames = [
            'D:\\abc.fbx',

        ]
        # create asset tools object
        assetTools = unreal.AssetToolsHelpers.get_asset_tools()
        # create asset import data object
        assetImportData = unreal.AutomatedAssetImportData()
        # set assetImportData attributes
        assetImportData.destination_path = '/Game/'
        assetImportData.filenames = fileNames
        assetImportData.replace_existing = True
        assetTools.import_assets_automated(assetImportData)

    def resizeEvent(self, event):
        """
        Called on automatically generated resize event
        """
        self.widget.resize(self.width(), self.height())

    def closewindow(self):
        """
        Close the window.
        """
        print('Closing the Window')
        self.destroy()


def openWindow():
    """
    Create tool window.
    """
    if QtWidgets.QApplication.instance():
        # Id any current instances of tool and destroy
        for win in (QtWidgets.QApplication.allWindows()):
            if 'toolWindow' in win.objectName():  # update this name to match name below
                win.destroy()
    else:
        QtWidgets.QApplication(sys.argv)

    # load UI into QApp instance
    UnrealWidget.window = UnrealWidget()
    UnrealWidget.window.show()
    UnrealWidget.window.setObjectName('toolWindow')  # update this with something unique to your tool
    UnrealWidget.window.setWindowTitle('UE Automation')
    unreal.parent_external_window_to_slate(UnrealWidget.window.winId())


openWindow()

import unreal

def listAssetsPath():
    EAL = unreal.EditorAssetLibrary

    assetPaths = EAL.list_assets('/Game')

    for assetPath in assetPaths :
        print(assetPath)
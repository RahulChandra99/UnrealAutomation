import unreal


@unreal.uclass()
class MyEditorUtility(unreal.GlobalEditorUtilityBase):
    pass


def selectAssets():
    selectedAssets = MyEditorUtility().get_selected_assets()
    for asset in selectedAssets:
        print("Asset: " + asset.get_name())


def selectActors():
    selectedActors = MyEditorUtility().get_selection_set()
    for actors in selectedActors:
        print("Actor: " + actors.get_name())


def createBPAssets():
    factory = unreal.BlueprintFactory()
    factory.set_editor_property("ParentClass", unreal.PlayerController)

    BPPath = "/Game/Test"
    assetTools = unreal.AssetToolsHelpers.get_asset_tools()
    myNewFile = assetTools.create_asset_with_dialog("CustomBP2", BPPath, None, factory)

    unreal.EditorAssetLibrary.save_loaded_asset(myNewFile)


def createProgressBarTasks():
    totalFrames = 1111111
    textDisplay = "My Bar"

    with unreal.ScopedSlowTask(totalFrames, textDisplay) as ST:
        ST.make_dialog(True)
        for i in range(totalFrames):
            if ST.should_cancel():
                break;
            unreal.log("Put your task here")
            ST.enter_progress_frame(1)


def createMultipleAssets():
    totalNumberOfBPs = 20
    textDisplay = "Creating Custom Assets"
    BPPath = "/Game/Test"
    BPName = "New_BP_%d"

    factory = unreal.BlueprintFactory()
    factory.set_editor_property("ParentClass",unreal.Pawn)
    assetTools = unreal.AssetToolsHelpers.get_asset_tools()


    with unreal.ScopedSlowTask(totalNumberOfBPs, textDisplay) as ST:
        ST.make_dialog(True)
        for i in range(totalNumberOfBPs):
            if ST.should_cancel():
                break;

            myNewFile = assetTools.create_asset(BPName%(i), BPPath,None,factory)
            unreal.EditorAssetLibrary.save_loaded_asset(myNewFile)

            ST.enter_progress_frame(1)


def createMultipleActors():
    actorsCount = 50
    textDisplay = "Creating actors in the level..."
    selectedAssets = MyEditorUtility().get_selected_assets()


    with unreal.ScopedSlowTask(actorsCount,textDisplay) as ST:
        ST.make_dialog(True)
        for x in range(actorsCount):
            if ST.should_cancel():
                break;

            if selectedAssets is None:
                unreal.log("Nothing is selected")
            else:
                unreal.EditorLevelLibrary.spawn_actor_from_object(selectedAssets[0],unreal.Vector(1.0+x+100,1.0+x+100,30.0), unreal.Rotator(0.0,0.0,10.0+x))
                unreal.log("New actors spawned")

            ST.enter_progress_frame(1)


createProgressBarTasks()
## BAKE TO NULLL v0.1###############################################################################
#                                                                                                  #
# THIS PYTHON SCRIPT BAKES AN OBJECTS TRANSFORMS TO A NULL OBJECT IN WORLD SPACE                   #
# THIS CAN BE VERY HELPFUL IF YOU JUST WANT TO GET THE TRANSFOMRS OF AN OBJECT                     #
# TO A SEPARATE OBJECT OR TO BAKE IT OUT AND DITCH THE TAGS AND HIERARCHY                          #
# This script is not meant to be used with cloner objects. It will only bake                       #  
# the selections objects global position.                                                          #
#                                                                                                  #
# USAGE: Select the objects you want to bake transfoms to and then run.                            #
#                                                                                                  #
#                                                                                                  #  
#                                                                                                  #
# Questions or bugs? please feel free to email me at andrez@aguayo.me                              #
# Created by Andrez Aguayo 2/16/16                                                                 # 
# Tested on Cineam R16                                                                             #   
# Email: andrez@aguayo.me                                                                          #
#                                                                                                  # 
####################################################################################################
import c4d
from c4d import gui


def selction_is_not_empty():
    """ This function is a boolean checker and will return if the users selection 
    is empty or not"""
    selected = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)
    if len(selected) == 0:
        return False
    else:
        return True
        
def set_priority(Mode, Value, obj):
    """ This funcion sets the priority of an expression """
    pd=obj[c4d.EXPRESSION_PRIORITY]
    pd.SetPriorityValue(c4d.PRIORITYVALUE_MODE, Mode)
    pd.SetPriorityValue(c4d.PRIORITYVALUE_PRIORITY, Value)
    obj[c4d.EXPRESSION_PRIORITY]=pd
    return

def select_list(list_of_objects):
    """ This funcion sets the selection to only the objects in a given list"""
    doc.SetActiveObject(list_of_objects[0],mode=c4d.SELECTION_NEW)
    if len(list_of_objects)>1:
        for obj in list_of_objects[1:]:
            doc.SetActiveObject(obj,mode=c4d.SELECTION_ADD)
            
def delete_objects_in_a_list(list_of_objects):
    """ This fuction deletes the objets in a given list from the c4d document"""
    for obj in list_of_objects:
        obj.Remove()

def create_ws_null_on_selected():
    """The fuciton loops through the selected c4d objects and creates a new Null at the 
    positon of each object"""
    selected = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN)# Get the selected objects
    WS_objects = []
    xTags = []
    for obj in selected:
        # Create a null and set set some perams 
        null = c4d.BaseObject(c4d.Onull)
        null[c4d.NULLOBJECT_ORIENTATION]=1
        null[c4d.NULLOBJECT_DISPLAY]=1
        null[c4d.NULLOBJECT_RADIUS]=150
        null[c4d.ID_BASEOBJECT_USECOLOR]=2
        null[c4d.ID_BASEOBJECT_COLOR] = c4d.Vector(0,0.5,1)
        null.SetName(obj.GetName() + "_WS")
        doc.InsertObject(null)
        WS_objects.append(null)
        xTag = null.MakeTag(1001149)# Create and Xpresso Tag
        xTags.append(xTag)
        set_priority(4,499, xTag)
        xMaster = xTag.GetNodeMaster()
        objectNode_Cube = xMaster.CreateNode(xMaster.GetRoot(), 
                                             c4d.ID_OPERATOR_OBJECT, 
                                             None, 320, 200)# Create Object Node
        objectNode_Null = xMaster.CreateNode(xMaster.GetRoot(), 
                                             c4d.ID_OPERATOR_OBJECT, 
                                             None, 455, 200)# Create Object Node
        objectNode_Cube[c4d.GV_OBJECT_OBJECT_ID]=obj # Connect the selected object to object nodes 
        objectNode_Null[c4d.GV_OBJECT_OBJECT_ID]=null # Connect the null object to object nodes 

        # Add ports in expresso and conect the Global Position, Globla Rotation, and Scale'
        mylist = [c4d.ID_BASEOBJECT_GLOBAL_POSITION, 
                  c4d.ID_BASEOBJECT_GLOBAL_ROTATION, 
                  c4d.ID_BASEOBJECT_REL_SCALE]
        for l in mylist:
            inA = objectNode_Null.AddPort(c4d.GV_PORT_INPUT, l)
            outA = objectNode_Cube.AddPort(c4d.GV_PORT_OUTPUT, l)
            outA.Connect(inA)
            
    c4d.EventAdd()
    return WS_objects,xTags

def bake_me():
    """ bake me funcion is heavly influenced by the bake script Breat Bays created.
    it will loop though the timeline and set a keyframe on all the selected objects
    """
    userStartTime=doc.GetMinTime().GetFrame(doc.GetFps())-1 #Not sure about the -1  but it works 
    userEndTime=doc.GetMaxTime().GetFrame(doc.GetFps())
    
    fps=doc.GetFps()
    
    # Build Current Frame time
    curentFrame=doc.GetTime().GetFrame(doc.GetFps())
    currentTime=doc.GetTime()
    currentTime.SetNumerator(curentFrame)
    currentTime.SetDenominator(fps)

    bakeStartTime=doc.GetTime()
    bakeStartTime.SetNumerator(userStartTime)
    bakeStartTime.SetDenominator(fps)
    
    doc.SetTime(bakeStartTime)
    currentFrame=doc.GetTime().GetFrame(fps)
    
    while(currentFrame <= userEndTime):
        c4d.StopAllThreads()
        c4d.CallCommand(12410)# Set Record(Key Frame)
        userStartTime=userStartTime+1
        bakeStartTime.SetNumerator(userStartTime)
        bakeStartTime.SetDenominator(fps)
        doc.SetTime(bakeStartTime)
        redraw=c4d.DrawViews(c4d.DA_STATICBREAK)
        c4d.EventAdd(c4d.EVENT_ANIMATE)
        if (redraw==True):
            currentFrame=doc.GetTime().GetFrame(fps)
    
    doc.SetTime(currentTime)
    redraw=c4d.DrawViews(c4d.DA_STATICBREAK)
    c4d.EventAdd(c4d.EVENT_ANIMATE)

    
def bake_to_null(): 
    """ This is the main logic funcion, it will bake a new null to the 
    global transforms of every selected object"""
    if selction_is_not_empty():
        nulls,xtags = create_ws_null_on_selected()
        select_list(nulls)
        bake_me()
        delete_objects_in_a_list(xtags)
        gui.MessageDialog("SUCCESS: Baked transforms to a null in world space! ")
    else: 
        gui.MessageDialog("NO OBJECT SELECTED \nTo Bake an object you must select an object(s) with transforms")
if __name__=='__main__':
    bake_to_null()
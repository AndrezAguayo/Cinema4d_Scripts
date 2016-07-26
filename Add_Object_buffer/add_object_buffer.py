## Add object buffer v0.1###########################################################################
#                                                                                                  #
# THIS PYTHON SCRIPT ADDS AN NEW OBJECT BUFFER ID FOR EVERY MATERIAL IN A SCENE TO                 #   
# EVERY OBJECT IT IS APPLYED TO. IT WILL ADD A NEW OBJECT BUFFER IN THE RENDER SETTINGS            #
# AND ADD A RENDER TAG AND ADD THE NEW ID. IF A RENDER TAG ALREADY IT WILL USE THE EXISTING TAG    #
#                                                                                                  #
#                                                                                                  #
# USAGE: Run Script                                                                                #
#                                                                                                  #
# Questions or Bugs? please feel free to email me at andrez@aguayo.me                              #
#                                                                                                  #  
#                                                                                                  #
# Created by Andrez Aguayo 1/07/16                                                                 # 
# Tested on Cinema R16 Physical Renderer                                                           #   
# Email: andrez@aguayo.me                                                                          #
#                                                                                                  # 
####################################################################################################

import c4d
from c4d import gui
#Welcome to the world of Python


def apply_obj_buff_from_materials(selection_type, bufferID):
    ### This Function adds a new buffer id to the render settings with
    ### the material of the object 
    ### selection_type --> int between 0 and 1,bufferID -->int
    
    if selection_type == 0:
        materials = doc.GetMaterials()
        
    elif selection_type == 1:
        materials = doc.GetActiveMaterials()
              
    else:
        gui.MessageDialog("Selection type Not specefied")
        return False
    
    ##print "this is the active material {0}".format(materials)
    
    rd = doc.GetActiveRenderData()          # Get the current renderdata
    
    for material in materials:
        
        materialName = material.GetName()
        
        # create a multipass object this materials
        vdepth=c4d.BaseList2D(c4d.Zmultipass)   
        vdepth.GetDataInstance()[c4d.MULTIPASSOBJECT_TYPE] = c4d.VPBUFFER_OBJECTBUFFER #Set type to 'Object Buffer'
        vdepth[c4d.MULTIPASSOBJECT_OBJECTBUFFER] = bufferID
        bufferID_name = "ObBuff_" + materialName + "_" + str(bufferID)
        vdepth.SetName(bufferID_name)
        rd.InsertMultipass(vdepth)              # Insert into Multipass list
        
        
        ## Collect all the objects that have that material
        objs = collect_all_objects_with_right_most_material(doc,material)
        #print"here are the objs {0}".format(objs)   
        for obj in objs:
            # check first to see if there already is a tag
            theTags = obj.GetTags()
            found = False
            for tag in theTags:
                if tag.CheckType(5637):
                    compositingTag = tag
                    found = True 
                    
                    COMPOSITINGTAG_ENABLECHN,COMPOSITINGTAG_IDCHN =  get_avaliable_buffer(compositingTag)  
                    compositingTag[COMPOSITINGTAG_ENABLECHN] = True
                    compositingTag[COMPOSITINGTAG_IDCHN] = bufferID
                    
                    break 
            
            
            if not found:        
                ## make a new compositing tag
                compositingTag = obj.MakeTag(5637)
                #tag.SetName("fdaf")
                compositingTag[c4d.COMPOSITINGTAG_ENABLECHN0] = True
                compositingTag[c4d.COMPOSITINGTAG_IDCHN0] = bufferID
                obj.InsertTag(compositingTag)
            
        ##5637 = Compositing tag type id 
        bufferID += 1   
            
            
    ## in render settings add a new object buffer 


def get_avaliable_buffer(compositingTag):
    """ This is my way of finding an empty id channel in the compositing tag,
    incase there is already a tag it will find the next availabe compositing channel"""
    if not compositingTag[c4d.COMPOSITINGTAG_ENABLECHN0]:
        return c4d.COMPOSITINGTAG_ENABLECHN0,c4d.COMPOSITINGTAG_IDCHN0
    if not compositingTag[c4d.COMPOSITINGTAG_ENABLECHN1]:
        return c4d.COMPOSITINGTAG_ENABLECHN1,c4d.COMPOSITINGTAG_IDCHN1
    if not compositingTag[c4d.COMPOSITINGTAG_ENABLECHN2]:
        return c4d.COMPOSITINGTAG_ENABLECHN2,c4d.COMPOSITINGTAG_IDCHN2
    if not compositingTag[c4d.COMPOSITINGTAG_ENABLECHN3]:
        return c4d.COMPOSITINGTAG_ENABLECHN3,c4d.COMPOSITINGTAG_IDCHN3
    if not compositingTag[c4d.COMPOSITINGTAG_ENABLECHN4]:
        return c4d.COMPOSITINGTAG_ENABLECHN4,c4d.COMPOSITINGTAG_IDCHN4
    if not compositingTag[c4d.COMPOSITINGTAG_ENABLECHN5]:
        return c4d.COMPOSITINGTAG_ENABLECHN5,c4d.COMPOSITINGTAG_IDCHN5
    if not compositingTag[c4d.COMPOSITINGTAG_ENABLECHN6]:
        return c4d.COMPOSITINGTAG_ENABLECHN6,c4d.COMPOSITINGTAG_IDCHN6
    if not compositingTag[c4d.COMPOSITINGTAG_ENABLECHN7]:
        return c4d.COMPOSITINGTAG_ENABLECHN7,c4d.COMPOSITINGTAG_IDCHN7
    if not compositingTag[c4d.COMPOSITINGTAG_ENABLECHN8]:
        return c4d.COMPOSITINGTAG_ENABLECHN8,c4d.COMPOSITINGTAG_IDCHN8
    if not compositingTag[c4d.COMPOSITINGTAG_ENABLECHN9]:
        return c4d.COMPOSITINGTAG_ENABLECHN9,c4d.COMPOSITINGTAG_IDCHN9
    if not compositingTag[c4d.COMPOSITINGTAG_ENABLECHN10]:
        return c4d.COMPOSITINGTAG_ENABLECHN10,c4d.COMPOSITINGTAG_IDCHN10
    if not compositingTag[c4d.COMPOSITINGTAG_ENABLECHN11]:
        return c4d.COMPOSITINGTAG_ENABLECHN11,c4d.COMPOSITINGTAG_IDCHN11

    return False


def walk(op):
    if not op: return
    elif op.GetDown():
        return op.GetDown()
    while op.GetUp() and not op.GetNext():
        op = op.GetUp()
    return op.GetNext()

def selectAllPolygonObjects(doc):
    op  = doc.GetFirstObject()
    #print op
    while op:
        if op.CheckType(c4d.Opolygon):
            op.SetBit(c4d.BIT_ACTIVE)
        else:
            op.DelBit(c4d.BIT_ACTIVE)
        op  = walk(op)
        
def collect_all_objects_with_material(doc,material):
    op  = doc.GetFirstObject()
    objects_with_materials=[]
    while op:     
        if object_has_materal(op,material):
            #op.SetBit(c4d.BIT_ACTIVE)
            objects_with_materials.append(op)
        #else:
        #    op.DelBit(c4d.BIT_ACTIVE)
        op  = walk(op)
    return objects_with_materials  
        
def object_has_materal(obj, material):
    ## function returnes a bool value if the object has the material
    #materials = TextureTag.GetMaterial()
    theTags = obj.GetTags()
    for tag in theTags:
        if tag.CheckType(5616):## 5616 material type 
            if tag[c4d.TEXTURETAG_MATERIAL]==material:
                return True
    return False

def collect_all_objects_with_right_most_material(doc,material):
    op  = doc.GetFirstObject()
    objects_with_materials=[]
    while op:     
        if object_has_materal_as_right_most_tag(op,material):
            #op.SetBit(c4d.BIT_ACTIVE)
            objects_with_materials.append(op)
        #else:
        #    op.DelBit(c4d.BIT_ACTIVE)
        op  = walk(op)
    return objects_with_materials  

            
def object_has_materal_as_right_most_tag(obj, material):
    ## function returnes a bool value if the object has the material
    #materials = TextureTag.GetMaterial()
    theTags = obj.GetTags()
    materialList = []
    for tag in theTags:
        if tag.CheckType(5616):## 5616 material type 
            materialList.append(tag)
    
    if len(materialList) == 0:
        return False 
           
    if materialList[-1][c4d.TEXTURETAG_MATERIAL]==material:
        return True
    return False




# Unique ID numbers for each of the GUI elements
TXT_IND_ID = 1000225
EDT_NUMB_ID = 1000226
RDO_GRP = 1000227
BTN_SET = 1000228
BTN_CNCL = 1000229
GROUP_OPTIONS = 1000230
RDO_GRP_TXT = 1000231

# Clip Board Dialog 
class add_obj_buffer_Dialog(gui.GeDialog):
    
    def CreateLayout(self):
        ########## 
        self.GroupBegin(GROUP_OPTIONS, c4d.BFH_SCALEFIT, 2, 1)
        ## self.ok = True
        self.SetTitle('DK Add Object Id Buffer')

        ## Add Starting Index ID text and edit number dialog   
        self.AddStaticText(TXT_IND_ID, c4d.BFH_LEFT)
        self.SetString(TXT_IND_ID, "(Starting) Index ID")      
        self.AddEditNumberArrows(EDT_NUMB_ID, c4d.BFH_LEFT, initw = 100)
        self.SetInt32(EDT_NUMB_ID,100) 
                
        # Add Radio Group elements for materal selection options
        ## Add Starting Index ID text and edit number dialog   
        self.AddStaticText(RDO_GRP_TXT, c4d.BFH_LEFT)
        self.SetString(RDO_GRP_TXT, "Material Selection") 
        self.AddRadioGroup(RDO_GRP, c4d.BFH_LEFT, 1)
        self.AddChild(RDO_GRP, 0, 'All Materaials')
        self.AddChild(RDO_GRP, 1, 'Selected Materials')
        self.SetInt32(RDO_GRP,0)
                
        #Add Set Current and Copy Buttons       
        self.AddButton(BTN_SET, c4d.BFH_RIGHT,initw=190, name='Set')
        self.AddButton(BTN_CNCL, c4d.BFH_LEFT,initw=190, name='Cancel')

        self.GroupEnd()        

        return True    # not sure if I need this too 
 
    # React to user's input:
    def Command(self, id, msg):
        if id==BTN_SET:
            selection_type = self.GetInt32(RDO_GRP) 
            print "this is the selection type {0}".format(selection_type)
            bufferID = self.GetInt32(EDT_NUMB_ID) 
            print "this is the buffer ID {0}".format(bufferID)
            apply_obj_buff_from_materials(selection_type, bufferID)
            c4d.EventAdd()
            self.Close()
            c4d.EventAdd()
        elif id==BTN_CNCL:
            self.Close()
        
        
        return True


def main():
    # Open the options dialogue to let users choose their options.
    dlg = add_obj_buffer_Dialog()
    #dog =  dir(dlg)

    dlg.Open(c4d.DLG_TYPE_MODAL, defaultw=75, defaulth=20)
 
        
if __name__=='__main__':
    main()    
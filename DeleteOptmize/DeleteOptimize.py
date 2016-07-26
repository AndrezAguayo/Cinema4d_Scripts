##################################################################################
# Delete + Optimized v1.0                                                        #
#                                                                                #
# This is script to delete the vertices of the                                   #
# deleted edge when they have zero length                                        #
#                                                                                #
# All it does is check if you are on polygon mode(or face mode as I call it)     #
# If so and you are going to delete a polygon then it will run the optimize      #
# afterwords.                                                                    #
#                                                                                #
## Contact me with any request, bugs or just want to chat                        #
## Created by Andrez Aguayo                                                      #
## Email:Andrez@aguayo.me                                                        #
## www.andrezaguayo.com                                                          #
## 9/12/2015                                                                     # 
##################################################################################
import c4d

def delete_optmize():
   
    ## make sure you are on Poly Mode
    if c4d.IsCommandEnabled(12187): #Polygons 
        ## Then Delete it 
        c4d.CallCommand(12109) # Delete
        ## Then Optimize 
        c4d.CallCommand(14039, 14039) # Optimize...
        
        
    ## if not then just do a normal delete  
    else: 
        c4d.CallCommand(12109) # Delete
        
    c4d.EventAdd()

if __name__=='__main__':
    delete_optmize()


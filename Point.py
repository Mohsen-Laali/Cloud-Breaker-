
'''
Created on 20/06/2012

@author: E86574
'''


class Point():
    '''
    classdocs
    '''
    x=None
    y=None
    z=None
    line=None
    def __init__(self,line = None):
        '''
        Constructor
        '''
        if ( line != None):
            self.line = line
            line = line.replace("\n","")
            coordinates = line.split("\t")
            self.x= float(coordinates[0])
            self.y= float(coordinates[1])
            self.z= float(coordinates[2])
        else :
            self.x = 0
            self.y = 0
            self.z = 0
        
        
        

        
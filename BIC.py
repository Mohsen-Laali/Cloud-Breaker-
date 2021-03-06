import math

class Point():
    '''
    this class keep the point 
    '''
    x=None
    y=None
    z=None
    d= None
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
            if len(coordinates) > 3 :
                self.d = int(coordinates[3])
        else :
            self.x = float(0)
            self.y = float(0)
            self.z = float(0)
            self.d = int(0)

class IO(object):
    _fileName = str()
    _readAndWriteStream = None 
    _minimumZValue = None
    _maximumZValue = None
    _minmumDensity = None
    _maxDensity = None
    _totalDensity = int() 
    _totalZValue = float()
    _numberOfPoins = 0
    _isFileIsOpen = False 
    _autoOpenClose = None
    _distanceFromCenter = None 
    
    def __init__(self,fileName,distanceFromCenter,autoOpenClose=True):
        self._autoOpenClose = autoOpenClose 
        self._fileName = fileName
        self._distanceFromCenter = distanceFromCenter
        if not autoOpenClose :
            self._readAndWriteStream = open(fileName,"w+")
            self._isFileIsOpen = True
        else :
            self._readAndWriteStream = open(fileName ,'w+')
            self._readAndWriteStream.close()
        
    def isFileIsOpen(self):
        return self._isFileIsOpen
        
    def readFromFile(self):
        self.openFileForRead()
        for line in self._readAndWriteStream :
            yield line 
            
    def writeToFile(self,line , z = None):
        if self._autoOpenClose :
            self.reOpenFile()
        self._readAndWriteStream.write(line)
        if self._autoOpenClose:
            self.colseFile()
        if z != None:
            if(self._minimumZValue == None):
                self._minimumZValue = z
            elif(self._minimumZValue > z ):
                self._minimumZValue = z 
                
    def reOpenFile(self):
        if not self._isFileIsOpen :
            self._readAndWriteStream = open(self._fileName,'a+')
            self._isFileIsOpen = True
            
    def excludePointWithZValue(self,zValue,mZValue):
        finalFileName = self._fileName.split(".")[0] + "ZzZz.asc"
        fileToWrite = open(finalFileName,"w")
        firstTime = True
        if mZValue == None:
            mZValue = self._minimumZValue
        pastMinumZValue = self._minimumZValue
        for line in self.readFromFile():
            point = Point(line)
            if ((point.z <=(pastMinumZValue + zValue)) and (point.z >= mZValue)):
                self._numberOfPoins += 1
                self._totalZValue +=point.z
                self._totalDensity += point.d
                if(firstTime):
                    firstTime = False
                    self._minimumZValue = point.z
                    self._maximumZValue = point.z
                    if point.d :
                        self._maxDensity = point.d
                        self._minmumDensity = point.d
                else:
                    if point.z > self._maximumZValue:
                        self._maximumZValue = point.z
                    if point.z < self._minimumZValue:
                        self._minimumZValue = point.z
                    if point.d :
                        if point.d > self._maxDensity :
                            self._maxDensity = point.d
                        if point.d < self._minmumDensity :
                            self._minmumDensity = point.d
                fileToWrite.write(line)
        fileToWrite.close()
        self.colseFile()
        os.remove(self._fileName)
        
    def colseFile(self):
        if(self._isFileIsOpen):
            self._readAndWriteStream.close()
            self._isFileIsOpen = False
            
    def openFileForRead(self):
        if(not self._isFileIsOpen):
            self._readAndWriteStream = open(self._fileName,"r+")
            self._isFileIsOpen = True 
            
    def minmumMaximumAndAverage(self):
        if(self._numberOfPoins != 0):
            average = self._totalZValue/float(self._numberOfPoins)
            averageDensity = self._totalDensity/float(self._numberOfPoins)
        else : average = 'NP      '
        if(self._maximumZValue == None):
            self._maximumZValue = 'NP      '
        if(self._minimumZValue == None): 
            self._minimumZValue = 'NP      '
        if self._minmumDensity :
            return [self._minimumZValue,self._maximumZValue,self._numberOfPoins,
                    average,self._minmumDensity,self._maxDensity,averageDensity,
                    self._distanceFromCenter]
        else :
            return [self._minimumZValue,self._maximumZValue,self._numberOfPoins,
                    average,self._distanceFromCenter]
        
    def getFileName(self):
        return self._fileName
        
import os
import glob
class BIC(object):
    '''
    classdocs
    '''
    
    def __init__(self ):
        '''
        Constructor
        '''
         
    def _findBorder(self,fileName):
        fileReader = open(fileName, "r")
        topLeft = None
        downRight = None
        firstTime = True
        
        for line in fileReader:
            if (firstTime):
                topLeft = Point(line)
                downRight = Point(line)
                firstTime = False
            else:
                point = Point(line)
                if (topLeft.x > point.x):
                    topLeft.x = point.x
                if (downRight.x < point.x):
                    downRight.x = point.x
                if (topLeft.y < point.y):
                    topLeft.y = point.y
                if (downRight.y > point.y):
                    downRight.y = point.y
                    
        return [topLeft,downRight]
    def _initialIO(self,topLeftPoint,downRightPoint,sizeOfBox,folderAddress,centerOfPlot,
                   largeNumberOfspilitting=False,writCloadSizeInfo=True):
        cloadSizeInfoFileAddress = os.path.join(folderAddress,'CloudSizeInfo.txt')
        if writCloadSizeInfo:
            cloadSizeInfoFileHandler = open(cloadSizeInfoFileAddress,'w+')
            
        tlp = Point()
        tlp.x = topLeftPoint.x
        tlp.y = topLeftPoint.y
        minimumX = tlp.x
        iOMatrix = []
        i = 0
        drp= Point()
        centerPoint = Point()
        cloadSizeInfoFileHandler.write('File_Name Top_Left_x Top_Left_y Down_Right_x Down_Right_y Center_x Center_y Distance_From_Center'+os.linesep)
        while(tlp.y > downRightPoint.y):
            iOLine = []
            tlp.x = minimumX
            while (tlp.x < downRightPoint.x):
                i += 1
                distanceToEdge  = tlp.y -downRightPoint.y
                widthOfBox = topLeftPoint.y - downRightPoint.y
                # 180 rotate the image 
                mirrorY = tlp.y - 2*distanceToEdge + widthOfBox
                drp.x = tlp.x+sizeOfBox
                drp.y = mirrorY+sizeOfBox
                centerPoint.x = tlp.x+ sizeOfBox/float(2)
                centerPoint.y = mirrorY- sizeOfBox/float(2)
                distanceFromCenter = math.sqrt((centerPoint.x - centerOfPlot.x)**2 + (centerPoint.y - centerOfPlot.y)**2)
                cloadSizeInfoFileHandler.write(str(i)+'. '+str(tlp.x)+' '+str(mirrorY )+' '
                                               +str(drp.x)+' '+str(drp.y)+' '
                                               +str(centerPoint.x)+' '+str(centerPoint.y)+' '+str(distanceFromCenter)
                                               +os.linesep)
                fileAddress = os.path.join( folderAddress , str(i)+".asc")
                io = IO(fileAddress,distanceFromCenter,largeNumberOfspilitting)
                iOLine.append(io)
                tlp.x = tlp.x +sizeOfBox
            tlp.y=tlp.y- sizeOfBox
            iOMatrix.append(iOLine)
        cloadSizeInfoFileHandler.close()
        return iOMatrix 
    
    def _initialIOForBoxInBox(self,topLeftBorder, downRightBorder,
                              topLeftBox,downRightBox, 
                              sizeOfBox, folderAddress):
        iOList = []
        numberOFBox = 0
        
        if abs(topLeftBox.x - topLeftBorder.x) > abs(topLeftBorder.y - topLeftBox.y):
            numberOFBox = int(math.ceil((abs(topLeftBox.x - topLeftBorder.x))/sizeOfBox))
        else :
            numberOFBox = int(math.ceil((abs(topLeftBorder.y - topLeftBox.y))/sizeOfBox))
        boxNumber = 0
        #while boxNumber <= numberOFBox:
        for boxNumber in range(1, numberOFBox+1):
            boxNumber +=1 
            fileAddress = os.path.join( folderAddress , str(boxNumber)+".asc")
            io = IO(fileAddress)
            iOList.append(io)
        return iOList
            
        
    def processData(self,folderAddress,sizeOfBox = 1 , zValue = 2 ,mZValue= None, 
                    centerOfPlot=None,largeNumberOfspilitting = False,plotInfo = 'plotInfo.txt'):
        #make result folder 
        
        os.chdir(folderAddress)
        for fileName in glob.glob('*.asc'):
            outPutFolder = folderAddress+os.sep+fileName.split('.')[0]
            fileName= folderAddress+os.sep+fileName
                        
            print('##########################################################################')
            print('start process of ' + fileName)
            if not os.path.exists(outPutFolder): os.makedirs(outPutFolder)
            outPutFolder += os.sep
            plotInfoFileHandler = open(os.path.join(outPutFolder,plotInfo),'w+') 
            
            topLeftPoint, downRightPoint = self._findBorder(fileName)
            print('find the border is done')
            if  centerOfPlot == None:
                centerOfPlot = Point()
                centerOfPlot.x = topLeftPoint.x +(downRightPoint.x - topLeftPoint.x)/2
                centerOfPlot.y = downRightPoint.y + (topLeftPoint.y - downRightPoint.y )/2
            print('center of plot is X:'+str(centerOfPlot.x)+ ' Y:'+str(centerOfPlot.y))  
            
            iOMatrix = self._initialIO(topLeftPoint, downRightPoint, sizeOfBox,outPutFolder, centerOfPlot,largeNumberOfspilitting)
            print ('initial IO is done')
            
            fileReader = open(fileName,'r')
            for line in fileReader:
                point = Point(line)
                io = iOMatrix[(int((point.y - downRightPoint.y)/sizeOfBox))]\
                [(int((point.x - topLeftPoint.x)/sizeOfBox))] 
                io.writeToFile(line ,point.z)
            print ('writing point to disk is done')   
            plotInfoFileHandler.write('File_Name Point_count Maximum_Z Minimum_Z Average_Z '
                                      +'Maximum_Density Minimum_Density Average_Density Distance_From_Center'+os.linesep )
            for iOLine in iOMatrix :
                for io in iOLine :
                    io.colseFile()
                    io.excludePointWithZValue(zValue,mZValue)  
                    cloadInfo = io.minmumMaximumAndAverage()
                    if len(cloadInfo) == 5:   
                        minimum,maximum,numberOfPoints,average,distanceFromCenter = cloadInfo
                        plotInfoFileHandler.write(io.getFileName().split(os.sep).pop().split('.')[0]
                                        +' '+str(numberOfPoints)+' '+str(maximum)+
                                        str(distanceFromCenter)+os.linesep)
                    else:
                        minimum,maximum,numberOfPoints,average,minimumD,maximumD,averageD,distanceFromCenter = cloadInfo
                        plotInfoFileHandler.write(io.getFileName().split(os.sep).pop().split('.')[0]
                                        +' '+str(numberOfPoints)+' '+str(maximum)+' '
                                        +str(minimum)+' '+str(average)+' '+
                                        str(maximumD)+' '+str(minimumD)+' '+
                                        str(averageD)+' '+str(distanceFromCenter)+os.linesep)
            print ('exclude z more than specific number is done')
            print ('finish process of '+ fileName)
            print('##########################################################################')
            plotInfoFileHandler.close()
        print('All fileName is processed :)')
      
    
    def breakBoxInsideBox(self,folderAddress,middelPoint1,middelPoint2,sizeOfBox):
        topLeft,downRight =self.topLeftDownRight(middelPoint1,middelPoint2)
        centerPoint = Point()
        width = abs(downRight.x - topLeft.x)
        length = abs(topLeft.y - downRight.y)
        centerPoint.x = topLeft.x + width/2 
        centerPoint.y = downRight.y + length/2

        os.chdir(folderAddress)
        for fileName in glob.glob('*.asc'):
            outPutFolder = folderAddress+os.sep+fileName.split('.')[0]
            fileName= folderAddress+os.sep+fileName
            print('##########################################################################')
            print('start process of ' + fileName)
            if not os.path.exists(outPutFolder): os.makedirs(outPutFolder)
            outPutFolder += os.sep
            
            topLeftBorder , downRightBorder = self._findBorder(fileName)
            print ('top left  x:'+str(topLeft.x) + ' y:'+str(topLeft.y))
            print ('down right  x:'+str(downRight.x) + ' y:'+str(downRight.y))
            ioList = self._initialIOForBoxInBox(topLeftBorder, downRightBorder,
                                                  topLeft, downRight, 
                                                  sizeOfBox,outPutFolder)
            sizeOfIO = len(ioList)
            print (sizeOfBox)
            fileReader = open(fileName,'r')
            for line in fileReader:
                point = Point(line)
                index = 0
                while index < sizeOfIO-1 :
                    if (point.x > (topLeft.x- (index+1)*sizeOfBox) and
                        point.y < (topLeft.y + (index+1)*sizeOfBox) and
                        point.x < (downRight.x+(index+1) *sizeOfBox) and
                        point.y > (downRight.y - (index+1)*sizeOfBox)):
                        break
                    index +=1
                #print('last index '+str(index))
                io = ioList[index]
                io.writeToFile(line ,point.z)
                
            for io in ioList :
                io.colseFile()
            print ('finish process of '+ fileName)
            print('##########################################################################')

    def topLeftDownRight(self,middelPoint1,middelPoint2):
        topLeft = Point()
        downRight = Point()
        if middelPoint1.x < middelPoint2.x :
            topLeft.x = middelPoint1.x
            downRight.x = middelPoint2.x
        else :
            topLeft.x = middelPoint2.x
            downRight.x = middelPoint1.x
        if middelPoint1.y > middelPoint2.y:
            topLeft.y = middelPoint1.y
            downRight.y = middelPoint2.y
        else :
            topLeft.y = middelPoint2.y
            downRight.y = middelPoint1.y
        
        return topLeft,downRight
        
    def findMinumZValue(self,fileHandler):
        minmuZ = None 
        # initial z value 
        for line in fileHandler:
            point = Point(line)
            minmuZ = point.z
            break 
        # find minumZVlue
        for line in fileHandler:
            point = Point(line)
            if point.z< minmuZ :
                minmuZ = point.z 
        return minmuZ 
        
    def exludeLessThanZ(self,folderAddress,zValue):
        outPutFolder = folderAddress+os.sep+'outPut'
        if not os.path.exists(outPutFolder): os.makedirs(outPutFolder)
        os.chdir(folderAddress)
        for fileName in glob.glob('*.asc'):
            fileAddress= folderAddress+os.sep+fileName
            outPutfile = os.path.join(outPutFolder,fileName)
            print('##########################################################################')
            print('start process of ' + fileName)
            outPutFolder += os.sep
            fileHandler = open(fileAddress,'r')
            minumZValue= self.findMinumZValue(fileHandler)
            print ('minimum z valued is found')
            print ('minimum z value is '+str(minumZValue))
            outPutFileHandler = open(outPutfile,'w')
            # reset fileName handler to read from beginning of fileName 
            fileHandler.seek(0)
            for line in fileHandler:
                point = Point(line)
                if (point.z < (minumZValue + zValue)):
                    outPutFileHandler.write(point.line)
            outPutFileHandler.close()
            fileHandler.close()
            print ('exclude z more than specific number is done')
            print ('finish process of '+ fileName)
            print('##########################################################################')
        print ('All file is processed')
        
    def cutBetweenTwoZValue(self,folderAddress,firstZValue,secondZValue):
        outPutFolder = folderAddress+os.sep+'outPut'
        smallZ,bigZ = [firstZValue,secondZValue] if firstZValue<secondZValue \
        else [secondZValue,firstZValue]
        if not os.path.exists(outPutFolder): os.makedirs(outPutFolder)
        os.chdir(folderAddress)
        for fileName in glob.glob('*.asc'):
            fileAddress= folderAddress+os.sep+fileName
            outPutfile = os.path.join(outPutFolder,fileName)
            print('##########################################################################')
            print('start process of ' + fileName)
            outPutFolder += os.sep
            fileHandler = open(fileAddress,'r')
            outPutFileHandler = open(outPutfile,'w')
            for line in fileHandler:
                point = Point(line)
                if point.z > smallZ and point.z < bigZ:
                    outPutFileHandler.write(line)
            outPutFileHandler.close()
            fileHandler.close()
            print ('exclude z more than specific number is done')
            print ('finish process of '+ fileName)
            print('##########################################################################')
        print ('All files are processed')

    def whereIsPoint(self,firstPoint,secondPoint,point):
        leftFormula = 0
        rightFormula = 0
        if firstPoint.x - secondPoint.x == 0 :
            leftFormula = firstPoint.x
            rightFormula = point.x 
        else :
            k = (firstPoint.y - secondPoint.y)/(firstPoint.x -secondPoint.x)
            rightFormula = point.y
            leftFormula =  point.x * k - k * firstPoint.x + firstPoint.y
        if rightFormula<leftFormula:
            return 1
        elif rightFormula > leftFormula:
            return -1
        else :
            return 0
    
    def excluder(self,fileAddress,*points):
        # check point is in valid order
        numberOfPoints =len(points)
        whatSide = []
        for i in range(0,numberOfPoints):
            j = (i+1)% numberOfPoints
            side = -2
            for n in range(1,numberOfPoints-1):
                m = (j+n)%numberOfPoints
                newSide =self.whereIsPoint(points[i], points[j], points[m])
                if(side != -2 and newSide != side):
                    print ("there is an error in your points ")
                    return
                side = newSide
            whatSide.append(side)
        
        fileHandler = open(fileAddress,'r')
        outPutAddress= fileAddress.split('.')[0]+'_result.asc'
        outPutFileHandler = open(outPutAddress,'w')
        for line in fileHandler:
            point = Point(line)
            isInside = True
            for i in range(0,numberOfPoints):
                j= (i+1)%numberOfPoints
                side = self.whereIsPoint(points[i], points[j], point)
                if side != whatSide[i]:
                    isInside= False
                    break 
            if not isInside :
                outPutFileHandler.write(line)
                
        outPutFileHandler.flush()
        outPutFileHandler.close()
        fileHandler.close()
            
            
if __name__ == '__main__':
##    #put your folder address here 
##    folderAddress = r"C:\TLS_Scans_2013_11_14\FinalRawProduct(10m)\P1\NONVEGHEIGHT"
##    #fileAddress = r"D:\My Backups\Dropbox\My Uni\My Courses\IWS\Cload_Breaks\plot4scan2_raw.asc"
##    #put z value here 
##    
##    zValue = float(1.0)
##    largeNumberOfspilitting = True
##    #put the size of box here 
##    sizeOfBox = float(0.5)
##    mZValue = None 
##    topLeftPoint = Point()
##    bottomRightPoint = Point()
##    topLeftPoint.x = 98.93
##    topLeftPoint.y = 101.16
##    bottomRightPoint.x = 101.03
##    bottomRightPoint.y = 99.21
##    
##    distanceFromTopLeftx=(topLeftPoint.x-bottomRightPoint.x)/2.0
##    distanceFromBottomRighty=(bottomRightPoint.y-topLeftPoint.y)/2.0
##    centerOfPlot=Point()
##    
##    centerOfPlot.x=(distanceFromTopLeftx+topLeftPoint.x)
##    centerOfPlot.y=(distanceFromBottomRighty+bottomRightPoint.y)
##    
###     centerOfPlot.x =  10
###     centerOfPlot.y = 10
##    centerOfPlot = None
##    bic = BIC()
##    bic.processData(folderAddress,sizeOfBox,zValue,mZValue,centerOfPlot,
##                    largeNumberOfspilitting)
##########################################################################
##    folderAddress = r"C:\TLS_Scans_2013_11_14\FinalRawProduct(10m)\P1\VEGHEIGHT"
##    #fileAddress = r"D:\My Backups\Dropbox\My Uni\My Courses\IWS\Cload_Breaks\plot4scan2_raw.asc"
##    #put z value here 
##    
##    zValue = float(1.0)
##    largeNumberOfspilitting = True
##    #put the size of box here 
##    sizeOfBox = float(0.5)
##    mZValue = 0.02 
##    topLeftPoint = Point()
##    bottomRightPoint = Point()
##    topLeftPoint.x = 98.93
##    topLeftPoint.y = 101.16
##    bottomRightPoint.x = 101.03
##    bottomRightPoint.y = 99.21
##    
##    distanceFromTopLeftx=(topLeftPoint.x-bottomRightPoint.x)/2.0
##    distanceFromBottomRighty=(bottomRightPoint.y-topLeftPoint.y)/2.0
##    centerOfPlot=Point()
##    
##    centerOfPlot.x=(distanceFromTopLeftx+topLeftPoint.x)
##    centerOfPlot.y=(distanceFromBottomRighty+bottomRightPoint.y)
##    
###     centerOfPlot.x =  10
###     centerOfPlot.y = 10
##    centerOfPlot = None
##    bic = BIC()
##    bic.processData(folderAddress,sizeOfBox,zValue,mZValue,centerOfPlot,
##                    largeNumberOfspilitting)

##########################################################################
##    folderAddress = r"C:\TLS_Scans_2013_11_14\FinalRawProduct(10m)\P2\NONVEGHEIGHT"
##    #fileAddress = r"D:\My Backups\Dropbox\My Uni\My Courses\IWS\Cload_Breaks\plot4scan2_raw.asc"
##    #put z value here 
##    
##    zValue = float(1.0)
##    largeNumberOfspilitting = True
##    #put the size of box here 
##    sizeOfBox = float(0.5)
##    mZValue = None 
##    topLeftPoint = Point()
##    bottomRightPoint = Point()
##    topLeftPoint.x = 99.19
##    topLeftPoint.y = 100.93
##    bottomRightPoint.x = 100.99
##    bottomRightPoint.y = 99.13
##    
##    distanceFromTopLeftx=(topLeftPoint.x-bottomRightPoint.x)/2.0
##    distanceFromBottomRighty=(bottomRightPoint.y-topLeftPoint.y)/2.0
##    centerOfPlot=Point()
##    
##    centerOfPlot.x=(distanceFromTopLeftx+topLeftPoint.x)
##    centerOfPlot.y=(distanceFromBottomRighty+bottomRightPoint.y)
##    
###     centerOfPlot.x =  10
###     centerOfPlot.y = 10
##    centerOfPlot = None
##    bic = BIC()
##    bic.processData(folderAddress,sizeOfBox,zValue,mZValue,centerOfPlot,
##                    largeNumberOfspilitting)
############################################################################
##    folderAddress = r"C:\TLS_Scans_2013_11_14\FinalRawProduct(10m)\P2\VEGHEIGHT"
##    #fileAddress = r"D:\My Backups\Dropbox\My Uni\My Courses\IWS\Cload_Breaks\plot4scan2_raw.asc"
##    #put z value here 
##    
##    zValue = float(1.0)
##    largeNumberOfspilitting = True
##    #put the size of box here 
##    sizeOfBox = float(0.5)
##    mZValue = 0.02 
##    topLeftPoint = Point()
##    bottomRightPoint = Point()
##    topLeftPoint.x = 99.19
##    topLeftPoint.y = 100.93
##    bottomRightPoint.x = 100.99
##    bottomRightPoint.y = 99.13
##    
##    distanceFromTopLeftx=(topLeftPoint.x-bottomRightPoint.x)/2.0
##    distanceFromBottomRighty=(bottomRightPoint.y-topLeftPoint.y)/2.0
##    centerOfPlot=Point()
##    
##    centerOfPlot.x=(distanceFromTopLeftx+topLeftPoint.x)
##    centerOfPlot.y=(distanceFromBottomRighty+bottomRightPoint.y)
##    
###     centerOfPlot.x =  10
###     centerOfPlot.y = 10
##    centerOfPlot = None
##    bic = BIC()
##    bic.processData(folderAddress,sizeOfBox,zValue,mZValue,centerOfPlot,
##                    largeNumberOfspilitting)
##########################################################################
    folderAddress = r"C:\TLS-data\2012_05_W2\RawASCII\Shifted\P2_Shifted_W2\Voxels"
    #fileAddress = r"D:\My Backups\Dropbox\My Uni\My Courses\IWS\Cload_Breaks\plot4scan2_raw.asc"
    #put z value here 
    
    zValue = float(1.0)
    largeNumberOfspilitting = True
    #put the size of box here 
    sizeOfBox = float(0.5)
    mZValue = 0.05 
    topLeftPoint = Point()
    bottomRightPoint = Point()
    topLeftPoint.x = 99.19
    topLeftPoint.y = 100.93
    bottomRightPoint.x = 100.99
    bottomRightPoint.y = 99.13
    
    distanceFromTopLeftx=(topLeftPoint.x-bottomRightPoint.x)/2.0
    distanceFromBottomRighty=(bottomRightPoint.y-topLeftPoint.y)/2.0
    centerOfPlot=Point()
    
    centerOfPlot.x=(distanceFromTopLeftx+topLeftPoint.x)
    centerOfPlot.y=(distanceFromBottomRighty+bottomRightPoint.y)
    
#     centerOfPlot.x =  10
#     centerOfPlot.y = 10
    centerOfPlot = None
    bic = BIC()
    bic.processData(folderAddress,sizeOfBox,zValue,mZValue,centerOfPlot,
                    largeNumberOfspilitting)

##########################################################################
##    folderAddress = r"C:\TLS_Scans_2013_11_14\P320140327\P3\VEGHEIGHT"
##    #fileAddress = r"D:\My Backups\Dropbox\My Uni\My Courses\IWS\Cload_Breaks\plot4scan2_raw.asc"
##    #put z value here 
##    
##    zValue = float(1.0)
##    largeNumberOfspilitting = True
##    #put the size of box here 
##    sizeOfBox = float(0.4999)
##    mZValue = 0.02 
##    topLeftPoint = Point()
##    bottomRightPoint = Point()
##    topLeftPoint.x = 98.98
##    topLeftPoint.y = 101.00
##    bottomRightPoint.x = 100.95
##    bottomRightPoint.y = 98.98
##    
##    distanceFromTopLeftx=(topLeftPoint.x-bottomRightPoint.x)/2.0
##    distanceFromBottomRighty=(bottomRightPoint.y-topLeftPoint.y)/2.0
##    centerOfPlot=Point()
##    
##    centerOfPlot.x=(distanceFromTopLeftx+topLeftPoint.x)
##    centerOfPlot.y=(distanceFromBottomRighty+bottomRightPoint.y)
##    
###     centerOfPlot.x =  10
###     centerOfPlot.y = 10
##    centerOfPlot = None
##    bic = BIC()
##    bic.processData(folderAddress,sizeOfBox,zValue,mZValue,centerOfPlot,
##                    largeNumberOfspilitting)


##########################################################################
##    folderAddress = r"C:\TLS_Scans_2013_11_14\FinalRawProduct(10m)\P4\NONVEGHEIGHT"
##    #fileAddress = r"D:\My Backups\Dropbox\My Uni\My Courses\IWS\Cload_Breaks\plot4scan2_raw.asc"
##    #put z value here 
##    
##    zValue = float(1.0)
##    largeNumberOfspilitting = True
##    #put the size of box here 
##    sizeOfBox = float(0.5)
##    mZValue = None
##    topLeftPoint = Point()
##    bottomRightPoint = Point()
##    topLeftPoint.x = 99.08
##    topLeftPoint.y = 101.02
##    bottomRightPoint.x = 100.95
##    bottomRightPoint.y = 99.04
##    
##    distanceFromTopLeftx=(topLeftPoint.x-bottomRightPoint.x)/2.0
##    distanceFromBottomRighty=(bottomRightPoint.y-topLeftPoint.y)/2.0
##    centerOfPlot=Point()
##    
##    centerOfPlot.x=(distanceFromTopLeftx+topLeftPoint.x)
##    centerOfPlot.y=(distanceFromBottomRighty+bottomRightPoint.y)
##    
###     centerOfPlot.x =  10
###     centerOfPlot.y = 10
##    centerOfPlot = None
##    bic = BIC()
##    bic.processData(folderAddress,sizeOfBox,zValue,mZValue,centerOfPlot,
##                    largeNumberOfspilitting)
############################################################################
##    folderAddress = r"C:\TLS_Scans_2013_11_14\FinalRawProduct(10m)\P4\VEGHEIGHT"
##    #fileAddress = r"D:\My Backups\Dropbox\My Uni\My Courses\IWS\Cload_Breaks\plot4scan2_raw.asc"
##    #put z value here 
##    
##    zValue = float(1.0)
##    largeNumberOfspilitting = True
##    #put the size of box here 
##    sizeOfBox = float(0.5)
##    mZValue = 0.02 
##    topLeftPoint = Point()
##    bottomRightPoint = Point()
##    topLeftPoint.x = 99.08
##    topLeftPoint.y = 101.02
##    bottomRightPoint.x = 100.95
##    bottomRightPoint.y = 99.04
##    
##    distanceFromTopLeftx=(topLeftPoint.x-bottomRightPoint.x)/2.0
##    distanceFromBottomRighty=(bottomRightPoint.y-topLeftPoint.y)/2.0
##    centerOfPlot=Point()
##    
##    centerOfPlot.x=(distanceFromTopLeftx+topLeftPoint.x)
##    centerOfPlot.y=(distanceFromBottomRighty+bottomRightPoint.y)
##    
###     centerOfPlot.x =  10
###     centerOfPlot.y = 10
##    centerOfPlot = None
##    bic = BIC()
##    bic.processData(folderAddress,sizeOfBox,zValue,mZValue,centerOfPlot,
##                    largeNumberOfspilitting)
## 
#     bic.processData(folderAddress,sizeOfBox,zValue,mZValue,centerOfPlot,
#                     largeNumberOfspilitting,intervals=1,min=89,max=105)

    #bic.exludeLessThanZ(folderAddress, zValue)
    #cut between two z value 
    #firstZValue = 100
    #secondZValue = 105
    #bic.cutBetweenTwoZValue(folderAddress, firstZValue, secondZValue)
#    sizeOfBox = 1
#    middelPoint1 = Point()
#    middelPoint1.x = 997.00
#    middelPoint1.y = 1004.42
#    middelPoint2 = Point()
#    middelPoint2.x = 1002.54
#    middelPoint2.y = 998.48
#    bic.breakBoxInsideBox(folderAddress, middelPoint1, middelPoint2, sizeOfBox)
#    point1 = Point()
#    point2 = Point()
#    point3 = Point()
#
#    
#    point1.x = 990
#    point1.y = 998
#    
#    point2.x = 992
#    point2.y = 997
#    
#    point3.x = 993
#    point3.y = 1000
#    
#    bic.excluder(fileAddress,point1,point2,point3)

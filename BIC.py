import math
from _pyio import open
from tkinter.tix import MAX

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
    _folderAddress = None
    
    
    def __init__(self,fileName,folderAddress,autoOpenClose=True):
        self._folderAddress = folderAddress
        self._autoOpenClose = autoOpenClose 
        self._fileName = fileName
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
            
    def excludePointWithZValue(self,zValue,intervals=0,min=0,max=0):
        finalFileName = self._fileName.split(".")[0] + "ZzZz.asc"
        fileName = finalFileName.replace(self._folderAddress,'')
        fileNameIntervalsCount = os.path.join(self._folderAddress,'intervals_counts.txt')
        intervalsCont = []
        
        if intervals != 0 :
            if(not os.path.exists(fileNameIntervalsCount)):
                fileIntervalsCount =open(fileNameIntervalsCount,'a+')
                fileIntervalsCount.write('file_Name ')
                start = min 
                loop = True 
                while loop:
                    end = start+intervals 
                    if end > max : end = max 
                    fileIntervalsCount.write(str(start)+'_'+str(end)+' ')
                    intervalsCont.append(0)
                    start = end 
                    if end == max : break
                    
                fileIntervalsCount.write(os.linesep)
            else : 
                fileIntervalsCount =open(fileNameIntervalsCount,'a+')
                start = min 
                loop = True 
                while loop:
                    end = start+intervals 
                    if end > max : end = max 
                    intervalsCont.append(int(0))
                    start = end 
                    if end == max : break
        fileToWrite = open(finalFileName,"w")
        firstTime = True
        for line in self.readFromFile():
            point = Point(line)
            if point.z-min > 0.00000001 and point.z -max <0.00000001 :
                start = min 
                end = min + intervals
                index = 0
                for count in intervalsCont:
                    if point.z- start >0.00000001 and point.z-end <0.00000001 :
                        intervalsCont[index] = count +1
                        break
                    index = index + 1
                    start = end 
                    end = start + intervals
#                intervalsCont[int(math.floor(float(max-point.z)/intervals))] = \
#                                    intervalsCont[int(math.floor(float(max-point.z)/intervals))]+1
            if ((point.z - (self._minimumZValue + zValue)) <0):
                self._numberOfPoins += 1
                self._totalZValue +=point.z
                if point.d:
                    self._totalDensity += point.d
                if(firstTime):
                    firstTime = False
                    self._maximumZValue = point.z
                    if point.d :
                        self._maxDensity = point.d
                        self._minmumDensity = point.d
                else:
                    if point.z > self._maximumZValue:
                        self._maximumZValue = point.z
                    if point.d :
                        if point.d > self._maxDensity :
                            self._maxDensity = point.d
                        if point.d < self._minmumDensity :
                            self._minmumDensity = point.d
                fileToWrite.write(line)
        fileIntervalsCount.write(fileName+' ')
        for count in intervalsCont :
            fileIntervalsCount.write(str(count)+' ')
        fileIntervalsCount.write(os.linesep)
        fileIntervalsCount.close()
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
        else : average = -1
        if(self._maximumZValue == None):
            self._maximumZValue = -1
        if(self._minimumZValue == None):
            self._minimumZValue = -1
        if self._minmumDensity :
            return [self._minimumZValue,self._maximumZValue,self._numberOfPoins,
                    average,self._minmumDensity,self._maxDensity,averageDensity]
        else :
            return [self._minimumZValue,self._maximumZValue,self._numberOfPoins,
                    average]
        
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
    
    def _initialIO(self,topLeftPoint,downRightPoint,sizeOfBox,folderAddress,
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
        cloadSizeInfoFileHandler.write('File_Name Top_Left_x Top_Left_y Down_Right_x Down_Right_y Center_x Center_y'+os.linesep)
        while(tlp.y > downRightPoint.y):
            iOLine = []
            tlp.x = minimumX
            while (tlp.x < downRightPoint.x):
                i += 1
                drp.x = tlp.x+sizeOfBox
                drp.y = tlp.y-sizeOfBox
                centerPoint.x = tlp.x+ sizeOfBox/float(2)
                centerPoint.y = tlp.y+ sizeOfBox/float(2)
                cloadSizeInfoFileHandler.write(str(i)+'. '+str(tlp.x)+' '+str(tlp.y)+' '
                                               +str(drp.x)+' '+str(drp.y)+' '
                                               +str(centerPoint.x)+' '+str(centerPoint.y)
                                               +os.linesep)
                fileAddress = os.path.join( folderAddress , str(i)+".asc")
                io = IO(fileAddress,folderAddress,largeNumberOfspilitting)
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
            
        
    def processData(self,folderAddress,sizeOfBox = 1 , zValue = 2 
                    ,largeNumberOfspilitting = False,plotInfo = 'plotInfo.txt',
                    intervals=0,min=0,max=0):
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
            
            iOMatrix = self._initialIO(topLeftPoint, downRightPoint, sizeOfBox, outPutFolder,largeNumberOfspilitting)
            print ('initial IO is done')
            
            fileReader = open(fileName,'r')
            for line in fileReader:
                point = Point(line)
                io = iOMatrix[(int((point.y - downRightPoint.y)/sizeOfBox))]\
                [(int((point.x - topLeftPoint.x)/sizeOfBox))] 
                io.writeToFile(line ,point.z)
            print ('writing point to disk is done')   
            plotInfoFileHandler.write('  '+' Point_count Maximum_Z Minimum_Z Average_Z '
                                      +'Maximum_Density Minimum_Density Average_Density '+os.linesep )
            for iOLine in iOMatrix :
                for io in iOLine :
                    io.colseFile()
                    io.excludePointWithZValue(zValue,intervals,min,max)  
                    cloadInfo = io.minmumMaximumAndAverage()
                    if len(cloadInfo) == 4:   
                        minimum,maximum,numberOfPoints,average= cloadInfo
                        plotInfoFileHandler.write(io.getFileName().split(os.sep).pop().split('.')[0]
                                        +' '+str(numberOfPoints)+' '+str(maximum)+os.linesep)
                    else:
                        minimum,maximum,numberOfPoints,average,minimumD,maximumD,averageD=cloadInfo
                        plotInfoFileHandler.write(io.getFileName().split(os.sep).pop().split('.')[0]
                                        +' '+str(numberOfPoints)+' '+str(maximum)+' '
                                        +str(minimum)+' '+str(average)+' '+
                                        str(maximumD)+' '+str(minimumD)+' '+
                                        str(averageD)+' '+os.linesep)
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
        print ('All file is processed')

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
    #put your folder address here 
    folderAddress = r"D:\My Backups\Dropbox\My Uni\My Courses\IWS\Cloud-Breaker-\Cloud-Breaker-"
    #fileAddress = r"D:\My Backups\Dropbox\My Uni\My Courses\IWS\Cload_Breaks\plot4scan2_raw.asc"
    #put z value here 
    
    zValue = float(0.5)
    largeNumberOfspilitting = False
    #put the size of box here 
    sizeOfBox = float(0.5)
    bic = BIC()
    bic.processData(folderAddress,sizeOfBox,zValue,
                    largeNumberOfspilitting,intervals=0.1,min=99,max=101)

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
    

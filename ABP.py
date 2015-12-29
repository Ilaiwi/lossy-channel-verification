

class Process : 
    def __init__(self,ID,state=0):
        self.ID = ID 
        self.state = state
    def __str__(self):
        return str(self.state)
class Channel : 
    def __init__(self,data="",alphabet=[1,0]):
        self.data = data  # string contains the data in the channel .
        self.alphabet=[] # list of alphabet allowed in the channels
        self.processes = [] # list contains ID of processes that can access the channel .// maybe we will use dictionary instead of list
    def subWords(self,length=None) :
        subWordList =[]
        data = self.data
        channelLength = len(data)
        if length== None : length=channelLength
        for i in range(1,length+1):
            for j in range(0,channelLength-i+1):
                subWordList.append(data[j:j+i])
        return subWordList
    def __str__(self):
        return self.data  
    def __lt__(self, other):
         return self.data < other.data
class SystemState : 
    def __init__(self,controlState,channels):
        self.controlState = controlState # list of processes // maybe we will use dictionary instead of list 
        self.channels = channels #list contain all channels in the system // maybe we will use dictionary instead of list  
       # self.badStates = [] #list of  string to identify the bad states

        
    def alpha(self, k):
        views = [] 
        subWordList1 = self.channels[0].subWords(k)
        subWordList2 = self.channels[1].subWords(k)
        for i in range(len(subWordList1)):
            for j in range(len(subWordList2)):
                view = SystemState(self.controlState,[Channel(subWordList1[i]),Channel(subWordList2[j])]) 
                if view not in views :
                    views.append(view)
        

        return views; # return the views of the system
    
    def subView(self):
        
        return [];  # return the sub views of the system
    
    def __str__( self ):
        tempProc=""
        for i in self.controlState:
            tempProc=tempProc+str(i)+','
        tempData=""
        for i in self.channels:
            tempData=tempData+'['+str(i)+'],'
        return '<'+tempProc+tempData+'>';
    
   
    
    
    #help function for divideConfs
    def strProcesses(self,conf):
        temp=""
        for i in conf.controlState:
            temp=temp+str(i.state)
        return temp
    
    #helper function for gama
    def divideConfs(self,confs):
        matchedConfs={}
        
        for i in confs:
            key=self.strProcesses(i)
            if key in matchedConfs:
                matchedConfs[key].append(i);
            else:
                matchedConfs[key]=[i];
        return matchedConfs
    
    #helper function to return the biggest confs
    def biggestChannel(self,conf):
        
        for i in conf:
        	pass   
        return []
    #helper extract channel data from all confs
    def extractData(self,i,confs):
        tempData=[]
        for j in confs:
            tempData.append(j.channels[i])
        return tempData
    
    #helper function to return the k gama of a channel data
    def gamaData(self,k,conf):
        return []
    
    #helper function to find gama for only one channel
    def gamaChannel(self,k,conf):
        conf.sort()
        i=-1
        if (len(conf[-1].data)==k-1):
            for j in range(len(conf)):
                if(len(conf[i].data)==k-1):
                    i=i-1
                else:
                    break
        gamaChannels=conf[len(conf)+i:len(conf)]
        for j in gamaChannels:
            temp=self.gamaData(k, j)
            for w in temp:
                w.subWords() in conf
        return []
    
    def gama(self, k , confs):
        matchedConfs=self.divideConfs(confs)
        gamaResult=[]
        for i in matchedConfs.values():
            gamaChannelsResult=[]
            for j in range(len(i.channels)):
                gamaChannelsResult.append(self.gamaChannel(k, self.extractData(j, i)))
        return []
    
                
    def post(self):
        
        return 1; # return a systemState
    
    def Apost(self):
        
        return []; # return set of views
    def __eq__(self,other):
        if self.controlState==other.controlState and self.channels==other.channels :
            return True 

        return False
test = SystemState([Process(1,1),Process(2,1)],[Channel("110"),Channel("111")])
l  = test.alpha(2)
for i in xrange(0,len(l)):
	print str(i) + " => "+str(l[i])
print str(len(l))

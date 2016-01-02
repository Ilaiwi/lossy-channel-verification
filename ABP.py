
class Process : 
    def __init__(self,ID,state=0):
        self.ID = ID 
        self.state = state
    def __str__(self):
        return str(self.state)
    def next(self) : 
        self.state = (self.state % 4 ) +1  
    def copy(self):
        return Process(self.ID,self.state)
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
    def append(self,char):
        self.data = self.data + char
        return 0
    def copy(self):
        return Channel(self.data,self.alphabet)

    def remove(self):
        if len(self.data)>0 :
            char = self.data[0]
            self.data = self.data[1:]
            return char
        return None
class SystemState : 
    def __init__(self,controlState,automata,channels):
        self.controlState = controlState # list of processes // maybe we will use dictionary instead of list 
        self.channels = channels #list contain all channels in the system // maybe we will use dictionary instead of list  
       	self.automata = automata
       # self.badStates = [] #list of  string to identify the bad states

        
    def alpha(self, k):
        views = [] 
        subWordList1 = self.channels[0].subWords(k)
        subWordList2 = self.channels[1].subWords(k)
        for i in range(len(subWordList1)):
            for j in range(len(subWordList2)):
                view = SystemState(self.controlState,self.automata,[Channel(subWordList1[i]),Channel(subWordList2[j])]) 
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
        return '<'+tempProc+str(self.automata)+","+tempData+'>';
    
   # helper function for post , returns control state as a lost of integers
    def controlStateVal(self) : 
        return [self.controlState[0].state ,self.controlState[1].state ]
    
    #help function for divideConfs
    def strProcesses(self,conf):
        temp=""
        for i in conf.controlState:
            temp=temp+str(i.state)
        return temp
    def copy(self) :
        return SystemState([self.controlState[0].copy(),self.controlState[1].copy()], self.automata,[self.channels[0].copy(),self.channels[1].copy()])
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
            tempData.append(j.channels[i].data)
        return tempData
    
    #helper function to find gama for only one channel
    def gamaChannel(self,k,conf):
        
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
        nextStateList =[]
        currState = self
        nextState1,nextState2 = currState.copy(),currState.copy()
        sender = currState.controlState[0]
        reciever = currState.controlState[1]
        #second possible transition
        nextState1 = self.copy()
        if sender.state == 1 or sender.state == 3  : 
            nextState1.automata+=1
            nextState1.controlState[0].next()
        elif sender.state == 2 : 
            rec = nextState1.channels[1].remove()
            if rec == "0" : 
                nextState1.controlState[0].next()
            else :
                nextState1.channels[0].append("0")
        elif sender.state ==4 : 
            rec = nextState1.channels[1].remove()
            if rec == "1" : 
                nextState1.controlState[0].next()
            else :
                nextState1.channels[0].append("1")
       
        nextStateList.append(nextState1)
        # second possible transition
        nextState2 = self.copy()
        if reciever.state == 1 : 
            rec = nextState2.channels[0].remove()
            if rec == "0" : 
                nextState2.controlState[1].next()
            else :
                nextState2.channels[1].append("1")
        elif reciever.state == 2 or reciever.state ==4 : 
            nextState2.automata-=1
            if(nextState2.automata==0): nextState2.automata = 3
            nextState2.controlState[1].next()
        elif reciever.state == 3 :
            rec = nextState2.channels[0].remove()
            if rec == "1" : 
                nextState2.controlState[1].next()
            else :
                nextState2.channels[1].append("0")                

        nextStateList.append(nextState2)

        return nextStateList

       
    def channelsVal(self):
    	return [self.channels[0].data,self.channels[1].data]
    def Apost(self):
        
        return []; # return set of views
    def __eq__(self,other):
        if self.controlStateVal()==other.controlStateVal() and self.channelsVal()==other.channelsVal() and self.automata==other.automata :
            return True 

        return False

def underApproximation(initState,K): # return False if there is an reachable bad state of size K 
	reachableList = []
	reachableList.append(initState)
	i=0
	while i != len(reachableList):
		state1,state2 = reachableList[i].post()
		#print str(reachableList[i]) # + "------" + str(state1) + "------" + str(state2)
		if len(state1.channels[0].data) <= K and len(state1.channels[1].data) <= K :
			if state1.automata == 3 : return False
			if state1 not in reachableList : reachableList.append(state1)
		if len(state2.channels[0].data) <= K and len(state2.channels[1].data) <= K :
			if state2.automata == 3 : return False
			if state2 not in reachableList : reachableList.append(state2)
		i+=1
	return True


test = SystemState([Process(1,1),Process(1,1)],1, [Channel(""),Channel("")])
test2 = SystemState([Process(1,2),Process(1,1)],1, [Channel(""),Channel("")])
#print test==test2
print underApproximation(test, 2)
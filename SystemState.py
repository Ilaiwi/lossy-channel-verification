from bisect import *
import itertools 
from Channel import * 
from Process import * 
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
    @staticmethod
    def divideConfs(confs):
        matchedConfs={}
        
        for i in confs:
            key=i.strProcesses(i)
            if key in matchedConfs:
                matchedConfs[key].append(i);
            else:
                matchedConfs[key]=[i];
        return matchedConfs
    @staticmethod
    def extractData(i,confs):
        tempData=[]
        for j in confs:
            tempData.append(j.channels[i])
        return list(set(tempData))

    #helper function to return the biggest confs
    def biggestChannel(self,conf):
        
        for i in conf:
            pass   
        return []
   
    @staticmethod
    def gamaData(conf):
        gamaConfs=[]
        gamaConfs.append(Channel(conf.data[0]+conf.data))
        for i in range(len(conf.data)-1):
            if conf.data[i]!=conf.data[i+1]:
                gamaConfs.append(Channel(conf.data[0:i+1]+conf.data[i+1]+conf.data[i+1:len(conf.data)]))
        return gamaConfs

    @staticmethod
    def binary_search(a, x, lo=0, hi=None):   # can't use a to specify default for hi
        hi = hi if hi is not None else len(a) # hi defaults to len(a)   
        pos = bisect_left(a,x,lo,hi)          # find insertion position
        return (pos if pos != hi and a[pos] == x else -1) # don't walk off the end

    #helper function to find gama for only one channel
    @staticmethod
    def gamaChannel(k,conf):
        result=[]
        conf.sort()
        #Channel.printArray(conf)
        i=-1
        for j in range(len(conf)):
            if(len(conf[i].data)==k-1):
                i=i-1
            else:
                break
        gamaChannels=conf[len(conf)+i+1:len(conf)]
        for j in gamaChannels:
            temp=SystemState.gamaData(j)
            # Channel.printArray(temp)
            for w in temp:
                Subtemp=w.subWords()
                Subtemp=Subtemp[:-1]
                #print(Subtemp)
                flag=False
                for c in Subtemp:
                    tempConf=Channel(c)
                    #print(SystemState.binary_search(conf, tempConf))
                    if (SystemState.binary_search(conf, tempConf) != -1):
                        
                        flag=True
                    else:
                        flag=False
                #print(flag)
                if flag:
                    result.append(w)
        return result

    @staticmethod
    def gama(k , confs):
        matchedConfs=SystemState.divideConfs(confs)
        gamaResult=[]
        for i in matchedConfs.values():
            gamaChannelsResult=[]
            for j in range(len(i[0].channels)):
                channels=SystemState.extractData(j, i);
#                 print ("---------"+str(j)+"-------------")
#                 print (Channel.printArray(channels));
#                 print ("----------------------")
                temp=SystemState.gamaChannel(k, channels);
                gamaChannelsResult.append([temp,temp+channels])
                
            gamaChannelsResultCompined=[]
            for j in range(len(gamaChannelsResult)):
                temp=[]
                for w in range(len(gamaChannelsResult)):
                    if w == j:
                        temp.append(gamaChannelsResult[w][0])
                    else:
                        temp.append(gamaChannelsResult[w][1])
                gamaChannelsResultCompined=gamaChannelsResultCompined+(list(itertools.product(*temp)))
            
            for j in gamaChannelsResultCompined:      
                gamaResult.append(SystemState(i[0].controlState,i[0].automata,list(j)))
        gamaResult=gamaResult+confs
        return gamaResult
                
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
    @staticmethod
    def Apost(K,X):
        V = X
        C = SystemState.gama(K,X)
        for c in C :
            state1,state2 = c.post()
            for s in state1.alpha(K):
                if s not in V : V.append(s)
            for s in state2.alpha(K):
                if s not in V : V.append(s)            
        return V
         
    def __eq__(self,other):
        if self.controlStateVal()==other.controlStateVal() and self.channelsVal()==other.channelsVal() and self.automata==other.automata :
            return True 

        return False
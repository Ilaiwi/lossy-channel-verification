

class Process : 
    def __init__(self,ID,state):
        self.ID = ID 
        self.state = state
class Channel : 
    def __init__(self):
        self.data = ""  # string contains the data in the channel . 
        self.processes = [] # list contains ID of processes that can access the channel .// maybe we will use dictionary instead of list  
class SystemState : 
    def __init__(self,controlState,channels):
        self.controlState = controlState # list of processes // maybe we will use dictionary instead of list 
        self.channels = channels #list contain all channels in the system // maybe we will use dictionary instead of list  
       # self.badStates = [] #list of  string to identify the bad states
        
    def alpha(self, k):
        views = [] 
        sub =[[]]  
        for c in range(0,len(self.channels)):
            sub.append([])
            for i in range(1,k+1):
                j=0
                while j+i <= len(self.channels[c]) :
                    sub[c].append(self.channels[c][j:j+i])
                    j+=1
        for i in range(len(sub[0])):
            for j in range(len(sub[1])):
                view = SystemState(self.controlState,[sub[0][i],sub[1][j]]) 
                if view not in views :
                    views.append(view)
        

        return views; # return the views of the system
    
    def subView(self):
        
        return [];  # return the sub views of the system
    
    def __str__( self ):
        
        return '<'+str(self.controlState)+','+str(self.channels)+'>';
    
    
    
    
    #help function for divideConfs
    def strProcesses(self,conf):
        temp=""
        for i in conf.controlState:
            temp.append(str(i))
        return temp
    
    #helper function for gama
    def divideConfs(self,confs):
        matchedConfs={}
        for i in confs:
            if self.strProcesses(i) in matchedConfs.keys():
                matchedConfs[self.strProcesses(i)].append(i);
            else:
                matchedConfs[self.strProcesses(i)]=[i];
        return matchedConfs
    
    #helper function to return the biggest confs
    def biggestChannel(self,conf):
        
        for i in conf:
            
        return []
    
    #helper function to find gama for only one config
    def gamaConf(self,k,conf):
        
        return []
    
    def gama(self, k , confs):
        matchedConfs=self.divideConfs(confs)
        for i in matchedConfs.values():
            i
        return []
    
                
    def post(self):
        
        return 1; # return a systemState
    
    def Apost(self):
        
        return []; # return set of views
    def __eq__(self,other):
        if self.controlState==other.controlState and self.channels==other.channels :
            return True 

        
init = SystemState([1,2],["110","111"]) 
L = init.alpha(3)
for i in range(len(L)):
    print(L[i]) 
    #automata 
    
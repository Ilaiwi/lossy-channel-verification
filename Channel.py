class Channel : 
    def __init__(self,data="",alphabet=['1','0']):
        self.data = data  # string contains the data in the channel .
        self.alphabet=alphabet # list of alphabet allowed in the channels
        self.processes = [] # list contains ID of processes that can access the channel .// maybe we will use dictionary instead of list
    def subWords(self,length=None) :
        subWordList =[""]
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
    def __hash__(self):
        return hash(self.data)
    def __lt__(self, other):
        return self.data < other.data
    @staticmethod
    def printArray(confs):
        for i in confs:
            print(i)
    def __eq__(self,other):
        return self.data==other.data
    def remove(self):
        if len(self.data)>0 :
            char = self.data[0]
            self.data = self.data[1:]
            return char
        return None

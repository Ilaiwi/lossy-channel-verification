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

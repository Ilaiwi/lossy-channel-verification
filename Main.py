from Channel import * 
from Process import * 
from SystemState import * 
def underApproximation(initState,K): # return False if there is an reachable bad state of size K 
    reachableList = []
    reachableList.append(initState)
    i=0
    while i != len(reachableList):
        state1,state2 = reachableList[i].post()
        if len(state1.channels[0].data) <= K and len(state1.channels[1].data) <= K :
            if state1.automata == 3 : return False
            if state1 not in reachableList : reachableList.append(state1)
        if len(state2.channels[0].data) <= K and len(state2.channels[1].data) <= K :
            if state2.automata == 3 : return False
            if state2 not in reachableList : reachableList.append(state2)
        i+=1
    return True

def overAproximation(initState,K) :
    V = initState.alpha(K)
    print str(V)
    len1 = len(V)
    V = SystemState.Apost(K,V)
    len2 = len(V)
    while len2!=len1:
        len1 = len(V)
        V = SystemState.Apost(K,V)
        len2 = len(V)
    for x in V:
        if x.automata == 3 :
            return False
    print len(V)
    return True


# K=1
# initState = SystemState([Process(1,1),Process(2,1)],1,[Channel(""),Channel("")])
# while  True :
#     if not underApproximation(initState,K):
#         print "there is an bad state" , str(K)
#         exit()
#     if overAproximation(initState,K) :
#         print "The system is verified" , str(K)
#         exit()

# test gamachannel
# a = [Channel('0'),Channel('1'),Channel('10'),Channel('11'),Channel('110')]
# print(Channel.printArray(SystemState.gamaChannel(4, a)))

# #test alpha
# print "test alpha ----------------------- "

test = SystemState([Process(1,1),Process(2,1)],1,[Channel("111"),Channel("")])
l  = test.alpha(1)

# for x in l:
#     print str(x)
# print "===================="
# V = test.Apost(2,l)
# for x in V :
#     print str(x)
# print overAproximation(test,1)
# for i in xrange(0,len(l)):
#     print str(i) + " => "+str(l[i])
# print str(len(l))

#test gama
print "test gama ----------------------- "
g=SystemState.gama(1, l)
# print g
for i in xrange(0,len(g)):
    print str(i) + " => "+str(g[i])
print str(len(g))

#test underapproximation
print "test underapproximation ----------------------- "

test = SystemState([Process(1,1),Process(1,1)],1, [Channel(""),Channel("")])
test2 = SystemState([Process(1,2),Process(1,1)],1, [Channel(""),Channel("")])
# print underApproximation(test, 2)


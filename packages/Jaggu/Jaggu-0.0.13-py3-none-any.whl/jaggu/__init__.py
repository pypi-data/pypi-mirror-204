def pgm1a():
	return """ 
SuccList={

    'A':[['B',3],['C',2]],

    'B':[['A',5],['C',2],['D',2],['E',3]],

    'C':[['A',5],['B',3,],['F',2],['G',4]],

    'D':[['H',1],['I',99]],

    'F':[['J',99]],

    'G':[['K',99],['L',3]]

}

start='A'

goal='E'

closed=list()

SUCCESS=True

FAILURE=False

state=FAILURE

def MOVEGEN(N):

    New_List=list()

    if N in SuccList.keys():

        New_List=SuccList[N]

    return New_List

def GOALTEST(N):

    if N==goal:

        return True

    else:

        return False

def APPEND(l1,l2):

    New_List=list(l1)+list(l2)

    return New_List

def SORT(L):

    L.sort(key=lambda x:x[1])

    return L

def BestFirstSearch():

    OPEN=[[start,5]]

    CLOSED=list()

    global state

    global closed

    while(len(OPEN)!=0)and (state!=SUCCESS):

        print("-------------------------------")

        N=OPEN[0]

        print("N = ",N)

        del OPEN[0]

        if GOALTEST(N[0])==True:

             state=SUCCESS

            CLOSED=APPEND(CLOSED,[N])

            print("Closed = ",CLOSED)

        else:

            CLOSED=APPEND(CLOSED,[N])

            print("Closed = ",CLOSED)

            CHILD=MOVEGEN(N[0])

            print("Child = ",CHILD)

            for val in CLOSED:

                if val in CHILD:

                    CHILD.remove(val)

            for val in OPEN:

                if val in CHILD:

                    CHILD.remove(val)

            OPEN=APPEND(CHILD,OPEN)

            print("Unsorted List = ",OPEN)

            SORT(OPEN)

            print("Sorted List = ",OPEN)

    closed=CLOSED

    return state  



result=BestFirstSearch()

print(closed,result)
	
"""

def pgm1b():
	return """
def aStarAlgo(start_node,stop_node):

    open_set=set(start_node)

    closed_set=set()

    g={}

    parents={}

    

    g[start_node]=0

    parents[start_node]=start_node

    

    while len(open_set)>0:

        n=None

        for v in open_set:

            if n== None or g[v]+heuristic(v)<g[n]+heuristic(n):

                n=v

        if n==stop_node or Graph_nodes[n]==None:

            pass

        

        else:

            for (m,weight) in get_neighbors(n):

                if m not in open_set and m not in closed_set:

                    open_set.add(m)

                    parents[m]=n

                    g[m]=g[n]+weight

                else:

                    if g[m]>g[n]+weight:

                        g[m]=g[n]+weight

                        parents[m]=n

                                            

                        if m in closed_set:

                            closed_set.remove(m)

                            open_set.add(m)

                            

        if n==None:

            print('Path does not exist!')

            return None

        if n==stop_node:

            path=[]

            

            while parents[n]!=n:

                path.append(n)

                n=parents[n]

                

            path.append(start_node)

            path.reverse()

            print('Path found: {}'.format(path))

            return path

        

        open_set.remove(n)

        closed_set.add(n)

    print('Path does not exist!')

    return None

    

def get_neighbors(v):

    if v in Graph_nodes:

        return Graph_nodes[v]

    else:

        return None

    

def heuristic(n):

    H_dist={

        'A':11,

        'B':6,

        'C':99,

        'D':1,

        'E':7,

        'G':0,

    }

    return H_dist[n]



Graph_nodes = {

    'A': [('B',2),('E',3)],

    'B':[('C',1),('G',9)],

    'C':None,

    'E':[('D',6)],

    'D':[('G',1)],

}

aStarAlgo('A','G')
"""


def pgm2():

	return """
from collections import defaultdict



jug1,jug2,aim=4,3,2 

visited=defaultdict(lambda:False)



def waterJugSolver(amt1,amt2):

    if(amt1==aim and amt2==0)or(amt2==aim and amt1==0):

        print(amt1,amt2)

        return True

    

    if visited[(amt1,amt2)]==False:

        print(amt1,amt2)

        visited[(amt1,amt2)]=True

        return(waterJugSolver(0,amt2) or 

               waterJugSolver(amt1,0) or 

               waterJugSolver(jug1,amt2) or

              waterJugSolver(amt1,jug2) or waterJugSolver(amt1+min(amt2,(jug1-amt1)),amt2-min(amt2,(jug1-amt1))) or 

              waterJugSolver(amt1-min(amt1,(jug2-amt2)),at2+min(amt1,(jug2-amt2))))

    

    else:

        return False

    



print("Steps: ")

waterJugSolver(0,0)
"""


def pgm3():
	return """
global N

N = 4 

def printSolution(board):

    for i in range(N):

        for j in range(N):

            print(board[i][j], end = " ")

        print()





def isSafe(board, row, col):

 



    for i in range(col):

        if board[row][i] == 1:

            return False

 



    for i, j in zip(range(row, -1, -1),

                    range(col, -1, -1)):

        if board[i][j] == 1:

            return False

 

   

    for i, j in zip(range(row, N, 1),

                    range(col, -1, -1)):

        if board[i][j] == 1:

            return False

 

    return True

 

def solveNQUtil(board, col):

     



    if col >= N:

        return True

 



    for i in range(N):

 

        if isSafe(board, i, col):

             

 

            board[i][col] = 1



            if solveNQUtil(board, col + 1) == True:

                return True

 

         

            board[i][col] = 0



    return False

 



def solveNQ():

    board = [ [0, 0, 0, 0],

              [0, 0, 0, 0],

              [0, 0, 0, 0],

              [0, 0, 0, 0] ]

 

    if solveNQUtil(board, 0) == False:

        print ("Solution does not exist")

        return False

 

    printSolution(board)

    return True

 

solveNQ()
"""


def pgm4():
	return """
facts={

       "apple": "A fruit that is red or green",

       "banana":"A yellow fruit that is often eaten for breakfast",

       "orange":"A round fruit that is orange in colour and has a citrusy taste",

}



def handle_query(query):

    if query in facts:

        return facts[query]

    else:

        return "I don't know about that"

query=input("BOT: What do you want to know?")

result=handle_query(query)

print(result)
"""


def pgm5():
	return """

def word_blocks(word):

    if len(word)==1:

        return[word]

    words=[]

    for i in range(len(word)):

        letter=word[i]

        new_word=word[:i]+word[i+1:]

        sub_words=word_blocks(new_word)

        for sub_word in sub_words:

            words.append(letter+sub_word)

    return words

print(word_blocks('bca'))
"""


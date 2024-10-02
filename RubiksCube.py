import random
import sys
import time
import copy
from collections import deque


MOVES = {
    "U": [2,  0,  3,  1, 20, 21,  6,  7,  4,  5, 10, 11, 12, 13, 14, 15,  8,  9, 18, 19, 16, 17, 22, 23],
    "U'": [1,  3,  0,  2,  8,  9,  6,  7, 16, 17, 10, 11, 12, 13, 14, 15, 20, 21, 18, 19,  4,  5, 22, 23],
    "R": [0,  9,  2, 11,  6,  4,  7,  5,  8, 13, 10, 15, 12, 22, 14, 20, 16, 17, 18, 19,  3, 21,  1, 23],
    "R'": [0, 22,  2, 20,  5,  7,  4,  6,  8,  1, 10,  3, 12, 9, 14, 11, 16, 17, 18, 19, 15, 21, 13, 23],
    "F": [0,  1, 19, 17,  2,  5,  3,  7, 10,  8, 11,  9, 6,  4, 14, 15, 16, 12, 18, 13, 20, 21, 22, 23],
    "F'": [0,  1,  4,  6, 13,  5, 12,  7,  9, 11,  8, 10, 17, 19, 14, 15, 16,  3, 18,  2, 20, 21, 22, 23],
    "D": [0,  1,  2,  3,  4,  5, 10, 11,  8,  9, 18, 19, 14, 12, 15, 13, 16, 17, 22, 23, 20, 21,  6,  7],
    "D'": [0,  1,  2,  3,  4,  5, 22, 23,  8,  9,  6,  7, 13, 15, 12, 14, 16, 17, 10, 11, 20, 21, 18, 19],
    "L": [23,  1, 21,  3,  4,  5,  6,  7,  0,  9,  2, 11, 8, 13, 10, 15, 18, 16, 19, 17, 20, 14, 22, 12],
    "L'": [8,  1, 10,  3,  4,  5,  6,  7, 12,  9, 14, 11, 23, 13, 21, 15, 17, 19, 16, 18, 20,  2, 22,  0],
    "B": [5,  7,  2,  3,  4, 15,  6, 14,  8,  9, 10, 11, 12, 13, 16, 18,  1, 17,  0, 19, 22, 20, 23, 21],
    "B'": [18, 16,  2,  3,  4,  0,  6,  1,  8,  9, 10, 11, 12, 13,  7,  5, 14, 17, 15, 19, 21, 23, 20, 22],
}


def perm_apply(perm, position):
  return tuple([position[i] for i in perm])

def perm_inverse(p):
    n = len(p)
    q = [0]*n
    for i in range(n):
        q[p[i]] = i
    return tuple(q)

def perm_to_string(p):
    s = "("
    for x in p: s = s + "%2d "%x
    s += ")"
    return s

I = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23)

F = (0,  1, 19, 17,  2,  5,  3,  7, 10,  8, 11,  9, 6,  4, 14, 15, 16, 12, 18, 13, 20, 21, 22, 23)
Fi = perm_inverse(F)

L = (23,  1, 21,  3,  4,  5,  6,  7,  0,  9,  2, 11, 8, 13, 10, 15, 18, 16, 19, 17, 20, 14, 22, 12)
Li = perm_inverse(L)

U = (2,  0,  3,  1, 20, 21,  6,  7,  4,  5, 10, 11, 12, 13, 14, 15,  8,  9, 18, 19, 16, 17, 22, 23)
Ui = perm_inverse(U)

R = (0,  9,  2, 11,  6,  4,  7,  5,  8, 13, 10, 15, 12, 22, 14, 20, 16, 17, 18, 19,  3, 21,  1, 23)
Ri = perm_inverse(R)

D = (0,  1,  2,  3,  4,  5, 10, 11,  8,  9, 18, 19, 14, 12, 15, 13, 16, 17, 22, 23, 20, 21,  6,  7)
Di = perm_inverse(D)

B = (5,  7,  2,  3,  4, 15,  6, 14,  8,  9, 10, 11, 12, 13, 16, 18,  1, 17,  0, 19, 22, 20, 23, 21)
Bi = perm_inverse(B)

quarter_twists = (F, Fi, L, Li, U, Ui, R, Ri, D, Di, B, Bi)

quarter_twists_names = {}
quarter_twists_names[F] = 'F'
quarter_twists_names[Fi] = 'Fi'
quarter_twists_names[L] = 'L'
quarter_twists_names[Li] = 'Li'
quarter_twists_names[U] = 'U'
quarter_twists_names[Ui] = 'Ui'
quarter_twists_names[R] = 'R'
quarter_twists_names[Ri] = 'Ri'
quarter_twists_names[D] = 'D'
quarter_twists_names[Di] = 'Di'
quarter_twists_names[B] = 'B'
quarter_twists_names[Bi] = 'Bi'



class Cube:
    
    def __init__(self, string="WWWW RRRR GGGG YYYY OOOO BBBB"):
        self.no_cube = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23)
        self.string = string
        self.available_moves = ["U", "U'", "R", "R'", "F", "F'", "D", "D'", "L", "L'", "B", "B'"]
        self.stickers = list(range(24))
        
    def clone(self,abc):
        judgeFace = copy.deepcopy(abc) 
        return judgeFace
    
    def print_cube(self):
        str = self.string
        str = str.replace(" ", "")
        
        print("    " + str[0:2])
        print("    " + str[2:4])
        print(str[16:18] + "  " + str[8:10] + "  " + str[4:6] + "  " + str[20:22])
        print(str[18:20] + "  " + str[10:12] + "  " + str[6:8] + "  " + str[22:24])
        print("    " + str[12:14])
        print("    " + str[14:16])

    
    
    def newMove (self, move, abc):
        xyz = []
        if move == 'U':
            xyz = abc[2] ,  abc[0] , abc[3] ,  abc[1], abc[20], abc[21],  abc[6],  abc[7],  abc[4], abc[5] , abc[10], abc[11], abc[12], abc[13], abc[14], abc[15],  abc[8],  abc[9], abc[18], abc[19], abc[16], abc[17], abc[22] , abc[23]
        elif move == "U'":
            xyz = abc[1] , abc[3] , abc[0] , abc[2] , abc[8] , abc[9] , abc[6] , abc[7] , abc[16] , abc[17] , abc[10] , abc[11] , abc[12] , abc[13] , abc[14] , abc[15] , abc[20] , abc[21] , abc[18] , abc[19] , abc[4] , abc[5] , abc[22] , abc[23]
        elif move == "R":
            xyz = abc[0] , abc[9] , abc[2] , abc[11] , abc[6] , abc[4] , abc[7] , abc[5] , abc[8] , abc[13] , abc[10] , abc[15] , abc[12] , abc[22] , abc[14] , abc[20] , abc[16] , abc[17] , abc[18] , abc[19] , abc[3] , abc[21] , abc[1] , abc[23]
        elif move == "R'":
            xyz = abc[0] , abc[22] , abc[2] , abc[20] , abc[5] , abc[7] , abc[4] , abc[6] , abc[8], abc[1] , abc[10] , abc[3] , abc[12] , abc[9] , abc[14] , abc[11] , abc[16] , abc[17] , abc[18] , abc[19] , abc[15] , abc[21] , abc[13] , abc[23]
        elif move == "F":
            xyz = abc[0] , abc[1] , abc[19] , abc[17] , abc[2] , abc[5] , abc[3] , abc[7] , abc[10], abc[8] , abc[11] , abc[9] , abc[6] , abc[4] , abc[14] , abc[15] , abc[16] , abc[12] , abc[18] , abc[13] , abc[20] , abc[21] , abc[22] , abc[23]
        elif move == "F'":
            xyz = abc[0] , abc[1] , abc[4] , abc[6] , abc[13] , abc[5] , abc[12] , abc[7] , abc[9], abc[11] , abc[8] , abc[10] , abc[17] , abc[19] , abc[14] , abc[15] , abc[16] , abc[3] , abc[18] , abc[2] , abc[20] , abc[21] , abc[22] , abc[23]
        elif move == "D":
            xyz = abc[0] , abc[1] , abc[2] , abc[3] , abc[4] , abc[5] , abc[10] , abc[11] , abc[8], abc[9] , abc[18] , abc[19] , abc[14] , abc[12] , abc[15] , abc[13] , abc[16] , abc[17] , abc[22] , abc[23] , abc[20] , abc[21] , abc[6] , abc[7]
        elif move == "D'":
            xyz = abc[0] , abc[1] , abc[2] , abc[3] , abc[4] , abc[5] , abc[22] , abc[23] , abc[8], abc[9] , abc[6] , abc[7] , abc[13] , abc[15] , abc[12] , abc[14] , abc[16] , abc[17] , abc[10] , abc[11] , abc[20] , abc[21] , abc[18] , abc[19]
        elif move == "L":
            xyz = abc[23] , abc[1] , abc[21] , abc[3] , abc[4] , abc[5] , abc[6] , abc[7] , abc[0], abc[9] , abc[2] , abc[11] , abc[8] , abc[13] , abc[10] , abc[15] , abc[18] , abc[16] , abc[19] , abc[17] , abc[20] , abc[14] , abc[22] , abc[12]
        elif move == "L'":
            xyz = abc[8] , abc[1] , abc[10] , abc[3] , abc[4] , abc[5] , abc[6] , abc[7] , abc[12], abc[9] , abc[14] , abc[11] , abc[23] , abc[13] , abc[21] , abc[15] , abc[17] , abc[19] , abc[16] , abc[18] , abc[20] , abc[2] , abc[22] , abc[0]
        elif move == "B":
            xyz = abc[5] , abc[7] , abc[2] , abc[3] , abc[4] , abc[15] , abc[6] , abc[14] , abc[8], abc[9] , abc[10] , abc[11] , abc[12] , abc[13] , abc[16] , abc[18] , abc[1] , abc[17] , abc[0] , abc[19] , abc[22] , abc[20] , abc[23] , abc[21]
        elif move == "B'":
            xyz = abc[18] , abc[16] , abc[2] , abc[3] , abc[4] , abc[0] , abc[6] , abc[1] , abc[8], abc[9] , abc[10] , abc[11] , abc[12] , abc[13] , abc[7] , abc[5] , abc[14] , abc[17] , abc[15] , abc[19] , abc[21] , abc[23] , abc[20] , abc[22]
        
        return xyz
    
    def applyMoves(self, move, abc):
        xyz = ""
        if move == 'U':
            xyz = abc[2] +  abc[0] + abc[3] +  abc[1]+ abc[20]+ abc[21]+  abc[6]+  abc[7]+  abc[4]+ abc[5] + abc[10]+ abc[11]+ abc[12]+ abc[13]+ abc[14]+ abc[15]+  abc[8]+  abc[9]+abc[18]+ abc[19]+ abc[16]+ abc[17]+ abc[22] + abc[23]
        if move == "U'" or move == "Ui":
            xyz = abc[1] + abc[3] + abc[0] + abc[2] + abc[8] + abc[9] + abc[6] + abc[7] + abc[16] + abc[17] + abc[10] + abc[11] + abc[12] + abc[13] + abc[14] + abc[15] + abc[20] + abc[21] + abc[18] + abc[19] + abc[4] + abc[5] + abc[22] + abc[23]
        if move == "R":
            xyz = abc[0] + abc[9] + abc[2] + abc[11] + abc[6] + abc[4] + abc[7] + abc[5] + abc[8] + abc[13] + abc[10] + abc[15] + abc[12] + abc[22] + abc[14] + abc[20] + abc[16] + abc[17] + abc[18] + abc[19] + abc[3] + abc[21] + abc[1] + abc[23]
        if move == "R'" or move == "Ri":
            xyz = abc[0] + abc[22] + abc[2] + abc[20] + abc[5] + abc[7] + abc[4] + abc[6] + abc[8]+ abc[1] + abc[10] + abc[3] + abc[12] + abc[9] + abc[14] + abc[11] + abc[16] + abc[17] + abc[18] + abc[19] + abc[15] + abc[21] + abc[13] + abc[23]
        if move == "F":
            xyz = abc[0] + abc[1] + abc[19] + abc[17] + abc[2] + abc[5] + abc[3] + abc[7] + abc[10]+ abc[8] + abc[11] + abc[9] + abc[6] + abc[4] + abc[14] + abc[15] + abc[16] + abc[12] + abc[18] + abc[13] + abc[20] + abc[21] + abc[22] + abc[23]
        if move == "F'" or move == "Fi":
            xyz = abc[0] + abc[1] + abc[4] + abc[6] + abc[13] + abc[5] + abc[12] + abc[7] + abc[9]+ abc[11] + abc[8] + abc[10] + abc[17] + abc[19] + abc[14] + abc[15] + abc[16] + abc[3] + abc[18] + abc[2] + abc[20] + abc[21] + abc[22] + abc[23]
        if move == "D":
            xyz = abc[0] + abc[1] + abc[2] + abc[3] + abc[4] + abc[5] + abc[10] + abc[11] + abc[8]+ abc[9] + abc[18] + abc[19] + abc[14] + abc[12] + abc[15] + abc[13] + abc[16] + abc[17] + abc[22] + abc[23] + abc[20] + abc[21] + abc[6] + abc[7]
        if move == "D'" or move == "Di":
            xyz = abc[0] + abc[1] + abc[2] + abc[3] + abc[4] + abc[5] + abc[22] + abc[23] + abc[8]+ abc[9] + abc[6] + abc[7] + abc[13] + abc[15] + abc[12] + abc[14] + abc[16] + abc[17] + abc[10] + abc[11] + abc[20] + abc[21] + abc[18] + abc[19]
        if move == "L":
            xyz = abc[23] + abc[1] + abc[21] + abc[3] + abc[4] + abc[5] + abc[6] + abc[7] + abc[0]+ abc[9] + abc[2] + abc[11] + abc[8] + abc[13] + abc[10] + abc[15] + abc[18] + abc[16] + abc[19] + abc[17] + abc[20] + abc[14] + abc[22] + abc[12]
        if move == "L'" or move == "Li":
            xyz = abc[8] + abc[1] + abc[10] + abc[3] + abc[4] + abc[5] + abc[6] + abc[7] + abc[12]+ abc[9] + abc[14] + abc[11] + abc[23] + abc[13] + abc[21] + abc[15] + abc[17] + abc[19] + abc[16] + abc[18] + abc[20] + abc[2] + abc[22] + abc[0]
        if move == "B":
            xyz = abc[5] + abc[7] + abc[2] + abc[3] + abc[4] + abc[15] + abc[6] + abc[14] + abc[8]+ abc[9] + abc[10] + abc[11] + abc[12] + abc[13] + abc[16] + abc[18] + abc[1] + abc[17] + abc[0] + abc[19] + abc[22] + abc[20] + abc[23] + abc[21]
        if move == "B'" or move == "Bi":
            xyz = abc[18] + abc[16] + abc[2] + abc[3] + abc[4] + abc[0] + abc[6] + abc[1] + abc[8]+ abc[9] + abc[10] + abc[11] + abc[12] + abc[13] + abc[7] + abc[5] + abc[14] + abc[17] + abc[15] + abc[19] + abc[21] + abc[23] + abc[20] + abc[22]
        
        return xyz
    
    def innerPrint(self, abc):
        print("   ",abc[0], abc[1])
        print("   ",abc[2], abc[3]) 
        print(abc[16], abc[17], abc[8], abc[9], abc[4], abc[5],abc[20], abc[21])
        print(abc[18], abc[19], abc[10], abc[11], abc[6], abc[7],abc[22], abc[23])
        print("   ",abc[12], abc[13])
        print("   ",abc[14], abc[15])
        print('\n\n')
    
    def optimize(self, move):
        moves = move.split()
        for i in range(len(moves) - 1):
            if moves[i] == moves[i + 1] + "'":
                moves[i] = ""
                moves[i + 1] = ""
            elif moves[i] + "'" == moves[i + 1]:
                moves[i] = ""
                moves[i + 1] = ""
        return " ".join(moves)

    def applyMove(self, move):
        string = self.string
        string = string.replace(" ", "")
        new_state = ""
        for i in range(24):
            new_state += string[MOVES[move][i]]
        self.string = new_state[0:4] + " " + new_state[4:8] + " " + new_state[8:12] + " " + new_state[12:16] + " " + new_state[16:20] + " " + new_state[20:24]

    def applyMoveStr(self, move):
        moves = move.split()
        for m in moves:
            self.applyMove(m)

    def equals(self, cube):
        return cube.string == "WWWW RRRR GGGG YYYY OOOO BBBB" or cube.string == "BBBB OOOO YYYY GGGG RRRR WWWW" or cube.string == "WWWW OOOO GGGG YYYY RRRR BBBB" or cube.string == "BBBB RRRR YYYY GGGG OOOO WWWW" or cube.string == "WWWW RRRR YYYY GGGG OOOO BBBB" or cube.string == "BBBB OOOO GGGG YYYY RRRR WWWW"

    def bfs(self,start,end):
        M = []											
        P = {start: "START"}								
        Q = deque()												
        F = False												
        counter = 0 
        if start == end:
            return M

        Q.append(start)
        while len(Q) > 0 and F == False:	
            counter += 1				
            x = Q.popleft()

            for i in range(12):
                p = quarter_twists[i]
                y = perm_apply(p, x)

                if y not in P:
                    Q.append(y)
                    P[y] = i

                if y == end:
                    F = True
                    break

        if F == False:											
            M = None
        else:
            z = end
            while P[z] != "START":
                c = quarter_twists[P[z]]

                if P[z] % 2 == 0:							
                    n = quarter_twists[P[z]+1]
                else:											
                    n = quarter_twists[P[z]-1]

                M.append(quarter_twists_names[c])
                z = perm_apply(n, z)

        if (M != None):
            M = M[::-1]

        return M, counter

    def shuffle(self, n):
        for i in range(n):
            self.applyMove(random.choice(self.available_moves))
            
            
    def randomWalk(self, maxMoves):
       
        moves = ""

      
        for i in range(maxMoves):

            move = random.choice(self.available_moves)
            self.applyMove(move)

            moves += " " + move

            if self.equals(self):
                return self.optimize(moves)

        return None
        
    def dls(self, limit):
        
        stack = []
        stack.append(self)
        nodes = 0
        visited = set()
        visited.add(self.string)

        moves = {}
        moves[self.string] = ""

        while len(stack) > 0:

            cube = stack.pop()
            nodes += 1

            if cube.equals(cube):
                return self.optimize(moves[cube.string]), nodes

            if len(moves[cube.string].split()) < limit:

                for move in self.available_moves:

                    new_cube = Cube(cube.string)
                    new_cube.applyMove(move)

                    if new_cube.string not in visited:

                        visited.add(new_cube.string)

                        stack.append(new_cube)

                        moves[new_cube.string] = moves[cube.string] + " " + move
                        
        return None

    def dlsi(self, limit):
        
        stack = []
        stack.append(self)
        nodes = 0
        visited = set()
        visited.add(self.string)

        moves = {}
        moves[self.string] = ""

        while len(stack) > 0:

            cube = stack.pop()
            nodes += 1

            if cube.equals(cube):
                return self.optimize(moves[cube.string]), nodes

            if len(moves[cube.string].split()) < limit:

                for move in self.available_moves:

                    new_cube = Cube(cube.string)
                    new_cube.applyMove(move)

                    if new_cube.string not in visited:

                        visited.add(new_cube.string)

                        stack.append(new_cube)

                        moves[new_cube.string] = moves[cube.string] + " " + move

        return None, nodes
    
    def ids(self,limit):
        
        depth = 0

        totalNodes = 0
        nodes = 0

        while depth<limit:

            solution,nodes = self.dlsi(depth)
            totalNodes += nodes
            if solution != None:
                print("Depth: " + str(depth))
                print("IDS found a solution at depth " + str(depth))
                return solution, totalNodes

            print("Depth: " + str(depth))

            depth += 1
        
        

    def astar(self) :
      
        nodes = 0
        queue = []
        queue.append((self, 0))

        visited = set()
        visited.add(self.string)

        moves = {}
        moves[self.string] = ""

        while True:
            nodes += 1
            
            cube, cost = queue.pop(0)

            if cube.equals(cube):
                return self.optimize(moves[cube.string]), nodes

            for move in self.available_moves:

                new_cube = Cube(cube.string)
                new_cube.applyMove(move)

                if new_cube.string not in visited:

                    visited.add(new_cube.string)

                    queue.append((new_cube, cost + 1))

                    moves[new_cube.string] = moves[cube.string] + " " + move
                
                if len(queue) < 0:
                    break

        return None, nodes

arguments = sys.argv
command = arguments[1]
if len (arguments) > 2:
    arg = arguments[2]
if len(arguments) > 3:
    arg2 = arguments[3]
if len(arguments) > 4:
    arg3 = arguments[4]

cube = Cube()

if command == "shuffle":
    if len(arguments) == 2:
        n = 10
    else:
        n = int(arg)
    cube.shuffle(n)
    cube.print_cube()

if command == "applyMoveStr":
    if len(arguments) == 2:
        move = "U R F U' B L'"
    else:
        move = arg
    cube.applyMoveStr(move)
    cube.print_cube()

if command == "goal":
    if len(arguments) == 2:
        cube = Cube()
    else:
        cube = Cube(arg)
    print(cube.isSolved())

if command == "print":
    if len(arguments) == 2:
        cube = Cube()
    else:
        cube = Cube(arg)
    cube.print_cube()

if command == "randomWalk":
    if len(arguments) == 2:
        n = 10
    else:
        n = int(arg)
    cube.randomWalk(n)
    cube.print_cube()

if arguments[1] == 'bfs':
  moves = arguments[2].split()
  state = cube.clone(cube.no_cube)
  for i in moves:
    state = cube.newMove(i,state)
  start = time.time()
  path, counter = cube.bfs(tuple(state), (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23))
  end = time.time()
  newstate = cube.clone(cube.string.replace(" ",""))
  for k in moves:
    k = k.replace("i","'")
    newstate = cube.applyMoves(k, newstate)
  for j in path:
    newstate = cube.applyMoves(j, newstate)
    cube.innerPrint(newstate)
    
  
  print("PATH found by bfs:" + str(path))
  print("Nodes explored:", counter)
  print('Time taken (in secs) by BFS: ' + str(end - start))
  
  
  
if command == "dls":
    nodes = 0
    if len(arguments) == 2:
        move = "R U R' U R U R'"
        limit = 8
    elif len(arguments) == 3:
        move = arg
        limit = 8
    else:
        move = arg
        limit = int(arg2)
    cube.applyMoveStr(move)
    start = time.time()
    result = cube.dls(limit)
    end = time.time()
    if result == None:
        print('A valid solution could not be found at the depth limit provided. Please try increasing the depth limit')
    else:
        move,nodes = result
        print(move)
        for move in move.split():
            cube.applyMove(move)
            cube.print_cube()
            print("\n")
        print('Nodes Explored: ', nodes)    
        print('Time taken (in secs) by DLS: ', str(end - start))
        

if command == "ids":
    nodes = 0
    if len(arguments) == 2:
        # move = "R U R' U R U R'"
        limit = 10
    elif len(arguments) == 3:
        move = arg
        limit = 10
    else:
        move = arg
        limit = int(arg2)
    cube.applyMoveStr(move)
    start = time.time()
    move,nodes = cube.ids(limit)
    end = time.time()
    print(move)
    for move in move.split():
        cube.applyMove(move)
        cube.print_cube()
        print("\n")
    print('Nodes Explored: ', nodes)
    print('Time taken (in secs) by IDS: ', end - start)

if command == "astar":
    nodes = 0
    if len(arguments) == 2:
        move = "R U R' U R U R'"
    else:
        move = arg
    cube.applyMoveStr(move)
    start = time.time()
    move, nodes = cube.astar()
    end = time.time()
    print(move)
    for move in move.split():
        cube.applyMove(move)
        cube.print_cube()
        print("\n")
    print('Nodes Explored: ', nodes)
    print('Time taken (in secs) by A*: ', end - start)
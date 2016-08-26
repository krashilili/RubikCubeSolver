import numpy as np
import os
import copy

debug = False
class Facelet:
    """A facelet class"""
    def __init__(self, color, num, pos=None):
        self.color = color
        self.num = num
        if pos == None:
            self.pos = None
        else:
            self.pos = pos

    def get_color(self):
        return self.color

    def get_num(self):
        return self.num

    def set_num(self, n):
        self.num = n

    def set_color(self, c):
        self.color = c

    def set_pos(self, p):
        self.pos = p

    def get_pos(self):
        return self.pos
    
    def __repr__(self):
        if self.pos != None:
            return "<color=%s, index=%s, position=(%s,%s)>" \
                   %(self.color,str(self.num),self.pos[0],self.pos[1])
        else:
            return "<color=%s, index=%s, position= None" \
                   %(self.color,str(self.num)) 
        

class Cube:
    colors = ['o','y','r','w','g','b']
    REF_CUBE = False
    """A Cube class"""
    def __init__(self, N, seq=False):
        """Initialize a NxNxN cube."""
        self.N = N
        #a map that mapping the location of a given corner(edge) piece
        #to where it stores in an array
        self.map = self._map_orientation_to_array()
        self.color_to_orientation = lambda x: self._map_color_to_orientation()[x]
        self.refcube = self._ref_cube()
        self.stickercolors = {0:'o',1:'y',2:'r',3:'w',4:'g',5:'b'}
        self.facedict = {'l':0, 'f':1,'r':2,'b':3,'u':4,'d':5}
        
        if seq:
            #a random cube defined by a user
            self.sticker = self._user_defined_cube(N,seq)
        else:
            #a solved cube
            self.sticker = self._ref_cube()
            self.REF_CUBE = True
        
        
        
    def _ref_cube(self):
        """A reference cube which is in a solved state.
            [
             [[L, L, L],
              [L, L, L], --> sticker[0]
              [L, L, L] ],

             [[F..],
               ..,
              [F..]],

             [[R..]],

             [[B..]],
             [[U..]],
             [[D..]]
        ]  
        """
        n=1
        cube = []
        for color in self.colors:
            f = []
            for r in range(self.N):
                row = []
                for c in range(self.N):
                    row.append(Facelet(color,n))
                    n+=1
                f.append(row)
            cube.append(f)
        return cube

    def _user_defined_cube(self, N, seq):
        """The user's cube representation.
            Input sequence follows:
                1. face order: L->F->R->B->U->D
                2. facelet order on a face: top->bottom, left->right
                    e.g.
                        b(46) b(47) b(48)   
                        b(49) b(50) b(51)      
                        b(52) b(53) b(54),   
                    then the order is b(46)->b(47)->b(48)->b(49)->...->b(54)
        @param seq is a dictionary. seq={'l':['r','b',x,...,x],'r':..,]
        @return a representation similar to that in _cube function.
        """
        order = ['l','f','r','b','u','d']
        colors = {'o':5,'y':14,'r':23,'w':32,'g':41,'b':50}
        ps = {'l':[(i,j) for j in range(3,6) for i in range(3)],
                     'f':[(i,j) for j in range(3,6) for i in range(3,6)],
                     'r':[(i,j) for j in range(3,6) for i in range(6,9)],
                     'b':[(i,j) for j in range(3,6) for i in range(9,12)],
                     'u':[(i,j) for j in range(3)   for i in range(3,6)],
                     'd':[(i,j) for j in range(6,9) for i in range(3,6)]}
        cube = []
       
        for o in order:
            facelets = seq[o]
            f = []
            row=[]
            positions = ps[o]
            #each face
            for i, facelet in enumerate(facelets):
                piece_position = positions[i]
                #the central piece
                if i == self.N*self.N/2:
                    row.append(Facelet(facelet,colors[facelet],piece_position))
                    continue
                row.append(Facelet(facelet,'50',piece_position))
                if (i+1)%3 == 0:
                    #each row
                    f.append(row)
                    row=[]
            cube.append(f)

        cube2=np.array(cube)
        corner_edge_pcs = self.map.keys()
        for pc in corner_edge_pcs:
            #get the colors of the corner/edge pieces in the user's cube
            colors = self._get_piece_color(pc, cube)
            #based on the colors from the user's cube, find the same corner/edge piece in reference cube,
            #and return the orientation of the piece 
            o = self.color_to_orientation(colors)
            #get the numbers associated to each faclet in the corner/edge piece in reference cube
            vals = self._get_piece_num(o, self.refcube)
            setvals = [vals[f] for f in colors]
            #set the values to the corner/edge piece in user's cube
            self._set_piece_num(pc, cube, setvals)
        return cube2       
        
    
    def _get_piece_num(self, cp, cube):
        """An internal function used to get the corner/edge piece of a cube.
        @param cp: corner piece by location. e.g. cp='UFR'
        @param cube: a cube representation. the return value either by
                     _user_defined_cube or _ref_cube function.
        @returns a dictionary.e.g. cp is 'luf', then it returns {'l':54,'u':27,'f':25}.
        """
        lc = self._from_orientation_to_array_allocation(cp)
        if len(cp)==2:
            p1 = cube[ lc[0][0]][ lc[0][1]][ lc[0][2]]
            p2 = cube[ lc[1][0]][ lc[1][1]][ lc[1][2]]
            c1,n1 = p1.get_color(), p1.get_num()
            c2,n2 = p2.get_color(), p2.get_num()
            return {c1:n1,c2:n2}
        else:
            p1 = cube[ lc[0][0]][ lc[0][1]][ lc[0][2]]
            p2 = cube[ lc[1][0]][ lc[1][1]][ lc[1][2]]
            p3 = cube[ lc[2][0]][ lc[2][1]][ lc[2][2]]
            return {p1.get_color():p1.get_num(),
                    p2.get_color():p2.get_num(),
                    p3.get_color():p3.get_num()}

    def _get_piece_color(self, cp, cube):
        """An internal function used to get the combination of colors
        of corner/edge piece in a cube.

        @param cp: corner piece by location. e.g. cp='UFR'
        @param cube: a cube representation.
        @returns a string. e.g.  if cp='lfr', it returns `rgb`.
        """
        lc = self._from_orientation_to_array_allocation(cp)
        if len(cp)==2:
            p1 = cube[ lc[0][0]][ lc[0][1]][ lc[0][2]]
            p2 = cube[ lc[1][0]][ lc[1][1]][ lc[1][2]]
            n1 = p1.get_color()
            n2 = p2.get_color()
            return n1+n2
        else:
            p1 = cube[ lc[0][0]][ lc[0][1]][ lc[0][2]]
            p2 = cube[ lc[1][0]][ lc[1][1]][ lc[1][2]]
            p3 = cube[ lc[2][0]][ lc[2][1]][ lc[2][2]]
            return p1.get_color()+p2.get_color()+p3.get_color()
        
    def _set_piece_num(self, cp, cube, vals):
        """An internal function used to set the number of a corner/edge piece.
        @param vals: a list of int. The values in the list are aligned with cp.
                    e.g. if cp='rfu' and vals=[1,2,3], then `1` assign to the index of
                            face `r`
        """
        
        lc = self._from_orientation_to_array_allocation(cp)
        if len(cp)==2:
            p1 = cube[ lc[0][0]][ lc[0][1]][ lc[0][2]]
            p2 = cube[ lc[1][0]][ lc[1][1]][ lc[1][2]]
            p1.set_num(vals[0])
            p2.set_num(vals[1])
        else:
            p1 = cube[ lc[0][0]][ lc[0][1]][ lc[0][2]]
            p2 = cube[ lc[1][0]][ lc[1][1]][ lc[1][2]]
            p3 = cube[ lc[2][0]][ lc[2][1]][ lc[2][2]]
            p1.set_num(vals[0])
            p2.set_num(vals[1])
            p3.set_num(vals[2])
    
    def _center_piece_color(self, post_in_sticker):
        """Find the color of the central piece on a face.
        @param: post_in_sticker is the face location in array sticker. Postion count starts with 0
        @returns the color in char"""
        return self.stickercolors[self.sticker[post_in_sticker][1][1]]

    def _get_center_pieces(self):
        """Get all center pieces in a cube.
        @returns a list of center pieces."""
        cps = []
        for facearray in self.sticker:
            for array in facearray:
                for cell in array:
                    if cell.get_pos() in [(1,4),(4,1),(4,4),(4,7),(7,4),(10,4)]:
                        cps.append(cell)
        return cps

    def turn(self, face, deg_num):
        """Turn the cube around the face 'face' with 'deg_num' 90-degress in the clkwise.
        e.g. 'deg_num' is 1 for 90 degresses in clockwise. 2 for 180 in clkwise.
        -1 for 90-degress turn in counter-clockwise. -2 for 190-degree turn in cnt-clkwise.
        @param face: a char in ('U','D','F','B','R','L')
        @param deg_num: an int in (+/- 1, +/- 2)
        @returns boolean true.
        """

        #turn the cube by layer
        for ly in range(self.N):
            #layer 'ly' turns deg_num*90 degress in clkwise/cnt-clkwise around 'face'
            self.move(face, deg_num, ly)
        return True

    def _rotate(self, args):
        """Internal method for the move() function.
        Rotate the edges."""
        
        edge0 = args[0]        
        edge0Value = self.sticker[edge0]
        #get the positions of the pieces
        dstPos = [piece.get_pos() for piece in edge0Value]      
        otherEdges = args[1:]
        dstEdge = edge0
        
        for srcEdge in otherEdges:
            srcVal = copy.deepcopy(self.sticker[srcEdge])
            #move the srcVal to the destination
            self.sticker[dstEdge] = srcVal 

            #set the piece's position in srcVal be the position of its predecessor
            for i,piece in enumerate(self.sticker[dstEdge]):
                piece.set_pos(dstPos[i]) 
            
            dstEdge = srcEdge
            dstPos = [piece.get_pos() for piece in self.sticker[srcEdge] ]
            
        self.sticker[dstEdge] = edge0Value
        for i, piece in enumerate(self.sticker[dstEdge]):
            piece.set_pos(dstPos[i])
                
        
    def move(self, face, deg_num, ly):
        """Move a layer 'ly' which is parallel to 'face' through 'deg_num'*90 degresses turn
        either in clockwise or counter-clockwise.
        An internal method.
        
        @param face: a char in ('U','D','F','B','R','L')
        @param deg_num: an int in (+/- 1, +/- 2)
        @param ly: an int in (0,1,2). ly=0 is the layer itself, and higher 'ly' values are for
        layers deeper into the cube.
        """
        
        rotationCount = range( (deg_num  + 4) %4)
        currentFace = self.facedict[face.lower()]

        #rotate the layer around the 'U' face through deg_num*90 degrees
        if face.lower() =='u':
         #   print "It's U"
            oppositeFace = self.facedict['d']
            for rotation in rotationCount:
                self._rotate([(self.facedict['F'.lower()], ly, range(self.N)),
                              (self.facedict['R'.lower()], ly, range(self.N)),
                              (self.facedict['B'.lower()], ly, range(self.N)),
                              (self.facedict['L'.lower()], ly, range(self.N))])

        #rotate the layer around the 'D' face
        if face.lower() == 'd':
          #  print "It's D"
            return self.move('U', -deg_num,(self.N-1-ly))

        #rotate the layer around the 'R' face
        if face.lower() == 'r':
           
            ly2 = self.N-1-ly
            assert ly2 < self.N
            for rotation in rotationCount:
                self._rotate([(self.facedict['U'.lower()], range(self.N), ly2),
                              (self.facedict['F'.lower()], range(self.N), ly2),
                              (self.facedict['D'.lower()], range(self.N), ly2),
                              (self.facedict['B'.lower()], range(self.N)[::-1], ly)])
                
        #roate around the 'L' face
        if face.lower() == 'l':
           # print "It's L"
            ly2 = self.N-1-ly
            return self.move('R', -deg_num, ly2)
            
        #roate around the 'F' face
        if face.lower() == 'f':
           # print "It's F"
            ly2 = self.N-1-ly
            assert ly2 < self.N
            for rotation in rotationCount:
                self._rotate([(self.facedict['U'.lower()], ly2, range(self.N)),
                              (self.facedict['L'.lower()], range(self.N)[::-1], ly2),
                              (self.facedict['D'.lower()], ly, range(self.N)[::-1]),
                              (self.facedict['R'.lower()], range(self.N), ly)])
        #roate around the 'B' face
        if face.lower() == 'b':
           # print "It's B"
            return self.move('F',-deg_num, (self.N-1-ly))

    def _move_face(self, f, deg_num):
        """An internal function. When move function called, it does not affect on the face
        that is parallel to the movement. So adding this function.
        """
        rotationCount = range( (deg_num  + 4) %4)
        for rotation in rotationCount:
            self._rotate([(self.facedict[f.lower()], 0, range(self.N)[::-1]),
                          (self.facedict[f.lower()], range(self.N), 0),
                          (self.facedict[f.lower()], 2, range(self.N)),
                          (self.facedict[f.lower()], range(self.N)[::-1],2)])
       
            
    def F(self):
        print "\n*** Turn F. ***\n"
        self.move('F', 1, 0)
        self._move_face('F',1) 

    def F_prime(self):
        print "\n*** Turn F'. ***\n"
        self.move('F', -1, 0)
        self._move_face('F',-1)

    def B(self):
        print "\n*** Turn B. ***\n"
        self.move('B', 1, 0)
        self._move_face('B',1)

    def B_prime(self):
        print "\n*** Turn B'. ***\n"
        self.move('B', -1, 0)
        self._move_face('B',-1) 
        
    def R(self):
        print "\n*** Turn R. ***\n"
        self.move('R', 1, 0)
        self._move_face('R',1)

    def R_prime(self):
        print "\n*** Turn R'. ***\n"
        self.move('R', -1, 0)
        self._move_face('R', -1)

    def L(self):
        print "\n*** Turn L. ***\n"
        self.move('L', 1, 0)
        self._move_face('L',1)

    def L_prime(self):
        print "\n*** Turn L'. ***\n"
        self.move('L', -1, 0)
        self._move_face('L', -1)

    def U(self):
        print "\n*** Turn U. ***\n"
        self.move('U', 1, 0)
        self._move_face('U',1)

    def U_prime(self):
        print "\n*** Turn U'. ***\n"
        self.move('U', -1, 0)
        self._move_face('U',-1)

    def D(self):
        print "\n*** Turn D. ***\n"
        self.move('D', 1, 0)
        self._move_face('D',1)

    def D_prime(self):
        print "\n*** Turn D'. ***\n"
        self.move('D',-1,0)
        self._move_face('D',-1)
        
    def __getitem__(self, args):
        """Get the pieces from the cube."""
        return "The piece:  ", self.sticker[args[0]][args[1]][args[2]]
    
    def __repr__(self):
        """Print the cube.
           dp[0][1]<---.    .--->dp[0][1][0][0] ( and the value '33' is dp[0][1][0][0][0])
                        \  /    
 dp = /  / {[-  -  -],  { [33 34 35],  {[-  -  -], {[-  -  -], \    \
      |  |  [-  -  -],    [36 U  37],   [-  -  -],  [-  -  -], |----|--> dp[0]
      |  \  [-  -  -]},   [38 39 40]},  [-  -  -]}, [-  -  -]} / ,  |----------> line1
            (lineitem)
      |     1  2  3   9  10 11  17 18 19  25 26 27  -->firstarrays(first row) |  
      |     4  L  5   12 F  13  20 R  21  28 B  29                   |  
      |     6  7  8   14 15 16  22 23 24  30 31 32                  ,|---------> line2
        
      |     -  -  -   41 42 43  -  -  -   -  -  -                    |
      |     -  -  -   44 D  45  -  -  -   -  -  -                    |---------> line3
      \     -  -  -   46 47 48  -  -  -   -  -  -                    /

        """
        dp =[[ [ [100,100,100] for k in range(3) ] for j in range(4)] for i in range(3) ]
        
        dp[0][1] = self.sticker[4] #U
        dp[1][0] = self.sticker[0] #L
        dp[1][1] = self.sticker[1] #F
        dp[1][2] = self.sticker[2] #R
        dp[1][3] = self.sticker[3] #B
        dp[2][1] = self.sticker[5] #D

        if debug:
            print dp[0][1]
            print "-"*32
            print self.sticker[4]
            
            
        
        cube ='<User\'s cube: > \n'
        if self.REF_CUBE:
            cube = '<Reference cube: >\n'
        innerlines = [' '*25+'(U)', \
                      ' '*6+'(L)'+' '*16+'(F)'+' '*17+'(R)'+' '*15+'(B)', \
                      ' '*25+'(D)']
        for enum in range(3):
            lines = dp[enum] # e.g. dp[0]
            firstarrays,secondarrays,thirdarrays =[],[],[]

            for lineitem in lines:
                firstarrays.append(lineitem[0])
                secondarrays.append(lineitem[1])
                thirdarrays.append(lineitem[2])
                arrays = [firstarrays,secondarrays,thirdarrays]
            if debug:
                print "-"*32
                print "first arrays \n"
                print firstarrays
                return
                
            for arrayitem in arrays:
                for item in arrayitem:
                    for e in item:
                        if e == 100:
                            cube+='  -   '
                        else:
                            cube+=e.get_color()+"("+str(e.get_num())+") "
                            if e.get_num() <10:
                                cube+=" "
                            
                    cube+=' '
                #finished a face
                cube+='\n'
            cube+=innerlines[enum]
            cube+='\n'
        return cube

    def _from_orientation_to_array_allocation(self, name):
        """An internal function. Applies to reference cube.
        @param name: the orientation of a corner peice or an edge piece. e.g. 'FUR' or 'FR'
        @returns the location where the pieces stores in the array of the reference cube.
            e.g. if `name` is 'FRU', then it returns [[1,0,2],[2,0,0],[4,2,2]]
        """
        
        n = name.lower()
        s0 =[j for j in n]
        s0.sort()
        src ="".join(s0)
        
        for key in self.map:
            s =[i for i in key]
            #keep the mapping info
            #e.g. 'lfu' <--> [ [x,x,x](l), [x,x,x](f), [x,x,x](u)]
            m = {}
            vals = self.map[key]
            for i, face in enumerate(s):
                m[face]= vals[i]
                
            s.sort()
            target="".join(s)

            if src == target:
                req = [k for k in n]
                
                return [m[f] for f in req]

 
    def _map_color_to_orientation(self):
        """An internal function that applies to the reference cube.
        This function is to mapping the combination of colors of corner/edge pieces
        to the orientation where these pieces are.
        @return a dictionary that contains the mapping."""
        m={}
        m['oyg'], m['ogy'],m['yog'],m['ygo'],m['goy'],m['gyo'] = ['lfu' for i in range(6)]
        m['ygr'], m['yrg'],m['ryg'],m['rgy'],m['gyr'],m['gry'] = ['fur' for i in range(6)]
        m['yrb'], m['ybr'],m['ryb'],m['rby'],m['byr'],m['bry'] = ['frd' for i in range(6)]
        m['ybo'], m['yob'],m['byo'],m['boy'],m['oyb'],m['oby'] = ['fdl' for i in range(6)]
        m['ogw'], m['owg'],m['gow'],m['gwo'],m['wgo'],m['wog'] = ['lub' for i in range(6)]
        m['obw'], m['owb'],m['bow'],m['bwo'],m['wbo'],m['wob'] = ['ldb' for i in range(6)]
        m['grw'], m['gwr'],m['rgw'],m['rwg'],m['wgr'],m['wrg'] = ['urb' for i in range(6)]
        m['brw'], m['bwr'],m['wrb'],m['wbr'],m['rwb'],m['rbw'] = ['drb' for i in range(6)]
        m['gy'],m['yg'] = 'uf','fu'
        m['yo'],m['oy'] = 'fl','lf'
        m['yb'],m['by'] = 'fd','df'
        m['yr'],m['ry'] = 'fr','rf'
        m['og'],m['go'] = 'lu','ul'
        m['rg'],m['gr'] = 'ru','ur'
        m['wg'],m['gw'] = 'bu','ub'
        m['ob'],m['bo'] = 'ld','dl'
        m['rb'],m['br'] = 'rd','dr'
        m['wb'],m['bw'] = 'bd','db'
        m['ow'],m['wo'] = 'lb','bl'
        m['rw'],m['wr'] = 'rb','br'
        return m
                            
    def _map_orientation_to_array(self):
        """An internal function. It creates a mapping between the piece location and
        and the location where the pieces are stored in the array of a reference cube.
        """
        
        pool = {}
        #corner pieces
        #case 1 : LFU
        pool['lfu'] =[ [0,0,2], [1,0,0], [4,2,0]]
        #case 2: FRU
        pool['fru'] =[ [1,0,2],[2,0,0],[4,2,2]]
        #case 3: FLD
        pool['fld'] =[ [1,2,0],[0,2,2],[5,0,0]]
        #case 4: FRD
        pool['frd']=[ [1,2,2],[2,2,0],[5,0,2]]
        #case 5: LUB
        pool['lub']=[ [0,0,0],[4,0,0],[3,0,2]]
        #case 6: LDB
        pool['ldb']=[ [0,2,0],[5,2,0],[3,2,2]]
        #case 7: URB
        pool['urb']=[ [4,0,2],[2,0,2],[3,0,0]]
        #case 8: RBD
        pool['rbd']=[ [2,2,2],[3,2,0],[5,2,2]]

        #edge pieces
        #case 1: UF
        pool['uf'] =[[4,2,1],[1,0,1]]
        #UL
        pool['ul'] =[[4,1,0],[0,0,1]]
        #UR
        pool['ur'] =[[4,1,2],[2,0,1]]
        #UB
        pool['ub'] =[[4,0,1],[3,0,1]]
        #LF
        pool['lf']= [[0,1,2],[1,1,0]]
        #LB
        pool['lb']= [[0,1,0],[3,1,2]]
        #LD
        pool['ld']= [[0,2,1],[5,1,0]]
        #FD
        pool['fd']= [[1,2,1],[5,0,1]]
        #FR
        pool['fr']= [[1,1,2],[2,1,0]]
        #DR
        pool['dr']= [[5,1,2],[2,2,1]]
        #DB
        pool['db']= [[5,2,1],[3,2,1]]
        #RB
        pool['rb']= [[2,1,2],[3,1,0]]
        return pool
        
    def _map_corners_edges(self):
        """An internal function. It returns a dictionary that has the array allocations
        for corner pieces and edge pieces in the cube.
        """
        #corner faclets, 8 pieces in total
        
        pool = {}
        corners=np.array([ [[10,10,10] for j in range(3) ] for i in range(8)])
        edges=np.array([ [[10,10,10] for m in range(2)] for n in range(12)])
        #case 1 : LFU
        corners[0][0]=[0,0,2] #L
        corners[0][1]=[1,0,0]
        corners[0][2]=[4,2,0]
        #case 2: FRU
        corners[1][0]=[1,0,2]
        corners[1][1]=[2,0,0]
        corners[1][2]=[4,2,2]
        #case 3: FLD
        corners[2][0]=[1,2,0]
        corners[2][1]=[0,2,2]
        corners[2][2]=[5,0,0]
        #case 4: FRD
        corners[3][0]=[1,2,2]
        corners[3][1]=[2,2,0]
        corners[3][2]=[5,0,2]
        #case 5: LUB
        corners[4][0]=[0,0,0]
        corners[4][1]=[4,0,0]
        corners[4][2]=[3,0,2]
        #case 6: LDB
        corners[5][0]=[0,2,0]
        corners[5][1]=[5,2,0]
        corners[5][2]=[3,2,2]
        #case 7: URB
        corners[6][0]=[4,0,2]
        corners[6][1]=[2,0,2]
        corners[6][2]=[3,0,0]
        #case 8: RBD
        corners[7][0]=[2,2,2]
        corners[7][1]=[3,2,0]
        corners[7][2]=[5,2,2]
        #edge pieces
        #case 1: UF
        edges[0][0],edges[0][1]=[4,2,1],[1,0,1]
        #UL
        edges[1][0],edges[1][1]=[4,1,0],[0,0,1]
        #UR
        edges[2][0],edges[2][1]=[4,1,2],[2,0,1]
        #UB
        edges[3][0],edges[3][1]=[4,0,1],[3,0,1]
        #LF
        edges[4][0],edges[4][1]=[0,1,2],[1,1,0]
        #LB
        edges[5][0],edges[5][1]=[0,1,0],[3,1,2]
        #LB
        edges[6][0],edges[6][1]=[0,2,1],[5,1,0]
        #FD
        edges[7][0],edges[7][1]=[1,2,1],[5,0,1]
        #FR
        edges[8][0],edges[8][1]=[1,1,2],[2,1,0]
        #DR
        edges[9][0],edges[9][1]=[5,1,2],[2,2,1]
        #DB
        edges[10][0],edges[10][1]=[5,2,1],[3,2,1]
        #RB
        edges[11][0],edges[11][1]=[2,1,2],[3,1,0]

        pool['corner']=corners
        pool['edge']=edges
        return pool
    
        for case in corners:
            f1 = cube[case[0][0] ][ case[0][1] ][ case[0][2] ]
            f2 = cube[case[1][0] ][ case[1][1] ][ case[1][2] ]
            f3 = cube[case[2][0] ][ case[2][1] ][ case[2][2] ]
                
            c1,c2,c3=f1.get_color(),f2.get_color(),f3.get_color()
            n1,n2,n3=f1.get_num(),f2.get_num(),f3.get_num()
            pool[c1+c2+c3]={c1:n1,c2:n2,c3:n3}
        for edge in edges:
            f1 = cube[edge[0][0] ][ edge[0][1] ][ edge[0][2]]
            f2 = cube[edge[1][0] ][ edge[1][1] ][ edge[1][2]]
            c1,c2=f1.get_color(),f2.get_color()
            n1,n2=f1.get_num(),f2.get_num()
            pool[c1+c2]={c1:n1,c2:n2}
        return pool

    def get_edge_pieces(self):
        """Get the edge pieces in the cube.
        @returns a list of edge pieces.
        """
        edges = self._map_corners_edges()['edge']
        cont = []
        for edge in edges:    
            pc1 = self.sticker[edge[0][0],edge[0][1],edge[0][2]]
            pc2 = self.sticker[edge[1][0],edge[1][1],edge[1][2]]
            cont.append((pc1,pc2))
        return cont

    def get_corner_pieces(self):
        """Get all corner pieces in the cube.
        @return a list of corner pieces.
        """
        corners = self._map_corners_edges()['corner']
        cont = []
        for corner in corners:
            pc1 = self.sticker[corner[0][0],corner[0][1],corner[0][2]]
            pc2 = self.sticker[corner[1][0],corner[1][1],corner[1][2]]
            pc3 = self.sticker[corner[2][0],corner[2][1],corner[2][2]]
            cont.append((pc1,pc2,pc3))
        return cont

    def get_center_piece(self, f):
        """Get the color of the middle piece on a face.
        @param f: char. e.g. 'U'
        @return a Facelet instance.
        """
        face = self.facedict[f.lower()]
        return self.sticker[face,1,1]
        
    def get_piece_by_num(self, num):
        """Get the piece by its index.
        @param num: int.
        @returns a Facelet instance."""
        for facearray in self.sticker:
            for array in facearray:
                for cell in array:
                    if cell.get_num() == num:
                        return cell

    def get_edge_piece_by_one_piece_member(self, pm):
        """Get the edge piece which has two piece members by one of members.
        @param pm: a facelet instance.
        @returns a tuple of two member pieces."""
        edges = self.get_edge_pieces()

        for edge in edges:
            for pieceMem in edge:
                if pieceMem.get_num() == pm.get_num():
                    return edge

    def get_edge_pieces_in_middle_layer(self):
        ps = [[(1, 5), (3, 7)], [(4, 5), (4, 6)], [(10, 5),(4, 8)], [(7, 5), (5, 7)],[(2,4),(3,4)],[(5,4),(6,4)],[(8,4),(9,4)],[(11,4),(0,4)]]

        midEdgePieces = []
        for edgePiece in ps:
            p1 = self.get_piece_by_location(edgePiece[0])
            p2 = self.get_piece_by_location(edgePiece[1])
            midEdgePieces.append((p1, p2))
        return midEdgePieces

    def get_piece_by_location(self, lc):
        """An internal function used to get the piece using its location.
        @param lc: a tuple. e.g. (3,5)
        @returns a Facelet instance at location `lc`.
        """
        for facearray in self.sticker:
            for array in facearray:
                for cell in array:
                    if cell.get_pos() == lc:
                        return cell

    def get_center_piece_by_corner_piece(self, cp):
        """Get the center piece of the face where the given one member `cp` in the corner piece is on.
        @param cp: an instance of the Facelet object.
        @returns a Facelet instance."""
        cp_loc = cp.get_pos()
        
        if cp_loc in [(3,0),(3,2),(5,0),(5,2)]:
            return self.get_piece_by_location((4,1))
        if cp_loc in [(0,3),(2,3),(0,5),(2,5)]:
            return self.get_piece_by_location((1,4))
        if cp_loc in [(3,3),(3,5),(5,3),(5,5)]:
            return self.get_piece_by_location((4,4))
        if cp_loc in [(6,3),(6,5),(8,3),(8,5)]:
            return self.get_piece_by_location((7,4))
        if cp_loc in [(9,3),(9,5),(11,3),(11,5)]:
            return self.get_piece_by_location((10,4))
        if cp_loc in [(3,6),(3,8),(5,6),(5,8)]:
            return self.get_piece_by_location((4,7))

    def get_center_piece_by_edge_piece(self, ep):
        """Get the center piece by one pc member of the edge piece which is on the same face with the centre piece.
        @param ep: a facelet instance.
        @returns a facelet instance."""
        ep_loc = ep.get_pos()
        if ep_loc in [(4,0),(4,2),(3,1),(5,1)]: #U
            return self.get_piece_by_location((4,1))
        if ep_loc in [(1,3),(1,5),(0,4),(2,4)]: #L
            return self.get_piece_by_location((1,4))
        if ep_loc in [(4,3),(4,5),(3,4),(5,4)]: #F
            return self.get_piece_by_location((4,4))
        if ep_loc in [(4,6),(4,8),(3,7),(5,7)]: #D
            return self.get_piece_by_location((4,7))
        if ep_loc in [(7,3),(7,5),(6,4),(8,4)]: #R
            return self.get_piece_by_location((7,4))
        if ep_loc in [(10,3),(10,5),(9,4),(11,4)]: #B
            return self.get_piece_by_location((10,4))

    def get_center_piece_of_face_one_piece_should_be(self, p):
        """Get the center piece of the face where the `p` piece should be on.
        @param p: is a facelet instance.
        @returns a facelt instance which is the center piece."""
        cps = self._get_center_pieces()
        for piece in cps:
            if piece.get_color() == p.get_color():
                return piece

    def get_center_piece_by_location_description(self, loc):
        """Get the center piece by giving the location where the center piece is.
        @param loc: 'L', 'R', etc.
        @returns the center piece."""
        if loc.lower() == 'l':
            return self.get_piece_by_location((1,4))
        elif loc.lower() == 'f':
            return self.get_piece_by_location((4,4))
        elif loc.lower() == 'r':
            return self.get_piece_by_location((7,4))
        elif loc.lower() == 'b':
            return self.get_piece_by_location((10,4))
        elif loc.lower() == 'u':
            return self.get_piece_by_location((4,1))
        elif loc.lower() == 'd':
            return self.get_piece_by_location((4,7))

    def get_corner_piece_by_one_piece_member(self, pm):
        """Get the corner piece (3 members) by one piece member.
        @param pm: is an facelet instance.
        @returns the corner piece where the `pm` is in. A tuple of three pieces."""
        cornerPieces = self.get_corner_pieces()
        for cornerPiece in cornerPieces:
            for piece in cornerPiece:
                if piece.get_num() == pm.get_num():
                    return cornerPiece

    def get_face_location_by_piece(self, p):
        """Get the face (L, F, R..) where the facelet instance `p` is.
        @param p: is a facelet instance.
        @returns a char. e.g. "L".
        """
        x = p.get_pos()[0]
        y = p.get_pos()[1]
        if x>=0 and x<=2:
            return 'L'
        if x>=3 and x<=5:
            if y>=0 and y<=2: return "U"
            if y>=3 and y<=5: return "F"
            if y>=6 and y<=8: return "D"
        if x>=6 and x<=8:
            return "R"
        if x>=9 and x<=11:
            return "B"

    def get_face_facelets_by_center_piece_num(self, n):
        """Get the facelets by the index of the center piece on that face.
        @param n: the index of the center piece.
        @returns a array of three rows."""
        piece = self.get_piece_by_num(n)
        loc = self.facedict[self.get_face_location_by_piece(piece).lower()]
        return self.sticker[loc]

    def get_opposite_face_location_by_piece(self, p):
        """Given a facelet `p`, it returns the face that opposites to the face `p` is on.
        @param p: is a facelet instance
        @return a char: 'L', 'R', etc."""
        oppFace = {'L':'R','R':'L',
                   'U':'D','D':'U',
                   'F':'B','B':'F'}
        return oppFace[self.get_face_location_by_piece(p)]

#add something somethng
def test():
    usercube = {
            'l':['b','o','r','y','g','b','g','b','r'],
            'f':['y','r','o','y','w','r','g','o','y'],
            'r':['w','g','o','w','b','y','o','r','r'],
            'b':['b','o','r','g','y','o','y','b','w'],
            'u':['w','g','y','b','o','w','b','y','b'],
            'd':['w','w','g','r','r','g','o','w','g']
        }
    #refcube = Cube(3)
    #print refcube
    #some changes
    usr = Cube(3,usercube)
    print usr
    one = usr.get_piece_by_num(10)
    print one
    print  usr.get_center_piece_by_one_face_piece(one)
    return

    

#if __name__ == '__main__':
#    test()
    

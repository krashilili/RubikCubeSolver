from Cube import Cube
import copy

debug = False
class Algorithm:
    """The algorithm of solving the rubik's cube.
       And it returns a solution.
    """

    def __init__(self, cube):
        """Initialize an alogrithm instance by inputing a cube.
        @param cube: cube is an instance of class Cube.
        """
        self.cube = cube
        self.solution =[]

    def _manipulation(self, f, n):
        """An internal function used to perform rotations around face `f`.
        @param f: is the face to be manipulated on. e.g. "F" or "U'"
        @param n: is the times of the rotation.
        """
        operation = { "L": self.cube.L, "L'":self.cube.L_prime,
                      "R": self.cube.R, "R'":self.cube.R_prime,
                      "F": self.cube.F, "F'":self.cube.F_prime,
                      "B": self.cube.B, "B'":self.cube.B_prime,
                      "U": self.cube.U, "U'":self.cube.U_prime,
                      "D": self.cube.D, "D'":self.cube.D_prime}   
        for t in range(n):
            operation[f.upper()]()
            self.solution.append(f.upper())
        #    print self.cube

    def _get_edge_pieces_by_color(self, c):
        """An internal function used to find the edge piece that has one facelet's color is `c`.
        @returns a list that has all edge pieces within each one there is one facelet in color `c`.
        """
        eps = self.cube.get_edge_pieces()
        pieces = []
        for ep in eps:
            for piece in ep:
                if piece.get_color() == c:
                    pieces.append(piece)
        return pieces

    def _get_corner_pieces_by_color(self, c):
        """An internal function used to find all corner pieces within each piece there is one facelet
        is in color `c`.
        @return a list of corner pieces.
        """
        cornerPieces = self.cube.get_corner_pieces()
        cont = []

        for cps in cornerPieces:
            for p in cps:
                if p.get_color() == c:
                    cont.append(cps)
        return cont


 #--> top cross


#---> the first layer cross
    def _top_cross(self):
        """An internal function which used to make a cross on the
            face `U`.
            first, form a cross without center on the opposite side of `U`.
            second, rotate each face to form a cross on `U`.
        """
        debugTC = False
        permutation = { (3,4):["L",1], (3,1):["L'",2],(11,4):["L'",1], #-> (3,7)
                        (4,0):["B",2], (0,4):["B",1], (8,4): ["B'",1], #->(4,8)
                        (2,4):["F'",1],(6,4):["F",1], (4,2): ["F",2], #->(4,6)
                        (5,4):["R'",1],(5,1):["R",2], (9,4): ["R",1], #->(5,7)
                        (1,3):["L",1], (1,5):["L",1], #->(0,4) or (2,4)
                        (4,3):["F",1], (4,5):["F",1], #->(3,4) or (5,4)
                        (7,3):["R",1], (7,5):["R",1], #->(6,4) or (8,4)
                        (10,3):["B",1],(10,5):["B",1],#->(9,4) or (11,4)
                        (4,0):["U",1], (4,2):["U",1]  #->(3,1) or (5,1)
                       }
       
        
        def _oppositeEdgeAffected(f, edgePieces):
            for p in edgePieces:
                if f.lower()=='l' and p.get_pos()==(3,7):
                    return True
                if f.lower()=='r' and p.get_pos()==(5,7):
                    return True
                if f.lower()=='b' and p.get_pos()==(4,8):
                    return True
                if f.lower()=='f' and p.get_pos()==(4,6):
                    return True
            return False

        def _avoidImpact(f, e, c):
            for i in range(3):
                if _oppositeEdgeAffected(f,e):
                    print "Avoiding impact. Perform D."
                    self._manipulation('D',1)
                    e = self._get_edge_pieces_by_color(c)
                if not _oppositeEdgeAffected(f,e):
                    break
            return True
        
        #top cross
     
            
        centerPiece = self.cube.get_center_piece('U')
        edgePieces = self._get_edge_pieces_by_color(centerPiece.get_color())
        deadloop = 0
        for i, currPiece in enumerate(edgePieces):
            #manipulate on the piece until it's in the right place
            currPieceIndex = currPiece.get_num()
            if debugTC:
                print "!"*60
                print "Working on the %s piece: " %i
                print "Piece : ",
                print currPiece
                print "!"*60
            
            while(True):
                deadloop +=1
                if deadloop > 10:
                    print "The program flies in _top_cross function !!"
                    break
                #the current location of the piece
                ep = self.cube.get_piece_by_num(currPieceIndex)
                edgePieces = self._get_edge_pieces_by_color(centerPiece.get_color())
                
                #the piece is at the right position 
                if ep.get_pos() in [(3,7),(4,8),(4,6),(5,7)]:
                    if debugTC:
                        print "-"*70
                        print "Piece : ",ep,
                        print " is in the right place.!!!"
                        print "-"*70
                        print self.cube
                        print "\n\n"
                    break
                    
                
                dr = permutation[ep.get_pos()][0]
                rep = permutation[ep.get_pos()][1] 

                for face in ['L','R','F','B','U']:
                    if face in dr and _avoidImpact(face, edgePieces,centerPiece.get_color()):
                        self._manipulation(dr, rep)

        if debugTC:
            print "Rotate to top!!"
            print self.cube
        #rotate the bottom cross to top
        edgePieces = self._get_edge_pieces_by_color(centerPiece.get_color())
        for currEdgePiece in edgePieces:
            currPieceIndex = currEdgePiece.get_num()
            twinPiece = None
            loop = 0
            while(True):
                loop+=1
                epiece = self.cube.get_piece_by_num(currPieceIndex)
                twinPieces = self.cube.get_edge_piece_by_one_piece_member(epiece)

                for twin in twinPieces:
                    if twin.get_num() != currPieceIndex:
                        twinPiece = twin

                if twinPiece.get_color() == self.cube.get_center_piece_by_edge_piece(twinPiece).get_color() \
                        or loop > 5:
                    break
                else:
                    self._manipulation('D', 1)

            f = self.cube.get_face_location_by_piece(twinPiece)
            self._manipulation(f, 2)




# 2 --> top layer

 #--> top layer

    def _get_wrong_corner_pieces_on_top(self,centerPiece, cornerPieces):
            #corner piece is on the top layer, but not in the right position
            
            cornerPieces = self._get_corner_pieces_by_color(centerPiece.get_color())

            #the piece in top center piece's color is on the top layer, but not on top face
            tmp = [[cps for piece in cps if piece.get_pos() in [(0,3),(2,3),(3,3),(5,3),(6,3),(8,3),(9,3),(11,3)] \
                           and piece.get_color() == centerPiece.get_color()] for cps in cornerPieces ]
            cpsOnTopLayer = [ p[0] for p in tmp if len(p)>0]

            #in the corner piece, the piece that is in top center piece's color is in
            #the right place, but the other two are not.
            for cps in cornerPieces:
                for piece in cps:
                    if piece.get_pos() in [(3,0),(3,2),(5,0),(5,2)] \
                       and piece.get_color() == centerPiece.get_color():
                        theOtherTwo = [ p for p in cps if p.get_color() != piece.get_color()]
                        if piece.get_pos() == (3,0):
                            if theOtherTwo[0].get_pos() == (0,3) and theOtherTwo[0].get_color() != self.cube.get_piece_by_location((1,4)).get_color() or\
                               theOtherTwo[0].get_pos() == (11,3) and theOtherTwo[0].get_color() != self.cube.get_piece_by_location((10,4)).get_color():
                                cpsOnTopLayer.append(cps)
                        if piece.get_pos() == (5,0):
                            if theOtherTwo[0].get_pos() == (8,3) and theOtherTwo[0].get_color() != self.cube.get_piece_by_location((7,4)).get_color() or\
                               theOtherTwo[0].get_pos() == (9,3) and theOtherTwo[0].get_color() != self.cube.get_piece_by_location((10,4)).get_color():
                                cpsOnTopLayer.append(cps)
                        if piece.get_pos() == (5,2):
                            if theOtherTwo[0].get_pos() == (5,3) and theOtherTwo[0].get_color() != self.cube.get_piece_by_location((4,4)).get_color() or\
                               theOtherTwo[0].get_pos() == (6,3) and theOtherTwo[0].get_color() != self.cube.get_piece_by_location((7,4)).get_color():
                                cpsOnTopLayer.append(cps)
                        if piece.get_pos() == (3,2):
                            if theOtherTwo[0].get_pos() == (2,3) and theOtherTwo[0].get_color() != self.cube.get_piece_by_location((1,4)).get_color() or\
                               theOtherTwo[0].get_pos() == (3,3) and theOtherTwo[0].get_color() != self.cube.get_piece_by_location((4,4)).get_color():
                                cpsOnTopLayer.append(cps)
            if debug:
                print "---->\n"
                print "\t _get_wrong_corner_pieces_on_top\n"
                print "\t Piece: ",
                print cpsOnTopLayer
                print "\n"
            return cpsOnTopLayer

    def _swap_wrong_top_corner_piece_to_bottom(self, topCenterPiece, topCornerPiece):
        #swap the corner piece which is on the top layer, and one piece member in top center piece's color,
        #but other two pieces are not in the right position
        if debug:
            print "\n--->"
            print "\t _swap_wrong_top_corner_piece_to_bottom"
            print "\t Piece: ",
            print topCornerPiece
            print "\n"
        topCornerPieceNum = topCornerPiece[0].get_num()
        for piece in topCornerPiece:
            if piece.get_pos() in [(0,3),(3,0),(11,3)]:
                self._manipulation("L'",1)
                self._manipulation("D",1)
                self._manipulation("L",1)
                self._manipulation("D'",1)
                break
            if piece.get_pos() in [(5,0),(8,3),(9,3)]:
                self._manipulation("R",1)
                self._manipulation("D",1)
                self._manipulation("R'",1)
                self._manipulation("D'",1)
                break
            if piece.get_pos() in [(2,3),(3,3),(3,2)]:
                self._manipulation("L",1)
                self._manipulation("D",1)
                self._manipulation("L'",1)
                self._manipulation("D'",1)
                break
            if piece.get_pos() in [(5,2),(5,3),(6,3)]:
                self._manipulation("R'",1)
                self._manipulation("D",1)
                self._manipulation("R",1)
                self._manipulation("D'",1)
                break
        return self.cube.get_corner_piece_by_one_piece_member( \
                    self.cube.get_piece_by_num(topCornerPieceNum))
                
                
        topCornerPieceNum = topCornerPiece[0].get_num()
        theOtherTwo = []
        for piece in topCornerPiece:
            if topCenterPiece.get_color() != piece.get_color():
                theOtherTwo.append(piece)
        pieceX = self.cube.get_center_piece_by_corner_piece(theOtherTwo[0])
        pieceY = self.cube.get_center_piece_by_corner_piece(theOtherTwo[1])

        if debug:
            print "PieceX: ",
            print pieceX
            print "PieceY: ",
            print pieceY
            print "\n"
        if self.is_on_right(pieceX, pieceY):
            #pieceY is on the right hand of pieceX
            Y = self.cube.get_face_location_by_piece(pieceY)
            Y_prime = Y+"'"
            self._manipulation(Y_prime,1)
     #       print self.cube
            self._manipulation("D",1)
     #       print self.cube
            self._manipulation(Y,1)
     #       print self.cube
            self._manipulation("D'",1)
     #       print self.cube
        else:
            X0 = self.cube.get_face_location_by_piece(pieceX)
            X0_prime = X0+"'"
            self._manipulation(X0,1)
     #       print self.cube
            self._manipulation("D",1)
     #       print self.cube
            self._manipulation(X0_prime,1)
     #       print self.cube
            self._manipulation("D'",1)
        return self.cube.get_corner_piece_by_one_piece_member( \
            self.cube.get_piece_by_num(topCornerPieceNum))

    def _bottom_corner_piece_to_right_corner(self, currCornerPiece):
        #on bottom, rotate the bottom corner piece to the right corner
        #param `currPiece` is a corner piece on bottom, but it is not on the right corner
        if debug:
            print "\n"
            print "--->"
            print "\t __bottom_corner_piece_to_right_corner \n",
            print currCornerPiece
        onePieceMember = currCornerPiece[0]
        cnt=0
        while(True):
            if cnt >5:
                print "!"*32,
                print "Program files in _bottom_corner_piece_on_right_corner() function."
                print "!"*32
                break
            cnt +=1
            faceColors =set( [ self.cube.get_center_piece_by_corner_piece(piece).get_color() for piece in currCornerPiece])
            cornerPieceColors = set([ piece.get_color() for piece in currCornerPiece])
            diff = faceColors.intersection(cornerPieceColors)
            if len(diff)==2:
                return currCornerPiece
            elif faceColors == cornerPieceColors:
               
                return None
            else:
                #perform a D rotation
                self.cube.D()
                self.solution.append('D')
            currCornerPiece = self.cube.get_corner_piece_by_one_piece_member(onePieceMember)
        return currCornerPiece
    
    def _is_on_right(self,cpL, cpR):
        """An internal function used to determine if center piece `cpR` is on the right hand of `cpL`."""
        if cpL.get_pos() in [(4,4),(7,4)]:
            if cpR.get_pos()[0] > cpL.get_pos()[0]:
                return True
            else:
                return False
        if cpL.get_pos()[0] == 1:
            if cpR.get_pos()[0] == 4:
                return True
            if cpR.get_pos()[0] == 10:
                return False
        if cpL.get_pos()[0] == 10:
            if cpR.get_pos()[0] == 1:
                return True
            if cpR.get_pos()[0] == 7:
                return False

#---> the top layer
    def _top_layer(self):
        """An internal function in algorithm class. It is to make
            the first layer in the cube done.
        """
        print "\n"
        print "#" * 32
        print "----> In _top_layer function!!! \n"
        topCrossCenterPiece = self.cube.get_center_piece('U')
        cnt = 0
        currCornerPieceOnBottom = None
        currCornerPieceOnBottomOneMemberNum = None
        rightPieces = []
        debugTopLayer = True

        while(True):
            cnt +=1 
            #the condition in which it jumps out of the loop
            facelets = self.cube.get_face_facelets_by_center_piece_num(topCrossCenterPiece.get_num())
            if len(rightPieces) == 4 or\
               cnt >6:
                return

            if currCornerPieceOnBottomOneMemberNum != None:
                currCornerPieceOnBottom = self.cube.get_corner_piece_by_one_piece_member(\
                    self.cube.get_piece_by_num(currCornerPieceOnBottomOneMemberNum))
                
      #      print "%"*32
      #      print currCornerPieceOnBottom
      #      print "\n"
            
      #      if currCornerPieceOnBottom != None:
      #          print "curr[0]: ",
      #          print currCornerPieceOnBottom[0].get_color()
      #          print "center[0]: ",
      #          print self.cube.get_center_piece_by_corner_piece(currCornerPieceOnBottom[0]).get_color()
      #          print "\n"
      #      print "%"*32
            
            if (currCornerPieceOnBottom != None) and\
               (currCornerPieceOnBottom[0].get_color() == self.cube.get_center_piece_by_corner_piece(currCornerPieceOnBottom[0]).get_color()) and \
               (currCornerPieceOnBottom[1].get_color() == self.cube.get_center_piece_by_corner_piece(currCornerPieceOnBottom[1]).get_color()) and \
               (currCornerPieceOnBottom[2].get_color() == self.cube.get_center_piece_by_corner_piece(currCornerPieceOnBottom[2]).get_color()) :
                rightPieces.append(currCornerPieceOnBottom)

                if debugTopLayer:
                    print "#"*32
                    print "Piece in the right place: \n",
                    print currCornerPieceOnBottom,
                    print "\n"
                    print "#"*32
            
                
            #get a current corner piece to work on
            cornerPieces = self._get_corner_pieces_by_color(topCrossCenterPiece.get_color())
            totalCornerPieces = self.cube.get_corner_pieces()

            if debugTopLayer:
                print "----| "
                print "cornerPieces : ",
                print cornerPieces
                print "rightPieces : ",
                print rightPieces
            if rightPieces != None: #remove the corner pieces which are already in the right place
                for rcp in rightPieces:
                    pieceMem = self.cube.get_piece_by_num(rcp[0].get_num())
                    nrcp = self.cube.get_corner_piece_by_one_piece_member(pieceMem)
                    cornerPieces.remove(nrcp)

                    if debugTopLayer:
                        print "remove Piece: \n",
                        print nrcp
                        print "from the corner pieces."

            cornerPiecesOnTop = self._get_wrong_corner_pieces_on_top(topCrossCenterPiece, totalCornerPieces )
            
            if len(cornerPiecesOnTop) != 0:
                currCornerPiece = self._swap_wrong_top_corner_piece_to_bottom(topCrossCenterPiece, cornerPiecesOnTop[0])
            else:
                if debugTopLayer:
                    print "|"*32
                    print "corner piece on top is none!"
                    print "|"*32
                if len(cornerPieces)==0:
                    break
                currCornerPiece = cornerPieces.pop()

            if debugTopLayer:
                print self.cube
                print "\n"
                print "$"*32
                print "Current corner piece: \n",
                print currCornerPiece
                print "$"*32
            
            currCornerPieceOnBottom = self._bottom_corner_piece_to_right_corner(currCornerPiece)                  

            if currCornerPieceOnBottom != None:
                currCornerPieceOnBottomOneMemberNum = currCornerPieceOnBottom[0].get_num()
            else:
                currCornerPieceOnBottomOneMemberNum = None

            if debugTopLayer:
                print "\n\n"
                print "-"*32
                print "Currently working on : ",
                print currCornerPieceOnBottom
                print "-"*32
                print "\n\n"

            # working on the corner piece on bottom
            if currCornerPieceOnBottom != None:
                for piece in currCornerPieceOnBottom:
                    if debugTopLayer:
                        print "Piece : ",
                        print piece

                    #case 1 and 2
                    if piece.get_color() == topCrossCenterPiece.get_color() and \
                       self.cube.get_center_piece_by_corner_piece(piece).get_pos() != (4,7):
                        pieceX, pieceY = None, None
                        pieceX = self.cube.get_center_piece_by_corner_piece(piece)

                        for p in currCornerPieceOnBottom:
                            if p.get_color() != pieceX.get_color() and p != piece:
                                pieceY = self.cube.get_center_piece_by_corner_piece(p)

                        if debugTopLayer:
                            print "Case 1 and 2 "
                            print "pieceX: ",
                            print pieceX
                            print "pieceY: ",
                            print pieceY

                        Y = self.cube.get_face_location_by_piece(pieceY)
                        Y_prime = Y+"'"
                        if self._is_on_right(pieceX, pieceY):
                            
                            # X1(-1) D(-1) X1 D
                            self._manipulation("D'",1)
                            self._manipulation(Y_prime,1)
                            self._manipulation('D',1)
                            self._manipulation(Y,1)
                            break
                        
                        else:#X0 D X0(-1) D(-1)
                            self._manipulation('D',1)
                            self._manipulation(Y,1)
                            self._manipulation("D'",1)
                            self._manipulation(Y_prime,1)
                            break
                    #case 3 and 4
                    if piece.get_color() == topCrossCenterPiece.get_color() and \
                       self.cube.get_center_piece_by_corner_piece(piece).get_pos() == (4,7):
                        pieceTmp = [p for p in currCornerPieceOnBottom if p != piece]
                    
                        print self.cube
                        pieceX = self.cube.get_center_piece_by_corner_piece(pieceTmp[0])
                        pieceY = self.cube.get_center_piece_by_corner_piece(pieceTmp[1])

                        if debugTopLayer:
                            print "Case 3 and 4 "
                            print "pieceX: ",
                            print pieceX
                            print "pieceY: ",
                            print pieceY

                        if self._is_on_right(pieceX, pieceY):# Y is on the right to X
                            x = self.cube.get_face_location_by_piece(pieceX)
                            x_prime = x+"'"
                            self._manipulation("D",1)
                            self._manipulation(x,1)
                            self._manipulation("D'",2)
                            self._manipulation(x_prime,1)
                            break
                        
                        else: # X is on the right to Y
                            y = self.cube.get_face_location_by_piece(pieceY)
                            y_prime = y+"'"
                            self._manipulation("D",1)
                            self._manipulation(y,1)
                            self._manipulation("D'",2)
                            self._manipulation(y_prime,1)
                            break
                            
                #print self.cube
                   
#--> middle layer

 #--> middle layer

    def _get_edge_piece_member_on_left(self, edgePiece):
        # get the piece member on the left in a edge piece
        ep1 = edgePiece[0]
        ep2 = edgePiece[1]
        if ep2.get_pos() in [(3,4),(6,4),(9,4)]and ep2.get_pos()[1] > ep1.get_pos()[1]:
            return ep1
        if ep1.get_pos() in [(3, 4), (6, 4), (9, 4)] and ep1.get_pos()[1] > ep2.get_pos()[1]:
            return ep2
        if ep2.get_pos()[0] == 0:
            return ep1
        if ep1.get_pos()[0]==0:
            return ep2


#---> solve the second layer
    def _mid_layer(self):
        """Solve the second layer."""
        debugML = False

        print "\n"
        print "#" * 32
        print "---->  In _mid_layer function !!\n"
        # find the edge pieces that should be in the middle layer
        loopCnt = 0
        while(True):
            loopCnt +=1
            if loopCnt > 6 or \
                self.cube.get_piece_by_location((0,4)).get_color() == self.cube.get_center_piece_by_location_description('L').get_color() and \
                self.cube.get_piece_by_location((2,4)).get_color() == self.cube.get_center_piece_by_location_description('L').get_color() and \
                self.cube.get_piece_by_location((3,4)).get_color() == self.cube.get_center_piece_by_location_description('F').get_color() and \
                self.cube.get_piece_by_location((5,4)).get_color() == self.cube.get_center_piece_by_location_description('F').get_color() and \
                self.cube.get_piece_by_location((6,4)).get_color() == self.cube.get_center_piece_by_location_description('R').get_color() and \
                self.cube.get_piece_by_location((8,4)).get_color() == self.cube.get_center_piece_by_location_description('R').get_color() and \
                self.cube.get_piece_by_location((9,4)).get_color() == self.cube.get_center_piece_by_location_description('B').get_color() and \
                self.cube.get_piece_by_location((11,4)).get_color() == self.cube.get_center_piece_by_location_description('B').get_color():
                    break

            edgePiece = None
            midEdgePieces = self.cube.get_edge_pieces_in_middle_layer()
            for midEP in midEdgePieces:
                if (midEP[0].get_color() == self.cube.get_center_piece_by_edge_piece(midEP[0]).get_color()) and \
                        (midEP[1].get_color() == self.cube.get_center_piece_by_edge_piece(midEP[1]).get_color()):
                    continue
                elif midEP[0].get_color() != self.cube.get_piece_by_location((4,7)).get_color() and \
                        midEP[1].get_color() != self.cube.get_piece_by_location((4,7)).get_color():
                    edgePiece =(midEP[0],midEP[1])
                    break

            if debugML:
                print "\n"
                print "The edgePiece is ",
                print edgePiece

            # the edge piece is on the second layer, and the piece is in the right edge but in revised locations
            if edgePiece[0].get_pos()[1] == 4 and edgePiece[1].get_pos()[1]== 4 and \
                self.cube.get_center_piece_by_edge_piece(edgePiece[0]).get_color() == self.cube.get_piece_by_num(edgePiece[1].get_num()).get_color():

                if self._is_on_right(edgePiece[0],edgePiece[1]): #edgePiece1 is on the right hand of piece2
                    rF = self.cube.get_face_location_by_piece(self.cube.get_center_piece_of_face_one_piece_should_be(edgePiece[0]))
                else:
                    rF = self.cube.get_face_location_by_piece(self.cube.get_center_piece_of_face_one_piece_should_be(edgePiece[1]))
                rF_prime = rF + "'"
                self._manipulation(rF_prime,1)
                self._manipulation("D",1)
                self._manipulation(rF,1)
                self._manipulation("D'",1)
                self._manipulation("F",1)
                self._manipulation("D'",2)
                self._manipulation("F'",1)
                self._manipulation("D'",1)
                self._manipulation("F",1)
                self._manipulation("D'",2)
                self._manipulation("F'",1)

            # the edge piece is not in the right edge, has to be moved to bottom first
            if edgePiece[0].get_pos()[1]==4 and edgePiece[1].get_pos()[1]==4 and \
                self.cube.get_center_piece_by_edge_piece(edgePiece[0]).get_color() != self.cube.get_piece_by_num(edgePiece[0].get_num()).get_color() and \
                self.cube.get_center_piece_by_edge_piece(edgePiece[1]).get_color() != self.cube.get_peice_by_num(edgePiece[0].get_num()).get_color():
                leftPiece = self._get_edge_piece_member_on_left(edgePiece)
                rightPiece = None
                for piece in edgePiece:
                    if piece.get_num() != leftPiece.get_num():
                        rightPiece = piece
                        break
                left = self.cube.get_face_location_by_piece(leftPiece)
                left_prime = left+"'"
                f = self.cube.get_face_location_by_piece(rightPiece)
                f_prime = f+"'"
                self._manipulation("D",1)
                self._manipulation(left,1)
                self._manipulation("D'",1)
                self._manipulation(left_prime,1)
                self._manipulation("D'",1)
                self._manipulation(f_prime,1)
                self._manipulation("D",1)
                self._manipulation(f,1)


            # the edge piece is on the bottom layer
            if edgePiece[0].get_color() != self.cube.get_piece_by_location((4,7)).get_color() and \
                    edgePiece[1].get_color() != self.cube.get_piece_by_location((4,7)).get_color():
                # rotate the edge piece to the right face whose center piece is in the same
                # color with the edge piece
                bottomEdgePieceIndex = edgePiece[0].get_num()
                if debugML:
                    print "-"*64
                    print "Currently working on the mid layer edge piece: "
                    print "\t "
                    print edgePiece
                    print "-"*64
                    print "\n"

                loop = 0
                while(True):
                    loop +=1
                    if edgePiece[0].get_color() == \
                            self.cube.get_center_piece_by_edge_piece(self.cube.get_piece_by_num(bottomEdgePieceIndex)).get_color():
                        break
                    if loop >6:
                        print "\n"
                        print "!"*32
                        print "Program flies in _mid_layer function!!"
                        print "!" * 32
                        print "\n"
                        break
                    else:
                        self._manipulation('D',1)

                if debugML:
                    print "The mid layer edge piece has been moved to right place."
                    print self.cube
                    print "\n"
                #the edge piece is in the right place, then perform formula to this edge piece
                #add code here!
                currFCP = self.cube.get_center_piece_of_face_one_piece_should_be(edgePiece[0])
                neighborFCP = self.cube.get_center_piece_of_face_one_piece_should_be(edgePiece[1])
                cf = self.cube.get_face_location_by_piece(currFCP)
                cf_prime = cf+"'"
                nf = self.cube.get_face_location_by_piece(neighborFCP)
                nf_prime = nf+"'"
                if self._is_on_right( currFCP,neighborFCP): # neighborFCP is on the right hand of curFCP
                    self._manipulation("D'",1)
                    self._manipulation(nf_prime,1)
                    self._manipulation("D",1)
                    self._manipulation(nf,1)

                    self._manipulation("D",1)
                    self._manipulation(cf,1)
                    self._manipulation("D'",1)
                    self._manipulation(cf_prime,1)
                else:
                    self._manipulation("D", 1)
                    self._manipulation(nf,1)
                    self._manipulation("D'",1)
                    self._manipulation(nf_prime,1)

                    self._manipulation("D'",1)
                    self._manipulation(cf_prime,1)
                    self._manipulation("D",1)
                    self._manipulation(cf,1)

                if debugML:
                    print self.cube


#
# ---> form a cross on the last layer



#---> solve the last layer cross
    def _is_backwards_L(self):
        """An internal function used in _last_layer_cross function. It is to
        check if the current layout of pieces in the last layer.
        @returns a boolean value."""
        centerPieceInLastLayer = self.cube.get_piece_by_location((4,7))
        centerPieceColor = centerPieceInLastLayer.get_color()
        if self.cube.get_piece_by_location((4,6)).get_color() == centerPieceColor and \
            self.cube.get_piece_by_location((3,7)).get_color() == centerPieceColor and \
            self.cube.get_piece_by_location((5,7)).get_color() != centerPieceColor and \
            self.cube.get_piece_by_location((4,8)).get_color() != centerPieceColor:
            return True
        elif self.cube.get_piece_by_location((4,6)).get_color() == centerPieceColor and \
            self.cube.get_piece_by_location((5,7)).get_color() == centerPieceColor and \
            self.cube.get_piece_by_location((3,7)).get_color() != centerPieceColor and \
            self.cube.get_piece_by_location((4,8)).get_color() != centerPieceColor:
            return True
        elif self.cube.get_piece_by_location((5,7)).get_color() == centerPieceColor and \
            self.cube.get_piece_by_location((4,8)).get_color() == centerPieceColor and \
            self.cube.get_piece_by_location((3,7)).get_color() != centerPieceColor and \
            self.cube.get_piece_by_location((4,6)).get_color() != centerPieceColor:
            return True
        elif self.cube.get_piece_by_location((4,8)).get_color() == centerPieceColor and \
            self.cube.get_piece_by_location((3,7)).get_color() == centerPieceColor and \
            self.cube.get_piece_by_location((5,7)).get_color() != centerPieceColor and \
            self.cube.get_piece_by_location((4,6)).get_color() != centerPieceColor:
            return True
        else:
            return False

    def _is_line(self):
        #check if the layout is a line
        centerPieceInLastLayer = self.cube.get_piece_by_location((4, 7))
        centerPieceColor = centerPieceInLastLayer.get_color()
        if self.cube.get_piece_by_location((3,7)).get_color() == centerPieceColor and \
            self.cube.get_piece_by_location((5,7)).get_color() == centerPieceColor and \
            self.cube.get_piece_by_location((4,6)).get_color() != centerPieceColor and \
            self.cube.get_piece_by_location((4,8)).get_color() != centerPieceColor:
            return True
        elif self.cube.get_piece_by_location((4,8)).get_color() == centerPieceColor and \
            self.cube.get_piece_by_location((4,6)).get_color() == centerPieceColor and \
            self.cube.get_piece_by_location((3,7)).get_color() != centerPieceColor and \
            self.cube.get_piece_by_location((5,7)).get_color() != centerPieceColor:
            return True
        else:
            return False

    def _is_cross(self):
        #check if the layout is a cross
        centerPieceInLastLayer = self.cube.get_piece_by_location((4, 7))
        centerPieceColor = centerPieceInLastLayer.get_color()
        if self.cube.get_piece_by_location((3,7)).get_color() == centerPieceColor and \
            self.cube.get_piece_by_location((5,7)).get_color() == centerPieceColor and \
            self.cube.get_piece_by_location((4,6)).get_color() == centerPieceColor and \
            self.cube.get_piece_by_location((4,8)).get_color() == centerPieceColor:
            return True

    def _is_dot(self):
        #check if the layout is a dot
        if not self._is_backwards_L() and not self._is_line() and not self._is_cross():
            return True

    def _last_layer_cross(self):
        """Solve the last layer to be a cross."""
        debugCross = False
        print "\n"
        print "#" * 32
        print "---->  In _last_layer_cross function !!\n"

        centerPieceOnBottom = self.cube.get_piece_by_location((4,7))
        centerPieceOnBottomColor = centerPieceOnBottom.get_color()
        loopCnt = 0
        while(True):
            loopCnt +=1
            if loopCnt >10:
                print "\n"
                print "!"*32
                print "The program files in _last_layer_cross function!!!"
                print "!"*32
                print "\n"
                return
            if self._is_backwards_L():
                print "It's a backwards L."
                if self.cube.get_piece_by_location((4,6)).get_color() == centerPieceOnBottomColor and \
                    self.cube.get_piece_by_location((5,7)).get_color() == centerPieceOnBottomColor:
                    self._manipulation("L",1)
                    self._manipulation("D",1)
                    self._manipulation("B",1)
                    self._manipulation("D'",1)
                    self._manipulation("B'",1)
                    self._manipulation("L'",1)


                elif self.cube.get_piece_by_location((4,6)).get_color() == centerPieceOnBottomColor and \
                    self.cube.get_piece_by_location((3,7)).get_color() == centerPieceOnBottomColor:
                    self._manipulation("B",1)
                    self._manipulation("D",1)
                    self._manipulation("R",1)
                    self._manipulation("D'",1)
                    self._manipulation("R'",1)
                    self._manipulation("B'",1)

                elif self.cube.get_piece_by_location((3,7)).get_color() == centerPieceOnBottomColor and \
                    self.cube.get_piece_by_location((4,8)).get_color() == centerPieceOnBottomColor:
                    self._manipulation("R",1)
                    self._manipulation("D",1)
                    self._manipulation("F",1)
                    self._manipulation("D'",1)
                    self._manipulation("F'",1)
                    self._manipulation("R'",1)

                elif self.cube.get_piece_by_location((4,8)).get_color() == centerPieceOnBottomColor and \
                    self.cube.get_piece_by_location((5,7)).get_color() == centerPieceOnBottomColor:
                    self._manipulation("F",1)
                    self._manipulation("D",1)
                    self._manipulation("L",1)
                    self._manipulation("D'",1)
                    self._manipulation("L'",1)
                    self._manipulation("F'",1)
                if debugCross:
                    print self.cube
            elif self._is_cross():
                print "It's a cross."
                break
            elif self._is_line():
                print "It's a line."
                if self.cube.get_piece_by_location((3,7)).get_color() == centerPieceOnBottomColor and \
                    self.cube.get_piece_by_location((5,7)).get_color() == centerPieceOnBottomColor:
                    self._manipulation("B",1)
                    self._manipulation("R",1)
                    self._manipulation("D",1)
                    self._manipulation("R'",1)
                    self._manipulation("D'",1)
                    self._manipulation("B'",1)
                elif self.cube.get_piece_by_location((4,6)).get_color() == centerPieceOnBottomColor and \
                    self.cube.get_piece_by_location((4,8)).get_color() == centerPieceOnBottomColor:
                    self._manipulation("R",1)
                    self._manipulation("F",1)
                    self._manipulation("D",1)
                    self._manipulation("F'",1)
                    self._manipulation("D'",1)
                    self._manipulation("R'",1)

                if debugCross:
                    print self.cube
            elif self._is_dot():
                print "It's a dot."
                #use one of the algorithms for the backwards L shape
                self._manipulation("L", 1)
                self._manipulation("D", 1)
                self._manipulation("B", 1)
                self._manipulation("D'", 1)
                self._manipulation("B'", 1)
                self._manipulation("L'", 1)

#---> solve the last layer edge

 #---> the last layer edges
    def _get_edge_piece_on_right(self, twoEdgePieces):
        """An internal funtion used in _last_layer_edges function. Get the
        right one of two adjacent edge pieces on the last layer."""
        p1, p2 = twoEdgePieces[0],twoEdgePieces[1]
        p1Loc = p1.get_pos()
        p2Loc = p2.get_pos()
        if p1Loc == (4,5) and p2Loc ==(7,5) or\
           p2Loc == (4,5) and p1Loc ==(7,5):
            return self.cube.get_piece_by_location((4,5))
        elif p1Loc ==(4,5) and p2Loc ==(1,5) or\
             p2Loc ==(4,5) and p1Loc ==(1,5):
            return self.cube.get_piece_by_location((1,5))
        elif p1Loc ==(10,5) and p2Loc ==(1,5) or\
            p2Loc ==(10,5) and p1Loc == (1,5):
            return self.cube.get_piece_by_location((10,5))
        elif p1Loc ==(7,5) and p2Loc ==(10,5) or\
            p2Loc ==(7,5) and p1Loc ==(10,5):
            return self.cube.get_piece_by_location((7,5))

    def _get_edge_piece_members_around_last_layer(self):
        # returns the four pieces around the last layer
        p1 = self.cube.get_piece_by_location((1, 5))
        p2 = self.cube.get_piece_by_location((4, 5))
        p3 = self.cube.get_piece_by_location((7, 5))
        p4 = self.cube.get_piece_by_location((10, 5))
        return [p1,p2,p3,p4]

    def _is_at_least_two_edge_pieces_line_up(self):
        # check at least two edge pieces on the last layer lines up with the centre piece with same color
        pieces = self._get_edge_piece_members_around_last_layer()
        cnt = 0
        for pc in pieces:
            if pc.get_color() == self.cube.get_center_piece_by_edge_piece(pc).get_color():
                cnt +=1
                if cnt >= 2:
                    return True
        return False

    def _is_edge_pieces_at_right_location(self):
        #check if four edge pieces are at the right places on the last layer
        p1,p2,p3,p4 = self._get_edge_piece_members_around_last_layer()
        if p1.get_color() == self.cube.get_center_piece_by_edge_piece(p1).get_color() and \
            p2.get_color() == self.cube.get_center_piece_by_edge_piece(p2).get_color() and \
            p3.get_color() == self.cube.get_center_piece_by_edge_piece(p3).get_color() and \
            p4.get_color() == self.cube.get_center_piece_by_edge_piece(p4).get_color():
            return True
        else:
            return False

    def _get_edge_pieces_at_opposite_locations(self):
        # if the two edge pieces which are not in the right place
        # are in the opposite, it returns the two edge pieces
        p1,p2,p1Opp,p2Opp = self._get_edge_piece_members_around_last_layer()
        if p1.get_color() == self.cube.get_center_piece_by_edge_piece(p1Opp).get_color():
            return [p1,p1Opp]
        elif p2.get_color() == self.cube.get_center_piece_by_edge_piece(p2Opp).get_color():
            return [p2,p2Opp]
        else:
            return None

    def _get_adjacent_edge_pieces(self):
        # returns two adjacent edge pieces
        p1,p2,p3,p4 = self._get_edge_piece_members_around_last_layer()
        combs = [[p1,p2],[p2,p3],[p3,p4],[p4,p1]]
        for c in combs:
            if c[0].get_color() == self.cube.get_center_piece_by_edge_piece(c[1]).get_color() and \
                c[1].get_color() == self.cube.get_center_piece_by_edge_piece(c[0]).get_color():
                return c
        return None

    def _last_layer_edges(self):

        """Solve the edges on the last layer"""
        print "\n"
        print "#" * 32
        print "---->  In _last_layer_edges function !!\n"
        debugLastEgs = True

        # at least one edge piece lines up with the centre piece of the same color
        lpCnt = 0
        while(True):
            lpCnt +=1
            if lpCnt >5:
                print "!"*32
                print "Program flies in _last_layer_edges!!"
                print "!"*32
                print "\n"
            if self._is_at_least_two_edge_pieces_line_up():
                if debugLastEgs:
                    print "At least two edge pieces line up!!"
                break
            else:
                self._manipulation("D",1)

        lpCnt2 = 0
        while(True):
            lpCnt2 +=1
            if lpCnt2 >5:
                print "!" * 32
                print "Program flies (in _last_layer_edges) function loop count 2!!"
                print "!" * 32
                print "\n"

            if not self._is_edge_pieces_at_right_location():
                oppsiteEps = self._get_edge_pieces_at_opposite_locations()
                adjEps = self._get_adjacent_edge_pieces()

                if debugLastEgs:
                    print adjEps

                if adjEps != None:
                    rightPiece = self._get_edge_piece_on_right(adjEps)

                    if debugLastEgs:
                        print "\n"
                        print "the right piece is "
                        print rightPiece
                        print "\n"
                    r = self.cube.get_face_location_by_piece(rightPiece)
                    r_prime = r+"'"
                    self._manipulation("D",1)
                    self._manipulation(r,1)
                    self._manipulation("D",1)
                    self._manipulation(r_prime,1)
                    self._manipulation("D",1)
                    self._manipulation(r,1)
                    self._manipulation("D",2)
                    self._manipulation(r_prime,1)

                elif oppsiteEps != None:
                    self._manipulation("D", 1)
                    self._manipulation("R", 1)
                    self._manipulation("D", 1)
                    self._manipulation("R'", 1)
                    self._manipulation("D", 1)
                    self._manipulation("R", 1)
                    self._manipulation("D", 2)
                    self._manipulation("R'", 1)

            else:
                print "All four edge pieces are at the right location! Whoops!"
                break




#---> the last layer corners


#---> the last layer corners

#----> last layer corners
    def _get_last_layer_corner_pieces(self):
        #returns the four corner pieces on the last layer
        cpm1 = self.cube.get_piece_by_location((3, 8))
        cpm2 = self.cube.get_piece_by_location((5, 8))
        cpm3 = self.cube.get_piece_by_location((3, 6))
        cpm4 = self.cube.get_piece_by_location((5, 6))
        cp1 = self.cube.get_corner_piece_by_one_piece_member(cpm1)
        cp2 = self.cube.get_corner_piece_by_one_piece_member(cpm2)
        cp3 = self.cube.get_corner_piece_by_one_piece_member(cpm3)
        cp4 = self.cube.get_corner_piece_by_one_piece_member(cpm4)
        cps = [cp4, cp3, cp1, cp2]
        return cps

    def _is_four_corner_pieces_at_right_corner_and_orientation(self):
        # check if the four corner pieces on the last layer are
        # correctly positioned and in right orientation
        cps = self._get_last_layer_corner_pieces()
        cnt = 0
        for cp in cps:
            currColors = [p.get_color() for p in cp]
            cpsFaceColors = [self.cube.get_center_piece_by_corner_piece(p).get_color() for p in cp]
            if currColors == cpsFaceColors:
                cnt+=1
        if cnt == 4:
            return True
        else:
            return False


    def _get_corner_pieces_at_right_corner_incorrect_orientation(self):
        #returns the corner pieces that are at the correct corners, however,
        #this corner piece is in the right orientation
        cps = self._get_last_layer_corner_pieces()
        cpsAtRightCorner = []
        for cp in cps:
         #   print "Corner Piece: ",
         #   print cp
         #   print "\n"
            currColors = [p.get_color() for p in cp]
            cpsFaceColors = [self.cube.get_center_piece_by_corner_piece(p).get_color() for p in cp]
            currColors.sort()
            cpsFaceColors.sort()
            if currColors == cpsFaceColors and not self._is_four_corner_pieces_at_right_corner_and_orientation():
                cpsAtRightCorner.append(cp)
                continue

        if len(cpsAtRightCorner) >= 1:
            return cpsAtRightCorner
        else:
            return None

    def _perform_last_corner_piece_algorithm(self, locs):
        #perform the algorithm to get the corner piece which is at right place
        #to the correct orientation
        print "Perform last corner piece alg"
        if (3, 6) in locs:
            self._manipulation("D", 1)
            self._manipulation("L", 1)
            self._manipulation("D'", 1)
            self._manipulation("R'", 1)
            self._manipulation("D", 1)
            self._manipulation("L'", 1)
            self._manipulation("D'", 1)
            self._manipulation("R", 1)
        elif (5,6) in locs:
            self._manipulation("D", 1)
            self._manipulation("F", 1)
            self._manipulation("D'", 1)
            self._manipulation("B'", 1)
            self._manipulation("D", 1)
            self._manipulation("F'", 1)
            self._manipulation("D'", 1)
            self._manipulation("B", 1)
        elif (3,8) in locs:
            self._manipulation("D", 1)
            self._manipulation("B", 1)
            self._manipulation("D'", 1)
            self._manipulation("F'", 1)
            self._manipulation("D", 1)
            self._manipulation("B'", 1)
            self._manipulation("D'", 1)
            self._manipulation("F", 1)
        elif (5,8) in locs:
            self._manipulation("D", 1)
            self._manipulation("R", 1)
            self._manipulation("D'", 1)
            self._manipulation("L'", 1)
            self._manipulation("D", 1)
            self._manipulation("R'", 1)
            self._manipulation("D'", 1)
            self._manipulation("L", 1)

    def _last_layer_corners(self):
        #solve the last layer corners
        print "\n"
        print "#" * 32
        print "---->  In _last_layer_corners function !!\n"
        debugLastLayerCorners = True


        if self._is_four_corner_pieces_at_right_corner_and_orientation():
            print "Cube solved!!!"
            return

        lpCnt = 0
        while(True):
            lpCnt +=1
            cpsAtRightCorner = self._get_corner_pieces_at_right_corner_incorrect_orientation()
            if lpCnt >5:
                print "\n"
                print "!"*32
                print "Program flies in _last_layer_corners function!!"
                print "!"*32
                return

            if len(cpsAtRightCorner) == 4:
                print "\n"
                print "Four corner pieces on the last layer are in their right places!!"
                break
            # there is one or four corner pieces at the right place
            if cpsAtRightCorner != None:
                #perform this algorithm to move other corner cubies to their correct places.
                for cps in cpsAtRightCorner:
                    if debugLastLayerCorners:
                        print "\n"
                        print "perform on corner piece: ",
                        print cps

                    locs = [cp.get_pos() for cp in cps]
                    self._perform_last_corner_piece_algorithm(locs)


        return


#---> solve the cube
    def _perform_last_layer_corners2_algorithm(self, locs):

        if (5,6) in locs:
            self._manipulation("F'",1)
            self._manipulation("U'",1)
            self._manipulation("F",1)
            self._manipulation("U",1)

            self._manipulation("F'", 1)
            self._manipulation("U'", 1)
            self._manipulation("F", 1)
            self._manipulation("U", 1)
            return


    def _is_corner_piece_at_right_corner_and_orientation(self, cp):
        #check if the corner piece `cp` is in the right place and in the correct orientation
        bottomCenterPieceColor = self.cube.get_piece_by_location((4,7)).get_color()
        cpMemShouldBeOnBottom = [p for p in cp if p.get_color()== bottomCenterPieceColor][0]

        centerPieceOfCpMemShouldBeOnBottom = self.cube.get_center_piece_by_corner_piece(cpMemShouldBeOnBottom)

        if centerPieceOfCpMemShouldBeOnBottom.get_color() == bottomCenterPieceColor:
            return True
        else:
            return False

    def _move_corner_piece_to_FRD(self, cp):
        #move the corner piece `cp` to the location `FRD`
        cpLocs = [p.get_pos() for p in cp]
        if (5,6) in cpLocs:
            return
        if (3,6) in cpLocs:
            self._manipulation("D",1)
            return
        if (3,8) in cpLocs:
            pass

    def _last_layer_corners2(self):
        #the last step

        debugLLC2= False
        print "\n"
        print "#" * 32
        print "---->  In _last_layer_corners2 function !!\n"

        cps = self._get_last_layer_corner_pieces()

        #get the corner pieces to the right orientations
        #note: need to move the next incorrect corner piece into the same location
        for cp in cps:
            lpCnt = 0
            if debugLLC2:
                print "current corner piece is ",
                print cp
                print "\n"


            onePieceMemIndex = cp[0].get_num()
            while(True):
                lpCnt +=1
                if lpCnt >4:
                    print "!"*32
                    print "Program flies in _last_layer_corner2 function!"
                    print "!"*32
                    print "\n"
                    return

                cp = self.cube.get_corner_piece_by_one_piece_member(self.cube.get_piece_by_num(onePieceMemIndex))
                if self._is_corner_piece_at_right_corner_and_orientation(cp):
                    print "This corner piece is at home!!!"
                    self._manipulation("D",1)
                    print self.cube
                    break

                cpLocs = [p.get_pos() for p in cp]
                self._perform_last_layer_corners2_algorithm(cpLocs)
                print self.cube

    def _get_solution(self):
        # simplified the solution
        simplified = lambda orgSolution,b: [(i, i + len(b)) for i in range(len(orgSolution)) if orgSolution[i:i + len(b)] == b]
        duplicated = [("D'",["D","D","D"]),("D",["D'","D'","D'"]),("U'",["U","U","U"]),("U",["U'","U'","U'"]),
                      ("F'",["F","F","F"]),("F",["F'","F'","F'"]),("B'",["B","B","B"]),("B",["B'","B'","B'"]),
                      ("L'",["L","L","L"]),("L",["L'","L'","L'"]),("R'",["R","R","R"]),("R",["R'","R'","R'"])]
        dic = {}
        for simpB, b in duplicated:
           # print "simpB is ",
           # print simpB
           # print "duplicated is ",
           # print b
            dic[simpB] = simplified(self.solution,b)

        solutionLen = len(self.solution)
      #  print dic
        for key in dic.keys():
            items = dic[key]

            if len(items) !=0:
                for item in items:
               #     print "Replaced [%s,%s] with " %(str(item[0]),str(item[1])),
               #     print key
                    self.solution[item[0]:item[1]]="X"
                    self.solution[item[0]] = key
                    for indx in range(solutionLen)[(item[0]+1):item[1]]:
                        self.solution.insert(indx, "")
        emptyCnt = self.solution.count("")
        for c in range(emptyCnt):
            self.solution.remove("")
        return self.solution

    def _solve(self):
        self._top_cross()
        self._top_layer()
        print self.cube
        self._mid_layer()
        self._last_layer_cross()
        print self.cube
        self._last_layer_edges()
        print self.cube
        self._last_layer_corners()
        print self.cube
        self._last_layer_corners2()


def manipulation(cube, f, n):
    """An internal function used to perform rotations around face `f`.
    @param f: is the face to be manipulated on. e.g. "F" or "U'"
    @param n: is the times of the rotation.
    """
    operation = {"L": cube.L, "L'": cube.L_prime,
                 "R": cube.R, "R'": cube.R_prime,
                 "F": cube.F, "F'": cube.F_prime,
                 "B": cube.B, "B'": cube.B_prime,
                 "U": cube.U, "U'": cube.U_prime,
                 "D": cube.D, "D'": cube.D_prime}
    for t in range(n):
        operation[f.upper()]()

def test_algorithm(cube, solution):
    for s in solution:
        manipulation(cube, s,1)

def test():
    t = False
    usercube = {
            'l':['o','b','r','w','o','r','y','r','w'],
            'f':['g','y','y','g','g','y','b','r','b'],
            'r':['b','o','b','b','r','r','w','o','g'],
            'b':['y','w','w','w','b','b','w','g','g'],
            'u':['g','o','o','o','w','g','y','g','r'],
            'd':['r','b','o','y','y','y','o','w','r']
        }
    refcube = Cube(3)
    
    usr = Cube(3,usercube)

    alg = Algorithm(usr)
    alg._solve()
    solution = alg._get_solution()

    # test on the solution
    print "\n\n"
    print "-"*50
    print "Test on the solution"
    usrcube = Cube(3,usercube)
    print usrcube
    test_algorithm(usrcube, solution)
    print usrcube
    return

   
    
    

if __name__ == '__main__':
    test()

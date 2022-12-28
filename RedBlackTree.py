# Global variable
RED, BLACK = 1, 0

class Node():
    def __init__(self, data=0, color=RED, parent=None, left=None, right=None):
        self.data = data
        self.color = color
        self.parent = parent
        self.left = left
        self.right = right

NIL = Node(color=BLACK)

class RedBlackTree():
    def __init__(self):
        self.root = NIL
# --------------------------------------------------
# ------------     PRINTING METHODS     ------------
# --------------------------------------------------
    def printPreRec(self, node):
        if node != NIL:
            print(node.data, "", end='')
            self.printPreRec(node.left)
            self.printPreRec(node.right)

    def printPre(self):
        self.printPreRec(self.root)

    def printInRec(self, node):
        if node != NIL:
            self.printInRec(node.left)
            print(node.data, "", end='')
            self.printInRec(node.right)

    def printIn(self):
        self.printInRec(self.root)

    def printPostRec(self, node):
        if node != NIL:
            self.printPostRec(node.left)
            self.printPostRec(node.right)
            print(node.data, "", end='')

    def printPost(self):
        self.printPostRec(self.root)

    def printHelper(self, node, indent, last):
        if node != NIL:
            print(indent, end='')
            if last:
                print("R----", end='')
                indent += "     "
            else:
                print("L----", end='')
                indent += "|    "
            s_color = "RED" if node.color == RED else "BLACK"
            print(str(node.data) + "(" + s_color + ")")
            self.printHelper(node.left, indent, False)
            self.printHelper(node.right, indent, True)

    def printTree(self):
        self.printHelper(self.root, "", True)
# --------------------------------------------------
# -----------------     SEARCH     -----------------
# --------------------------------------------------
    def search(self, data):
        N = self.root
        while N != NIL and N.data != data:
            if data < N.data:   N = N.left
            else:   N = N.right
        return N
# --------------------------------------------------
# ----------------     ROTATION     ----------------
# --------------------------------------------------
    def rotateLeft(self, N):
        C = N.right
        N.right = C.left
        if C.left != NIL:
            C.left.parent = N
        C.parent = N.parent
        if not N.parent:
            self.root = C
        elif N == N.parent.left:
            N.parent.left = C
        else:
            N.parent.right = C
        C.left = N
        N.parent = C

    def rotateRight(self, N):
        C = N.left
        N.left = C.right
        if C.right != NIL:
            C.right.parent = N
        C.parent = N.parent
        if not N.parent:
            self.root = C
        elif N == N.parent.right:
            N.parent.right = C
        else:
            N.parent.left = C
        C.right = N
        N.parent = C
# --------------------------------------------------
# ---------------     INSERTION     ----------------
# --------------------------------------------------
    def insertFix(self, N):
        while N.parent.color == RED:
            if N.parent == N.parent.parent.left:
                U = N.parent.parent.right
                if U.color == RED:
                    U.color = BLACK
                    N.parent.color = BLACK
                    N.parent.parent.color = RED
                    N = N.parent.parent
                else:
                    if N == N.parent.right:
                        N = N.parent
                        self.rotateLeft(N)
                    N.parent.color = BLACK
                    N.parent.parent.color = RED
                    self.rotateRight(N.parent.parent)
            else:
                U = N.parent.parent.left
                if U.color == RED:
                    U.color = BLACK
                    N.parent.color = BLACK
                    N.parent.parent.color = RED
                    N = N.parent.parent
                else:
                    if N == N.parent.left:
                        N = N.parent
                        self.rotateRight(N)
                    N.parent.color = BLACK
                    N.parent.parent.color = RED
                    self.rotateLeft(N.parent.parent)

            if N == self.root:
                break
        self.root.color = BLACK

    def insert(self, data):
        node = Node(data)
        node.left = NIL
        node.right = NIL
        P = None
        N = self.root
        while N != NIL:
            P = N
            if data < N.data:	N = N.left
            else:	N = N.right
        node.parent = P
        if not P:
            self.root = node
            node.color = BLACK
            return
        elif data < P.data: P.left = node
        else:   P.right = node
        if not P.parent:    return
        self.insertFix(node)
# --------------------------------------------------
# ----------------     DELETION     ----------------
# --------------------------------------------------
    def minNode(self, N):
        while N.left != NIL:
            N = N.left
        return N

    def replaceDelete(self, N, C):
        if N.parent == None:
            self.root = C
        elif N == N.parent.left:
            N.parent.left = C
        else:
            N.parent.right = C
        C.parent = N.parent

    def deleteFix(self, N):
        while N != self.root and N.color == BLACK:
            P = N.parent
            if N == P.left:
                S = P.right
                if S.color == RED:
                    S.color = BLACK
                    P.color = RED
                    self.rotateLeft(P)
                    S = P.right
                if S.left.color == BLACK and S.right.color == BLACK:
                    S.color = RED
                    N = P
                else:
                    if S.right.color == BLACK:
                        S.left.color = BLACK
                        S.color = RED
                        self.rotateRight(S)
                        S = P.right
                    S.color = P.color
                    P.color = BLACK
                    S.right.color = BLACK
                    self.rotateLeft(P)
                    N = self.root
            else:
                S = P.left
                if S.color == RED:
                    S.color = BLACK
                    P.color = RED
                    self.rotateRight(P)
                    S = P.left
                if S.left.color == BLACK and S.right.color == BLACK:
                    S.color = RED
                    N = P
                else:
                    if S.left.color == BLACK:
                        S.right.color = BLACK
                        S.color = RED
                        self.rotateLeft(S)
                        S = P.left
                    S.color = P.color
                    P.color = BLACK
                    S.left.color = BLACK
                    self.rotateRight(P)
                    N = self.root
        N.color = BLACK

    def deleteHelper(self, N, data):
        while N != NIL:
            if N.data == data:  break
            elif N.data < data: N = N.right
            else:   N = N.left
        if N == NIL:
            print("Cannot find data in the tree")
            return
        y = N
        originColor = y.color
        if N.left == NIL:
            x = N.right
            self.replaceDelete(N, N.right)
        elif N.right == NIL:
            x = N.left
            self.replaceDelete(N, N.left)
        else:
            y = self.minNode(N.right)
            originColor = y.color
            x = y.right
            if y.parent == N:
                x.parent = y
            else:
                self.replaceDelete(y, y.right)
                y.right = N.right
                y.right.parent = y
            self.replaceDelete(N, y)
            y.left = N.left
            y.left.parent = y
            y.color = N.color
        if originColor == BLACK:
            self.deleteFix(x)

    def delete(self, data):
        self.deleteHelper(self.root, data)

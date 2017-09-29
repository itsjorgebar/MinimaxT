import copy
import time

class Board(object):
    def _init_(self, width, height):
        self.width = width
        self.height = height
        self.lastHeight = -1
        self.values = [[0 for y in range(self.width)] for x in range(self.height)]

    def place(self, col, player_number):
        newBoard = copy.deepcopy(self)
        partial_height = newBoard.height - 1
        while (partial_height >= 0 and newBoard.values[partial_height][col] == 0):
            partial_height -= 1
        if (partial_height + 1 < newBoard.height):
            newBoard.values[partial_height+1][col] = player_number
            newBoard.lastHeight = partial_height + 1
        return newBoard

    def realPlace(self, column, player_number):
        if (column >= self.width or column < 0):
            return False
        partial_height = self.height - 1
        while (partial_height >= 0 and self.values[partial_height][column] == 0):
            partial_height -= 1
        if (partial_height + 1 < self.height):
            self.values[partial_height + 1][column] = player_number
            self.lastHeight = partial_height + 1
            return True
        return False

    def canPlace(self, col):
        if (col >= self.width or col < 0):
            return False
        partial_height = self.height - 1
        while (partial_height >= 0 and self.values[partial_height][col] == 0):
            partial_height -= 1
        if (partial_height + 1 < self.height):
            return True
        return False

    def count(self):
        counter = 0
        for row in range(0,self.height):
            for col in range(0,self.width):
                if self.values[row][col] != 0:
                    counter +=1
        return counter


    def gameFinished(self, player_number):
        available_moves = False
        for pos in range(self.width):
            if (self.values[self.height - 1][pos] == 0):
                available_moves = True
                break

        if (self.checkAnyT(player_number)):
            return 1

        if (not available_moves):
            return -1

        return 0

    # Function for printing the game board
    def printGame(self):
        for row in range(self.height - 1, -1, -1):
            for col in range(0, self.width):
                if(self.values[row][col] == -1 or self.values[row][col] == 2):
                    print('x', end=" ")
                elif(self.values[row][col] == 1):
                    print('1', end=" ")
                else: print('0', end=" ")
            print("\n")
        print("\n")

    def checkAnyT(self, player_number):
        for r in range(0, self.height):
            for c in range(0, self.width):
                if (self.values[r][c] == player_number):
                    if (self.checkWinBelow(r, c, player_number)
                        or self.checkWinAbove(r, c, player_number)
                        or self.checkLeft(r, c, player_number)
                        or self.checkRight(r, c, player_number)
                        or self.checkWinBottomRight(r, c, player_number)
                        or self.checkWinBottomLeft(r, c, player_number)
                        or self.checkWinTopLeft(r, c, player_number)
                        or self.checkWinTopRight(r, c, player_number)):
                        return True
        return False

    def checkWinBelow(self, row, col, player_number):
        if (col + 1 == self.width or col == 0 or row + 1 == self.height): return False
        if (self.values[row + 1][col - 1] == self.values[row + 1][col] == self.values[row + 1][
                col + 1] == player_number): return True
        return False

    def checkWinAbove(self, row, col, player_number):
        if (col == 0 or row == 0 or col + 1 == self.width): return False
        if (self.values[row - 1][col - 1] == self.values[row - 1][col] == self.values[row - 1][
                col + 1] == player_number): return True
        return False

    def checkLeft(self, row, col, player_number):
        if (row + 1 >= self.height or col + 1 >= self.width or row - 1 < 0): return False
        if (self.values[row - 1][col + 1] == self.values[row][col + 1] == self.values[row + 1][col + 1] == player_number): return True
        return False

    def checkRight(self, row, col, player_number):
        if (col == 0 or row == 0 or row + 1 == self.height): return False
        if (self.values[row - 1][col - 1] == self.values[row][col - 1] == self.values[row + 1][col - 1] == player_number): return True
        return False

    def checkWinBottomRight(self, row, col, player_number):
        if (row + 2 >= self.height or col - 2 < 0): return False
        if (self.values[row][col - 2] == player_number and self.values[row + 1][col - 1] == player_number and self.values[row + 2][
            col] == player_number): return True
        return False

    def checkWinBottomLeft(self, row, col, player_number):
        if (row + 2 >= self.height or col + 2 >= self.width): return False
        if (self.values[row + 2][col] == player_number and self.values[row + 1][col + 1] == player_number and self.values[row][
                col + 2] == player_number): return True
        return False

    def checkWinTopLeft(self, row, col, player_number):
        if (row - 2 < 0 or col + 2 >= self.width): return False
        if (self.values[row - 2][col] == player_number and self.values[row - 1][col + 1] == player_number and self.values[row][
                col + 2] == player_number): return True
        return False

    def checkWinTopRight(self, row, col, player_number):
        if (row - 2 < 0 or col - 2 < 0): return False
        if (self.values[row - 2][col] == player_number and self.values[row - 1][col - 1] == player_number and self.values[row][
                col - 2] == player_number): return True
        return False


max_int = 10000


class Node(object):
    def _init_(self, depth, playerNum, board, value, index):
        global max_int
        self.playColumn = 0
        self.depth = depth
        self.playerNum = playerNum
        self.board = board
        self.value = value
        self.average = 0
        if (abs(value) < max_int): self.value = self.determineValue() * (playerNum)
        self.children = []
        self.index = index


    def generateChildren(self):
        global max_int
        for curr in range(0, self.board.width):
            if (self.board.canPlace(curr)):
                self.children.append(Node(self.depth - 1, -self.playerNum, self.board.place(curr, -self.playerNum), 0, curr))
            else: self.children.append(Node(0, -self.playerNum, self.board.place(curr, -self.playerNum), max_int*self.depth*(self.playerNum), curr))

    def determineValue(self):
        global max_int
        #if (self.board.lastHeight >= self.board.height):
         #   return (self.depth + 1) * (-max_int)
        if (self.board.checkAnyT(self.playerNum)):
            return (self.depth+1) * max_int
        else: return 0

    def getRewards(self):
        return self.checkTwoStraight() + self.checkTwoDiagonal() + self.checkThreeStraight() + self.checkThreeDiagonals()

    def checkTwoRight(self):
        if (self.index > 0 and self.board.values[self.board.lastHeight][self.index - 1] == self.playerNum):
            # self.board.printGame()
            return 50
        else:
            return 0

    def checkTwoLeft(self):
        if (self.index < (self.board.width - 1) and self.board.values[self.board.lastHeight][
                self.index + 1] == self.playerNum):
            # self.board.printGame()
            return 50
        else:
            return 0

    def checkTwoTop(self):
        if (self.board.lastHeight > 0 and self.board.values[self.board.lastHeight - 1][self.index] == self.playerNum):
            # print(self.board.values[0][0], self.board.values[0][1], self.board.lastHeight)
            # self.board.printGame()
            return 50
        else:
            return 0

    def checkTwoDiagonalRightBottom(self):
        if (self.board.lastHeight < self.board.height - 1 and self.index > 0 and
                self.board.values[self.board.lastHeight + 1][self.index - 1] == self.playerNum):
            return 50
        else:
            return 0

    def checkTwoDiagonalLeftTop(self):
        if (self.board.lastHeight > 0 and self.index < self.board.width - 1 and
                self.board.values[self.board.lastHeight - 1][self.index + 1] == self.playerNum):
            return 50
        else:
            return 0

    def checkTwoDiagonalLeftBottom(self):
        if (self.board.lastHeight < self.board.height - 1 and self.index < self.board.width - 1 and
                self.board.values[self.board.lastHeight + 1][self.index + 1] == self.playerNum):
            return 50
        else:
            return 0

    def checkTwoDiagonalRightTop(self):
        if (self.board.lastHeight > 0 and self.index > 0 and self.board.values[self.board.lastHeight - 1][
                self.index - 1] == self.playerNum):
            return 50
        else:
            return 0

    def checkThreeHorizontalRight(self):
        if(self.index - 2 >= 0 and self.board.values[self.board.lastHeight][self.index-1] == self.board.values[self.board.lastHeight][self.index-2] == self.playerNum):
            return 150
        else: return 0

    def checkThreeHorizontalMiddle(self):
        if(self.index - 1 >= 0 and self.index + 1 < self.board.width and self.board.values[self.board.lastHeight][self.index-1] == self.board.values[self.board.lastHeight][self.index+1] == self.playerNum):
            return 150
        else: return 0

    def checkThreeHorizontalLeft(self):
        if(self.index + 2 < self.board.width and self.board.values[self.board.lastHeight][self.index+1] == self.board.values[self.board.lastHeight][self.index+2] == self.playerNum):
            return 150
        else: return 0

    def checkThreeVertical(self):
        if(self.board.lastHeight - 2 >= 0 and self.board.values[self.board.lastHeight-1][self.index] == self.board.values[self.board.lastHeight-2][self.index] == self.playerNum):
            return 150
        else: return 0

    def checkThreeDiagonalRightBottom(self):
        if(self.board.lastHeight + 2 < self.board.height and self.index - 2 >= 0 and self.board.values[self.board.lastHeight+1][self.index-1] == self.board.values[self.board.lastHeight+2][self.index-2] == self.playerNum):
            return 150
        else: return 0

    def checkThreeDiagonalRightMiddle(self):
        if(self.board.lastHeight + 1 < self.board.height and self.index - 1 >= 0 and self.board.lastHeight - 1 >= 0 and self.index + 1 < self.board.width
           and self.board.values[self.board.lastHeight+1][self.index-1] == self.board.values[self.board.lastHeight-1][self.index+1] == self.playerNum):
            return 150
        else: return 0

    def checkThreeDiagonalRightTop(self):
        if(self.board.lastHeight - 2 >= 0 and self.index + 2 < self.board.width and
                       self.board.values[self.board.lastHeight-1][self.index+1] == self.board.values[self.board.lastHeight-2][self.index+2] == self.playerNum):
            return 150
        else: return 0

    def checkThreeDiagonalLeftBottom(self):
        if(self.board.lastHeight + 2 < self.board.height and self.index + 2 < self.board.width and self.board.values[self.board.lastHeight+1][self.index+1] == self.board.values[self.board.lastHeight+2][self.index+2] == self.playerNum):
            return 150
        else: return 0

    def checkThreeDiagonalLeftMiddle(self):
        if (self.board.lastHeight + 1 < self.board.height and self.index - 1 >= 0 and self.board.lastHeight - 1 >= 0 and self.index + 1 < self.board.width and self.board.values[self.board.lastHeight + 1][self.index + 1] == self.board.values[self.board.lastHeight - 1][self.index - 1] == self.playerNum):
            return 150
        else:
            return 0

    def checkThreeDiagonalLeftTop(self):
        if(self.board.lastHeight - 2 >= 0 and self.index - 2 >= 0 and self.board.values[self.board.lastHeight-1][self.index-1] == self.board.values[self.board.lastHeight-2][self.index-2] == self.playerNum):
            return 150
        else: return 0

    def checkThreeDiagonals(self):
        return self.checkThreeDiagonalLeftBottom() + self.checkThreeDiagonalLeftMiddle() + self.checkThreeDiagonalLeftTop() + self.checkThreeDiagonalRightBottom() + self.checkThreeDiagonalRightMiddle()+ self.checkThreeDiagonalRightTop()

    def checkThreeStraight(self):
        return self.checkThreeVertical() + self.checkThreeHorizontalLeft()+ self.checkThreeHorizontalMiddle()+ self.checkThreeHorizontalRight()

    def checkTwoStraight(self):
        sumTot = 0
        top = self.checkTwoTop()
        left = self.checkTwoLeft()
        right = self.checkTwoRight()
        rightUp = self.checkTwoDiagonalRightTop()
        leftUp = self.checkTwoDiagonalLeftTop()
        leftDown = self.checkTwoDiagonalLeftBottom()
        rightDown = self.checkTwoDiagonalRightBottom()
        if(top == 50):
            if(left == 50): sumTot += 150
            if(right == 50): sumTot += 150

        if(right == 50):
            if(rightUp == 50): sumTot += 150
            if(rightDown == 50): sumTot +=350

        if(left == 50):
            if(leftUp == 50): sumTot += 150
            if(leftDown == 50): sumTot += 350

        return top + left + right + sumTot

    def checkTwoDiagonal(self):
        return self.checkTwoDiagonalLeftBottom() + self.checkTwoDiagonalLeftTop() + self.checkTwoDiagonalRightBottom() + self.checkTwoDiagonalRightTop()


def AlphaBetaMinMax(node, playerNum, alpha, beta, startTime):
    global max_int, maxDepth
    if(abs(node.value) >= max_int):
        return node.value
    if (node.depth <= 0):
        node.value = node.getRewards() * node.playerNum
        return node.value

    sum = 0
    bestValue = (max_int*maxDepth) * -playerNum # possitive p
    bestAverage = 0

    for child in range(0 , node.board.width):
        if(time.time() - startTime > 4):
            node.playColumn = -1
            return 0
        if (node.board.canPlace(child)): node.children.append(Node(node.depth - 1, -node.playerNum, node.board.place(child, -node.playerNum), 0, child))
        else: node.children.append(Node(0, -node.playerNum, node.board.place(child, -node.playerNum), max_int * node.depth * (node.playerNum), child))
        val = AlphaBetaMinMax(node.children[child], -playerNum, alpha, beta, startTime)
        sum += val
        if (abs(max_int * maxDepth * playerNum - val) < abs(max_int * maxDepth * playerNum - bestValue) or (abs(max_int * maxDepth * playerNum - val) == abs(max_int * maxDepth * playerNum - bestValue) and abs(max_int * maxDepth * playerNum - node.children[child].average) < abs( max_int * maxDepth * playerNum - bestAverage))):
            bestValue = val
            bestAverage = node.children[child].average
            node.playColumn = node.children[child].index
        if (node.playerNum == -1):
            alpha = max(alpha,bestValue)
        else:
            beta = min(beta,bestValue)
        if(beta < alpha): break
    if (time.time() - startTime > 4):
        node.playColumn = -1
        return 0
    node.average = sum/node.board.width
    node.value = bestValue
    return bestValue

def MinMax(node, playerNum):
    global max_int, maxDepth
    if(abs(node.value) >= max_int):
        return node.value
    if (node.depth <= 0):
        node.value = node.getRewards() * node.playerNum
        return node.value

    sum = 0
    bestValue = (max_int*maxDepth) * -playerNum # possitive p
    bestAverage = 0

    for child in range(0 , node.board.width):
        if (node.board.canPlace(child)): node.children.append(Node(node.depth - 1, -node.playerNum, node.board.place(child, -node.playerNum), 0, child))
        else: node.children.append(Node(0, -node.playerNum, node.board.place(child, -node.playerNum), max_int * node.depth * (node.playerNum), child))
        val = MinMax(node.children[child], -playerNum)
        sum += val
        if (abs(max_int*maxDepth * playerNum - val) < abs(max_int*maxDepth * playerNum - bestValue) or (abs(max_int*maxDepth * playerNum - val) == abs(max_int*maxDepth * playerNum - bestValue) and abs(max_int*maxDepth * playerNum - node.children[child].average) < abs(max_int*maxDepth * playerNum - bestAverage) ) ):
            bestValue = val  # store the found best value in this variable
            bestAverage = node.children[child].average
            node.playColumn = node.children[child].index
    node.average = sum/node.board.width
    return bestValue

def placeTop(board):
    for col in range (0, board.width):
        for row in range (board.height - 2, -1, -1):
            if(board.values[row][col] == 1 and board.values[row+1][col] == 0):
                return col
    return 4

def bestHeuristic(board, playerNum):
    if(playerNum == 2): playerNum = -1
    board = switchJudgeNums(board)
    global maxDepth
    maxDepth = 20
    if(playerNum == -1 and board.count() < 6): return placeTop(board)
    else:
        if(board.count() == 0): return board.width//2
        startDepth = 5
        startTime = time.time()
        answer = 0
        while(True):
            node = Node(startDepth, playerNum * -1, board, 0, 0)
            AlphaBetaMinMax(node, playerNum,-max_int*maxDepth, max_int*maxDepth, startTime)
            if(node.playColumn != -1 and startDepth < 40):
                answer = node.playColumn
            else: break
            if(node.value >= max_int):
                print("Destiny is written.")
                break
            else: startDepth+=1
        return answer


def switchJudgeNums(board):
    for row in range(0, board.height):
        for col in range(0, board.width):
            if(board.values[row][col] == 2): board.values[row][col] = -1
    return board

def main():
    global maxDepth
    board = Board(7,6)
    depth = 6
    maxDepth = depth+1
    player_num = 1
    lastPlay = 2
    move = 0
    while(not board.checkAnyT(lastPlay)):
        if(True):
            move = bestHeuristic(board,player_num)
        else: move = (int(input("Mueve: ")))
        if(not board.realPlace(move,player_num)): break
        board.printGame()
        lastPlay = player_num
        if(player_num == 1): player_num += 1
        else: player_num = 1

if _name_  == '_main_':
    main()
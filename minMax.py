import copy

class Board(object):
    def __init__(self, width, height):
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
                if(self.values[row][col] == -1):
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
        if (row + 1 >= self.height or col + 1 >= self.width or col - 1 < 0): return False
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
    def __init__(self, depth, playerNum, board, value, index):
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
        if (abs(self.value) < max_int):
            if(self.depth > 0):
                self.generateChildren()
            else: self.value = self.getRewards() * (playerNum)

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
            if(left == 50): sumTot += 100
            if(right == 50): sumTot += 100

        if(right == 50):
            if(rightUp == 50): sumTot += 100
            if(rightDown == 50): sumTot +=250

        if(left == 50):
            if(leftUp == 50): sumTot += 100
            if(leftDown == 50): sumTot += 250

        return top + left + right + sumTot

    def checkTwoDiagonal(self):
        return self.checkTwoDiagonalLeftBottom() + self.checkTwoDiagonalLeftTop() + self.checkTwoDiagonalRightBottom() + self.checkTwoDiagonalRightTop()


def MinMax(node, playerNum):
    global max_int, maxDepth
    if (node.depth <= 0) or (abs(node.value) >= max_int):
        #print("Node: ", node.value)# have we reached depth 0 or the best node?
        return node.value  # passing the best node up to the current node

    sum = 0
    bestValue = (max_int*maxDepth) * -playerNum # possitive p
    bestAverage = 0

    for child in (node.children):
        val = MinMax(child, -playerNum)
        sum += val
        if (abs(max_int*maxDepth * playerNum - val) < abs(max_int*maxDepth * playerNum - bestValue) or (abs(max_int*maxDepth * playerNum - val) == abs(max_int*maxDepth * playerNum - bestValue) and abs(max_int*maxDepth * playerNum - child.average) < abs(max_int*maxDepth * playerNum - bestAverage) ) ):
            bestValue = val  # store the found best value in this variable
            bestAverage = child.average
            node.playColumn = child.index
    node.average = sum/node.board.width
    # debug
    #print(bestValue)
    return bestValue

def main():
    global maxDepth
    board = Board(7,6)
    depth = 6
    maxDepth = depth+1
    player_num = 1
    move = 0
    while(not board.checkAnyT(-player_num)):
        if(player_num == 1):
            a = Node(depth, player_num*-1, board, 0, 0)
            print("CHECK!")
            MinMax(a, player_num)
            move = a.playColumn
        else: move = int(input('Enter your move!'))
        if(not board.realPlace(move,player_num)): break
        board.printGame()
        player_num*=-1

if __name__  == '__main__':
    main()
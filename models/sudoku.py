class SudokuSolver:

    def __init__(self, board = None):
        self.solutions = []
        self.board = Board(board)

    def __str__(self):
        return ''

    def solveBoard(self, board, numberOfSolutionsToFind):
        thisBoard = Board(board.getBoard())
        if thisBoard.isSolveable() == False:
            return
        nextUnsolvedIndexAndPossibleSolutions = thisBoard.getNextUnsolvedIndexAndPossibleValues()
        if (nextUnsolvedIndexAndPossibleSolutions['index']) >= 0:
            unsolvedIndex = nextUnsolvedIndexAndPossibleSolutions['index']
            possibleValues = nextUnsolvedIndexAndPossibleSolutions['possibleValues']
            for i in possibleValues:
                thisBoard.setIndexToValue(unsolvedIndex, str(i))
                self.solveBoard(thisBoard, numberOfSolutionsToFind)
                if len(self.solutions) >= numberOfSolutionsToFind:
                    return
        if thisBoard.isSolved():
            self.solutions.append(Board(thisBoard.getBoard()))
        return

    def findUpToNSolutions(self, n):
        self.solveBoard(self.board, n)

    def getFirstSolution(self):
        self.findUpToNSolutions(1)
        if len(self.solutions) > 0:
            return self.solutions[0]
        return Board()

class Board:

    VALID_VALUES = list('123456789')
    SQUARES = [[0,1,2,9,10,11,18,19,20],[3,4,5,12,13,14,21,22,23],[6,7,8,15,16,17,24,25,26],[27,28,29,36,37,38,45,46,47],[30,31,32,39,40,41,48,49,50],[33,34,35,42,43,44,51,52,53],[54,55,56,63,64,65,72,73,74],[57,58,59,66,67,68,75,76,77],[60,61,62,69,70,71,78,79,80]]

    def __init__(self, board = None):
        self.loadBoard(board)

    def __str__(self):
        result = ''
        for i in range(81):
            result += self.getValueAtIndex(i)
        return result

    def prettyPrint(self):
        result = ''
        for i in range(81):
            result += self.getValueAtIndex(i) + ' '
            if (i + 1) % 9 == 0:
                result += '\n'
            elif (i + 1) % 3 == 0:
                result += '| '
            if i == 26 or i == 53:
                result += '- - - | - - - | - - -\n'
        return result

    def getBoard(self):
        return self.cells

    def clearBoard(self):
       self.cells = ['0'] * 81

    def loadBoard(self, board = None):
        self.clearBoard()
        for i in range(len(board or '')):
            self.setIndexToValue(i, board[i])

    def setIndexToValue(self, boardIndex, value):
        if boardIndex >= 0 and boardIndex <= 80:
            self.cells[boardIndex] = self.convertToValidValue(value)

    def getValueAtIndex(self, boardIndex):
        return self.cells[boardIndex]

    def getUnsolvedIndexes(self):
        return filter(lambda index: self.getValueAtIndex(index) not in self.VALID_VALUES, range(81))

    def convertToValidValue(self, value):
        return str(value) if str(value) in self.VALID_VALUES else '0'

    def isSolved(self):
        return self.areRowsSolved() and self.areColumnsSolved() and self.areSquaresSolved()

    def isSolveable(self):
        return self.areRowsValid() and self.areColumnsValid() and self.areSquaresValid()

    def getNextUnsolvedIndexAndPossibleValues(self):
        unsolvedIndexesAndSolutions = []

        unsolvedIndexes = self.getUnsolvedIndexes()
        for index in unsolvedIndexes:
            possibleValuesForThisIndex = self.getPossibleValuesForIndex(index)
            if len(possibleValuesForThisIndex) == 0:
                return {'index': -1, 'possibleValues' : possibleValuesForThisIndex}
            if len(possibleValuesForThisIndex) == 1:
                return {'index': index, 'possibleValues' : possibleValuesForThisIndex}
            unsolvedIndexesAndSolutions.append({'index': index, 'possibleValues': possibleValuesForThisIndex})
        return sorted(unsolvedIndexesAndSolutions, key = lambda k: len(k['possibleValues']))[0] if len(unsolvedIndexesAndSolutions) > 0 else {'index': -1}

    def getPossibleValuesForIndex(self, index):
        possibleValues = self.VALID_VALUES[:]

        row = int(index / 9)
        for i in range(9):
            thisValue = self.getValueAtIndex((row * 9) + i)
            if thisValue in possibleValues:
                possibleValues.pop(possibleValues.index(thisValue))

        col = index % 9
        for i in range(9):
            thisValue = self.getValueAtIndex(col)
            col += 9
            if thisValue in possibleValues:
                possibleValues.pop(possibleValues.index(thisValue))

        for i in range(len(self.SQUARES)):
            if index in self.SQUARES[i]:
                square = i
                break
        for i in self.SQUARES[square]:
            thisValue = self.getValueAtIndex(i)
            if thisValue in possibleValues:
                possibleValues.pop(possibleValues.index(thisValue))
        
        return possibleValues

    def areRowsValid(self):
        for i in [0,9,18,27,36,45,54,63,72]:
            rowValues = []
            for j in range(9):
                if self.getValueAtIndex(i + j) != '0':
                    rowValues.append(self.getValueAtIndex(i + j))
            if len(rowValues) != len(set(rowValues)):
                return False
        return True

    def areColumnsValid(self):
        for i in range(9):
            columnValues = []
            for j in [0,9,18,27,36,45,54,63,72]:
                if self.getValueAtIndex(i + j) != '0':
                    columnValues.append(self.getValueAtIndex(i + j))
            if '0' in columnValues or (len(columnValues) != len(set(columnValues))):
                return False
        return True

    def areSquaresValid(self):
        for i in [0,3,6,27,30,33,54,57,60]:
            squareValues = []
            for j in [0,1,2,9,10,11,18,19,20]:
                if self.getValueAtIndex(i + j) != '0':
                    squareValues.append(self.getValueAtIndex(i + j))
            if '0' in squareValues or (len(squareValues) != len(set(squareValues))):
                return False
        return True

    def areRowsSolved(self):
        for i in [0,9,18,27,36,45,54,63,72]:
            rowValues = []
            for j in range(9):
                rowValues.append(self.getValueAtIndex(i + j))
            if '0' in rowValues or (len(rowValues) != len(set(rowValues))):
                return False
        return True

    def areColumnsSolved(self):
        for i in range(9):
            columnValues = []
            for j in [0,9,18,27,36,45,54,63,72]:
                columnValues.append(self.getValueAtIndex(i + j))
            if '0' in columnValues or (len(columnValues) != len(set(columnValues))):
                return False
        return True

    def areSquaresSolved(self):
        for i in [0,3,6,27,30,33,54,57,60]:
            squareValues = []
            for j in [0,1,2,9,10,11,18,19,20]:
                squareValues.append(self.getValueAtIndex(i + j))
            if '0' in squareValues or (len(squareValues) != len(set(squareValues))):
                return False
        return True

if __name__ == '__main__':
    x = SudokuSolver('800000000003600000070090200050007000000045700000100030001000068008500010090000400')
    #x = SudokuSolver('000005080000601043000000000010500000000106000300000005530000061000000004000000000')
    #x = SudokuSolver('003020600900305001001806400008102900700000008006708200002609500800203009005010300')
    print x.board.prettyPrint()
    print x.getFirstSolution().prettyPrint()

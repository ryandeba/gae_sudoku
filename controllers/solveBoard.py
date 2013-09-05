import webapp2
import json
from models.sudoku import SudokuSolver

class solveBoard(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/json'

        boardValues = str(self.request.get('board'))
        sudokuSolver = SudokuSolver(boardValues)
        
        self.response.write(json.dumps([str(sudokuSolver.getFirstSolution())]))

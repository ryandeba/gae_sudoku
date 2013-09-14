import webapp2
import os
import json
from google.appengine.ext.webapp import template
from models.sudoku import SudokuSolver
from models.sudoku import SudokuMaker

class index(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'views/index.html')
        self.response.write(template.render(path, {}))

class solveBoard(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/json'

        boardValues = str(self.request.get('board'))
        sudokuSolver = SudokuSolver(boardValues)
        
        self.response.write(json.dumps([str(sudokuSolver.getFirstSolution())]))

class newPuzzle(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/json'

        sudokuMaker = SudokuMaker()
        self.response.write(json.dumps([str(sudokuMaker.getNewPuzzle())]))

application = webapp2.WSGIApplication([
    ('/', index),
    ('/solveBoard', solveBoard),
    ('/newPuzzle', newPuzzle),
], debug=True)

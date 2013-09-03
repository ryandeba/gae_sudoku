import os
from google.appengine.ext.webapp import template
import webapp2
import json
from sudoku import SudokuSolver

class index(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.write(template.render(path, {}))

class solveBoard(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Content-Type'] = 'application/json'

        boardValues = str(self.request.get('board'))
        sudokuSolver = SudokuSolver(boardValues)
        
        self.response.write(json.dumps([str(sudokuSolver.getFirstSolution())]))

application = webapp2.WSGIApplication([
    ('/', index),
    ('/solveBoard', solveBoard),
], debug=True)

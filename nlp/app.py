from flask import Flask
from flask_restful import Api, Resource, reqparse

import sys

[sys.path.append(i) for i in ['.', '..']]
from common.play import *

HUMAN = -1
COMPUTER = +1
NOT_PLAYED = 0


class Board(Resource):
    board = [NOT_PLAYED] * 9

    def get(self):
        return {
                   "board": self.board
               }, 200

    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("move")
        args = parser.parse_args()

        free_cells = empty_cells(self.board)
        player_move = int(args.move)
        if player_move in free_cells:
            self.board[player_move] = HUMAN
            computer_move = ai_turn(self.board)
            self.display()
        else:
            return {
                       "message": "The cell is already taken"
                   }, 400

        winner = self.get_winner_name()

        return {
                   "player_move": player_move,
                   "computer_move": computer_move,
                   "winner": winner,
                   "board": self.board
               }, 200

    def get_winner_name(self):
        if wins(self.board, COMPUTER):
            return "computer"
        elif wins(self.board, HUMAN):
            return "human"
        return "no one" if self.board.count(NOT_PLAYED) else "draw"

    def delete(self):
        for i in range(len(self.board)):
            self.board[i] = NOT_PLAYED
        return {
                   "board": self.board
               }, 200

    def display(self):
        for index, value in enumerate(self.board):
            if index % 3 == 0:
                print("")
            print(self.format_value(value), end="|")
        print()

    def format_value(self, value):
        if value == NOT_PLAYED:
            return " "
        elif value == COMPUTER:
            return "O"
        return "X"


if __name__ == "__main__":
    app = Flask(__name__)

    api = Api(app)
    api.add_resource(Board, "/board")

    app.run(
        host='0.0.0.0',
        port=5001,
        debug=True
    )

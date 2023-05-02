
from utils import *
class Field:
    def __init__(self):
        self.field = [[0]*FIELD_W]*FIELD_H

    def size(self):
        return FIELD_W, FIELD_H

    def update_field(self, field):
        self.field = field



    def project_piece_down(self, piece, offsetX, workingPieceIndex):
        if offsetX+len(piece[0]) > FIELD_W or offsetX < 0:
            return None
        #result = copy.deepcopy(self)
        offsetY = FIELD_H
        for y in range(0, FIELD_H):
            if check_collision(self.field, piece, (offsetX, y)):
                offsetY = y
                break
        for x in range(0, len(piece[0])):
            for y in range(0, len(piece)):
                value = piece[y][x]
                if value > 0:
                    self.field[offsetY-1+y][offsetX+x] = -workingPieceIndex
        return self

    def undo(self, workingPieceIndex):
        self.field = [[0 if el == -workingPieceIndex else el for el in row] for row in self.field]

    def height_of_column(self, column):
        _, height = self.size()
        for i in range(0, height):
            if self.field[i][column] != 0:
                return height-i
        return 0

    def heights(self):
        result = []
        width, _ = self.size()
        for i in range(0, width):
            result.append(self.height_of_column(i))
        return result

    def heuristics(self):
        heights = self.heights()
        return [self.aggregate_height(heights), self.complete_line() , self.number_of_holes(heights), self.bumpinesses(heights)]

    def aggregate_height(self, heights):
        result = sum(heights)
        return result

    def complete_line(self):
        result = 0
        _, height = self.size()
        for i in range (0, height) :
            if 0 not in self.field[i]:
                result+=1
        return result

    def bumpinesses(self, heights):
        result = []
        for i in range(0, len(heights)-1):
            result.append(abs(heights[i]-heights[i+1]))
        return sum(result)

    def number_of_holes(self, heights):
        result = 0
        width, height = self.size()
        for j in range(0, width) :
            for i in range (0, height) :
                if self.field[i][j] == 0 and height-i < heights[j]:
                    result+=1
        return result

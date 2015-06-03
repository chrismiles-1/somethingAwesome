import csv


class LifeBoard:
    def __init__(self):
        self.board = []
        self.width = 0
        self.height = 0

    def set_board(self, board):
        self.board = board
        self.width = len(board[0])
        self.height = len(board)

    def get_board(self):
        return self.board

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def invert_cell(self, x, y):
        # since the board is stored as row first, its y,x not x,y
        self.board[y][x] = not (self.board[y][x])
        # change the value of a cell at x, y
        return

    def save_seed(self, file_name):
        # get file
        # write a row as a line, csv

        with open(file_name, 'wb') as seed_save:
            seed_writer = csv.writer(seed_save, delimiter=',')
            seed_writer.writerows(self.board)
            # for row in self.board:
            #    print row
            #    seed_writer.writerow(row)

    def load_seed(self, file_name):
        # get file
        # read a line as a row, csv

        board = []

        with open(file_name) as seed:
            seed_reader = csv.reader(seed, delimiter=',')  # do we need OS.join?
            for row in seed_reader:
                # must convert the row into ints
                board.append(map(int, row))
                # print row

        # print board
        self.set_board(board)

    def count_surrounding_cells(self, pos_x, pos_y):
        surround_cell_count = 0

        # check N,  if y > 0
        if pos_y > 0:
            # print "N",
            surround_cell_count += self.board[pos_y - 1][pos_x]
        # check NE, if y > 0, x < MAX_WIDTH
        if pos_x < self.width - 1 and pos_y > 0:
            # print "NE",
            surround_cell_count += self.board[pos_y - 1][pos_x + 1]
        # check E,  if x < MAX_WIDTH
        if pos_x < self.width - 1:
            # print "E",
            surround_cell_count += self.board[pos_y][pos_x + 1]
        # check SE, if y < MAX_HEIGHT, x < MAX_WIDTH
        if pos_x < self.width - 1 and pos_y < self.height - 1:
            # print "SE",
            surround_cell_count += self.board[pos_y + 1][pos_x + 1]
        # check S,  if y < MAX_HEIGHT
        if pos_y < self.height - 1:
            # print "S",
            surround_cell_count += self.board[pos_y + 1][pos_x]
        # check SW, if y < MAX_HEIGHT, x > 0
        if pos_y < self.height - 1 and pos_x > 0:
            # print "SW",
            surround_cell_count += self.board[pos_y + 1][pos_x - 1]
        # check W,  if x > 0
        if pos_x > 0:
            # print "W",
            surround_cell_count += self.board[pos_y][pos_x - 1]
        # check NW, if y > 0, x > 0
        if pos_y > 0 and pos_x > 0:
            # print "NW",
            surround_cell_count += self.board[pos_y - 1][pos_x - 1]

        # print ""
        return surround_cell_count

    def run(self):
        # run a given amount of cycles at a time
        tmp_board = list()
        tmp_row = list()

        # check surrounding cells
        for row_num in range(len(self.board)):
            for column_num in range(len(self.board[row_num])):

                # debug print
                # print str(column_num) + "x:y" + str(row_num),

                surround_cell_count = self.count_surrounding_cells(column_num, row_num)

                # dead cell
                if self.board[row_num][column_num] == 0:
                    if surround_cell_count == 3:
                        tmp_row.append(1)
                    else:
                        tmp_row.append(0)
                # live cell
                else:
                    if surround_cell_count > 3 or surround_cell_count < 2:
                        tmp_row.append(0)
                    elif surround_cell_count == 2 or surround_cell_count == 3:
                        tmp_row.append(1)

            tmp_board.append(tmp_row)
            tmp_row = list()

        self.board = tmp_board
        return

    def __str__(self):
        str_board = ""
        for cell in self.board:
            str_board += str(cell)
        return str_board

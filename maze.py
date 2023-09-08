#! /usr/bin/env python3
''' Run cool maze generating algorithms. '''
import random

class Cell:
    ''' Represents a single cell of a maze.  Cells know their neighbors
        and know if they are linked (connected) to each.  Cells have
        four potential neighbors, in NSEW directions.
    '''  
    def __init__(self, row, column):
        assert row >= 0
        assert column >= 0
        self.row = row
        self.column = column
        self.links = {}
        self.north = None
        self.south = None
        self.east  = None
        self.west  = None
        
    def link(self, cell, bidirectional=True):
        ''' Carve a connection to another cell (i.e. the maze connects them)'''
        assert isinstance(cell, Cell)
        self.links[cell] = True
        if bidirectional:
            cell.link(self, bidirectional=False)
        
    def unlink(self, cell, bidirectional=True):
        ''' Remove a connection to another cell (i.e. the maze 
            does not connect the two cells)
            
            Argument bidirectional is here so that I can call unlink on either
            of the two cells and both will be unlinked.
        '''
        assert isinstance(cell, Cell)
        del self.links[cell]
        if bidirectional:
            cell.unlink(self, bidirectional=False)
            
    def is_linked(self, cell):
        ''' Test if this cell is connected to another cell.
            
            Returns: True or False
        '''
        assert isinstance(cell, Cell)
        if cell in self.links:
            return True
        else:
            return False
        
    def all_links(self):
        ''' Return a list of all cells that we are connected to.'''
        slist = []
        for i in self.links.keys():
            slist.append(i)
        return slist
        
    def link_count(self):
        ''' Return the number of cells that we are connected to.'''
        count = len(self.links)
        return count
        
    def neighbors(self):
        ''' Return a list of all geographical neighboring cells, regardless
            of any connections.  Only returns actual cells, never a None.
        '''
        neighbors = []
        neighbors.clear()
        if self.north != None:
            neighbors.append(self.north)
        if self.south != None:
            neighbors.append(self.south)
        if self.east != None:
            neighbors.append(self.east)
        if self.west != None:
            neighbors.append(self.west)
        return neighbors
                
    def __str__(self):
        return f'Cell at {self.row}, {self.column}'
        

class Grid:
    ''' A container to hold all the cells in a maze. The grid is a 
        rectangular collection, with equal numbers of columns in each
        row and vis versa.
    '''
    
    def __init__(self, num_rows, num_columns):
        assert num_rows > 0
        assert num_columns > 0
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.grid = self.create_cells()
        self.connect_cells()
        
    def create_cells(self):
        ''' Call the cells into being.  Keep track of them in a list
            for each row and a list of all rows (i.e. a 2d list-of-lists).
            
            Do not connect the cells, as their neighbors may not yet have
            been created.
        '''
        rlists = [[] for i in range(self.num_rows)]
        for i in range(self.num_rows):
            for j in range(self.num_columns):
                c = Cell(i,j)
                rlists[i].append(c)
        return rlists    

            
    def connect_cells(self):
        for cell in self.each_cell():
            row, col = cell.row, cell.column
            cell.north = self.cell_at(row-1, col)
            cell.south = self.cell_at(row+1, col)
            cell.west = self.cell_at(row, col-1)
            cell.east = self.cell_at(row, col+1)
        
    def cell_at(self, row, column):
        ''' Retrieve the cell at a particular row/column index.'''
        if 0 <= row < self.num_rows and 0 <= column < self.num_columns:
            return self.grid[row][column]
        return None
        
    def deadends(self):
        ''' Return a list of all cells that are deadends (i.e. only link to
            one other cell).
        '''
        dlist = [len(self.grid)]
        for i in range(self.num_rows - 1):
            for j in range(self.num_columns - 1):
                if self.grid[i][j].link_count() == 1:
                    dlist.append(self.grid[i][j])
        return dlist

                            
    def each_cell(self):
        ''' A generator.  Each time it is called, it will return one of 
            the cells in the grid.
        '''
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                c = self.cell_at(row, col)
                yield c
                
    def each_row(self):
        ''' A row is a list of cells.'''
        for row in self.grid:
            yield row
               
    def random_cell(self):
        ''' Chose one of the cells in an independent, uniform distribution. '''
        a = random.randint(0,self.num_rows-1)
        b = random.randint(0,self.num_columns-1)
        c = self.grid[a][b]
        return c
        
    def size(self):
        ''' How many cells are in the grid? '''
        size = len(self.grid)
        return size
        
    def set_markup(self, markup):
        ''' Warning: this is a hack.
            Keep track of a markup, for use in representing the grid
            as a string.  It is used in the __str__ function and probably
            shouldn't be used elsewhere.
        '''
        self.markup = markup
        
    def __str__(self):
        ret_val = '+' + '---+' * self.num_columns + '\n'
        for row in self.grid:
            ret_val += '|'
            for cell in row:
                cell_value = self.markup[cell]
                ret_val += '{:^3s}'.format(str(cell_value))
                if not cell.east:
                    ret_val += '|'
                elif cell.east.is_linked(cell):
                    ret_val += ' '
                else:
                    ret_val += '|'
            ret_val += '\n+'
            for cell in row:
                if not cell.south:
                    ret_val += '---+'
                elif cell.south.is_linked(cell):
                    ret_val += '   +'
                else:
                    ret_val += '---+'
            ret_val += '\n'
        return ret_val
        
class Markup:
    ''' A Markup is a way to add data to a grid.  It is associated with
        a particular grid.
        
        In this case, each cell can have a single object associated with it.
        
        Subclasses could have other stuff, of course
    '''
    
    def __init__(self, grid, default=' '):
        self.grid = grid
        self.marks = {}  # Key: cell, Value = some object
        self.default = default
        
    def reset(self):
        self.marks = {}
        
    def __setitem__(self, cell, value):
        self.marks[cell] = value
        
    def __getitem__(self, cell):
        return self.marks.get(cell, self.default)
        
    def set_item_at(self, row, column, value):
        assert row >= 0 and row < self.grid.num_rows
        assert column >= 0 and column < self.grid.num_columns
        cell = self.grid.cell_at(row, column)
        if cell:
            self.marks[cell]=value
        else:
            raise IndexError
    
    def get_item_at(self, row, column):
        assert row >= 0 and row < self.grid.num_rows
        assert column >= 0 and column < self.grid.num_columns
        cell = self.grid.cell_at(row, column)
        if cell:
            return self.marks.get(cell)
        else:
            raise IndexError
            
    def max(self):
        ''' Return the cell with the largest markup value. '''
        return max(self.marks.keys(), key=self.__getitem__)

    def min(self):
        ''' Return the cell with the largest markup value. '''
        return min(self.marks.keys(), key=self.__getitem__)


def abw_improvement(grid):
# improve AB+Wilson to get a faster algorithm
# through the print we can see that when the switch boundary is 1/4 of unvisit list has been visited, the step need is about 1500 and the loop remove is about 400
# if the amount is less than 1/4 , such as 1/6, the removed loops will be unstable, sometimes 700+ and sometimes 400
# if the amount is bigger than 1/4 ,such as 1/2, the remove loops will still be about 400
# so we can get the algorithm with less loops to remove and less steps to execute comparing to ab and wilson, which is better.

    unvisit = []
    while_loop = 1
    loops_removed = 0
    walk = []
    for i in range(grid.num_rows):
            for j in range(grid.num_columns): 
                   unvisit.append(grid.grid[i][j])
    size = len(unvisit)
    a = random.randint(0,grid.num_rows-1)
    b = random.randint(0,grid.num_columns-1)
    unvisit.remove(grid.grid[a][b])
    while len(unvisit) > (3*size/4):    
        nlist = grid.grid[a][b].neighbors()
        nlen = len(nlist)-1
        idx = random.randint(0,nlen)
        if nlist[idx] == grid.grid[a][b].north:
                a_new = a-1
                b_new = b
        elif nlist[idx] == grid.grid[a][b].south:
                a_new = a+1
                b_new = b
        elif nlist[idx] == grid.grid[a][b].east:
                a_new = a
                b_new = b+1
        else:
                a_new = a
                b_new = b-1
        if unvisit.count(nlist[idx]) != 0:
            unvisit.remove(nlist[idx])
            grid.grid[a][b].link(nlist[idx])
            a = a_new
            b = b_new
        else:
            a = a_new
            b = b_new
        while_loop += 1
    while unvisit:    
        nlist = grid.grid[a][b].neighbors()
        nlen = len(nlist)-1
        idx = random.randint(0,nlen)
        if nlist[idx] == grid.grid[a][b].north:
                a_new = a-1
                b_new = b
        elif nlist[idx] == grid.grid[a][b].south:
                a_new = a+1
                b_new = b
        elif nlist[idx] == grid.grid[a][b].east:
                a_new = a
                b_new = b+1
        else:
                a_new = a
                b_new = b-1
        if walk.count(grid.grid[a_new][b_new]) != 0:
            idx = walk.index(grid.grid[a_new][b_new])
            walk = walk[:idx+1]
            a = a_new
            b = b_new
            loops_removed += 1
        elif unvisit.count(grid.grid[a_new][b_new]) == 0:
            walk.append(grid.grid[a_new][b_new])
            wlen = len(walk)-1
            for i in range(wlen):
                unvisit.remove(walk[i])
            for i in range(wlen):
                walk[i].link(walk[i+1])
            walk.clear()
            if unvisit:
                a = unvisit[0].row
                b = unvisit[0].column
                walk.append(unvisit[0])
        else:
            walk.append(grid.grid[a_new][b_new])
            a = a_new
            b = b_new    
            while_loop += 1

def improved_sidewinder(grid, odds=.35, e=3):
    # avg: sidewinder 每个 run 平均 avg 个格子就有一个向上开口
    assert odds >= 0.0
    assert odds < 1.0
    grid_rows = list(grid.each_row())
    half_rows = grid_rows[:len(grid_rows) // 2 + 1]  # only works if len(grid_row) is even

    def symmetric_cell(cell):
        loc = (cell.row, cell.column)
        sym_cel = grid.cell_at(grid.num_rows - loc[0] - 1, loc[1])
        return sym_cel

    for row in half_rows:
        run = []
        cell_up = []
        for cell in row:
            run.append(cell)
            close = cell.east is None or (cell.north is not None and random.random() < odds and cell.south is not None)
            if close:
                for i in range(len(run) // e + 1):
                    cell_up.append(random.choice([c for c in run if c not in cell_up]))
                while cell_up:
                    cel = cell_up.pop()
                    sym_cel = symmetric_cell(cel)
                    if cel.north:
                        cel.link(cel.north)
                    if sym_cel.south:
                        sym_cel.link(sym_cel.south)
                run = []
                # room_size = 0
            else:
                cell.link(cell.east)
                sym_cel = symmetric_cell(cell)
                sym_cel.link(sym_cel.east)
    create_base(grid)

def create_base(grid, size_rows = 3, size_cols = 3):
    total_rows = grid.num_rows
    total_columns = grid.num_columns
    if total_rows % 2 == 0: size_rows = size_rows  + 1
    if total_columns % 2 == 0: size_cols = size_cols + 1

    # choose a random row and link its sides.
    random_row = random.randint(1, total_rows - 2)
    link_side(grid, random_row)
    link_side(grid, total_rows - random_row - 1)


    center_cells = []
    for row in range((total_rows - size_rows) // 2,
                     (total_rows - size_rows) // 2 + size_rows):
        for col in range((total_columns - size_cols) // 2,
                         (total_columns - size_cols) // 2 + size_cols):
            center_cells.append(grid.cell_at(row, col))

    for cell in center_cells:
        for neighbor in cell.neighbors():
            if neighbor in center_cells and not cell.is_linked(neighbor):
                cell.link(neighbor)

def link_side(grid: Grid, row):
    total_columns = grid.num_columns
    rightmost = grid.cell_at(row, total_columns - 1)
    leftmost = grid.cell_at(row, 0)
    rightmost.east = leftmost
    leftmost.west = rightmost
    leftmost.link(rightmost)
    #rightmost.link(leftmost)



class DijkstraMarkup(Markup):
    ''' A markup class that will run Djikstra's algorithm and keep track
        of the distance values for each cell.
    '''

    def __init__(self, grid, root_cell, default=0):
        ''' Execute the algorithm and store each cell's value in self.marks[]
        '''
        super().__init__(grid, default)
        for i in range(self.grid.num_rows):
            for j in range(self.grid.num_columns):
                self.marks[self.grid.grid[i][j]] = None
        self.marks[root_cell] = 0
        frontier = []
        frontier.append(root_cell)
        while frontier:
            flist = {}
            flen = len(frontier)
            for i in range(flen):
                flist[frontier[i]] = self.marks[frontier[i]]
            c = min(flist, key=flist.get)
            frontier.remove(c)
            nlist = c.neighbors()
            nlen = len(nlist)
            remove= []
            for i in range(nlen):
                if c.is_linked(nlist[i]) == False:
                    remove.append(nlist[i])
            for i in range(len(remove)):
                nlist.remove(remove[i])
            nlen = len(nlist)
            for i in range(nlen):
                if self.marks[nlist[i]] == None:
                    self.marks[nlist[i]] = self.marks[c]+1
                    frontier.append(nlist[i])
           
    def farthest_cell(self):
        ''' Find the cell with the largest markup value, which will
            be the one farthest away from the root_call.
            
            Returns: Tuple of (cell, distance)
        '''
        c = max(self.marks, key=self.marks.get)
        d = self.marks[c]
        farthest = (c,d)
        return farthest
    
class ShortestPathMarkup(DijkstraMarkup):
    ''' Given a starting cell and a goal cell, create a Markup that will
        have the shortest path between those two cells marked.  
    '''
    def __init__(self, grid, start_cell, goal_cell):
        super().__init__(grid, start_cell)
        self.path = []
        loop = True
        self.path.append(goal_cell)
        c = goal_cell
        while loop:
            nlist = c.neighbors()
            nlen = len(nlist)
            remove= []
            for i in range(nlen):
                if c.is_linked(nlist[i]) == False:
                    remove.append(nlist[i])
            for i in range(len(remove)):
                nlist.remove(remove[i])
            nlen = len(nlist)
            nmin = nlist[0]
            for i in range(nlen):
                if self.marks[nlist[i]] <= self.marks[nmin]:
                    nmin = nlist[i]
            self.path.append(nmin)
            if self.marks[nmin] == 0:
                loop = False
            c = nmin

def BFS_distance(grid, start, end):
    start_cell = grid.cell_at(start[0], start[1])
    end_cell = grid.cell_at(end[0], end[1])
    frontier = [start_cell]
    visited = set()
    distance = {start_cell: 0}
    while frontier:
        cell = frontier.pop(0)
        visited.add(cell)
        if cell == end_cell:
            return distance[cell]
        for neighbor in cell.links.keys():
            if neighbor not in visited and cell.links[neighbor]:
                distance[neighbor] = distance[cell] + 1
                frontier.append(neighbor)

    return None


def DistAllFood(grid, distanceFunction = BFS_distance):
    #初始化所有食物的位置
    start_pos = (grid.num_rows - 1, grid.num_columns - 1)
    foods = []
    for i in range(grid.num_rows):
        for j in range(grid.num_columns):
            foods.append((i, j))

    # a function to get all subsets
    def generate_subsets(food_list):
        if not food_list:
            return [[]]
        subsets = generate_subsets(food_list[1:])
        return subsets + [[food_list[0]] + subset for subset in subsets]

    all_subsets_of_foods = generate_subsets(foods)
    distance = {}
    distance[([start_pos], start_pos)] = 0

    for s in range(2, len(foods) + 1):
        for subset in all_subsets_of_foods:
            if len(subset) == s and start_pos in subset:
                distance[(subset, start_pos)] = float('inf')
                for food_pos in subset:
                    if food_pos != start_pos:
                        st = subset
                        st.remove(food_pos)
                        distance[(subset, food_pos)] = min(distance[(st, i)] + distanceFunction(grid, i, food_pos) for i in subset and i != j)

    return min(distance[(foods, j)] for j in foods)



    

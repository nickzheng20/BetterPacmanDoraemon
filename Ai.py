import itertools

import maze
import heapq
import random
def manhattanDistance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

class GameState:
    def __init__(self, grid: maze.Grid, position: tuple, food_list: list, parent=None):
        self.parent = parent
        self.grid = grid
        self.num_rows = self.grid.num_rows
        self.num_cols = self.grid.num_columns
        self.food_list = food_list
        self.position = position
        self.current_cell = self.grid.cell_at(position[0], position[1])
        self.total_num_foods = self.grid.size()
        self.current_num_foods = len(self.food_list)

    def isWin(self):
        if self.food_list == []:
            return True
        return False

    def getSuccessorStates(self):
        if self.isWin():
            return None
        successor_states = []
        for next_cell in self.current_cell.all_links():
            x = next_cell.row
            y = next_cell.column
            next_food_list = self.food_list.copy()
            next_pos = (x, y)
            if next_pos in next_food_list:
                next_food_list.remove((x, y))
            successor_states.append(GameState(self.grid, next_pos, next_food_list, self))

        return successor_states


    def closestFood(self, distanceFunction = manhattanDistance):
        return min(distanceFunction(food, self.position) for food in self.food_list)

    def getScore(self):
        score = self.parent.getScore() - 1
        score += 1/self.closestFood(maze.BFS_distance)
        return score


def generate_coordinates(n, x_range, y_range):
    coordinates = []
    for _ in range(n):
        x = random.randint(0, x_range - 1)
        y = random.randint(0, y_range - 1)
        coordinates.append((x, y))
    return coordinates

"""
class Problem:
    def __init__(self, grid: maze.Grid):
        self.start = (grid.num_rows - 1, grid.num_columns - 1)
"""


def BFS_search(grid: maze.Grid):
    # Initialize start node
    start_pos = (grid.num_rows - 1, grid.num_columns - 1)
    initial_foodlist = generate_coordinates(10, grid.num_rows, grid.num_columns)
    start_node = GameState(grid, start_pos, initial_foodlist)

    next = start_node.getSuccessorStates()
    # Initialize BFS
    queue = [(start_node, 0)]
    visited = set()
    time = 0
    while queue:
        time += 1
        state, distance = queue.pop(0)
        mem = (state.position, tuple(state.food_list))
        print(state.position, f"foodlist: {state.food_list}")
        if mem not in visited:
            visited.add(mem)
            if state.isWin():
                print(time)
                return distance
            for successor in state.getSuccessorStates():
                if successor not in visited:
                    queue.append((successor, distance + 1))

    print(time)
    return None



def foodHeuristic(state: GameState):
    foodlist = state.food_list
    position = state.position
    def mstFood(foodlist :list):
        visited = set()
        visited.add(foodlist[0])
        sum = 0
        while len(visited) < len(foodlist):
            min = float('inf')
            for food in foodlist:
                if food not in visited:
                    for visited_food in visited:
                        distance = maze.BFS_distance(state.grid,visited_food, food)
                        if distance < min:
                            min = distance
                            new_food = food
            visited.add(new_food)
            sum = sum + min
        return sum
    if len(foodlist) == 0:
        return 0
    distance = min([maze.BFS_distance(state.grid, food, position) for food in foodlist])
    return distance + mstFood(foodlist)






def aStarSearch(grid: maze.Grid, n = 5):
    # Initialize start node
    start_pos = (grid.num_rows - 1, grid.num_columns - 1)
    #initial_foodlist = [(i, j) for i in range(grid.num_rows) for j in range(grid.num_columns) if (i, j) != start_pos]
    initial_foodlist = generate_coordinates(n, grid.num_rows, grid.num_columns) + [(0, 0)]
    print(initial_foodlist)
    start_node = GameState(grid, start_pos, initial_foodlist)
    counter = itertools.count()

    # Initialize BFS
    queue = []
    heapq.heappush(queue, (0, next(counter), 0, start_node))
    visited = set()
    time = 0
    while queue:
        time += 1
        _, _, distance, state = heapq.heappop(queue)
        mem = (state.position, tuple(state.food_list))
        #print(state.position, f"foodlist: {state.food_list}")
        if mem not in visited:
            visited.add(mem)
            if state.isWin():
                #print(time)
                return distance
            for successor in state.getSuccessorStates():
                if successor not in visited:
                    total_cost = distance + 1
                    aster_cost = foodHeuristic(successor) + total_cost
                    heapq.heappush(queue, (aster_cost, next(counter), total_cost, successor))

    #print(time)
    return None

def greedy_search(grid: maze.Grid):
    # Initialize start node
    start_pos = (grid.num_rows - 1, grid.num_columns - 1)
    initial_foodlist = [(i, j) for i in range(grid.num_rows) for j in range(grid.num_columns) if (i, j) != start_pos]
    start_node = GameState(grid, start_pos, initial_foodlist)
    counter = itertools.count()

    # Initialize BFS
    queue = []
    heapq.heappush(queue, (0, next(counter), 0, start_node))
    visited = set()
    time = 0
    while queue:
        time += 1
        _, _, distance, state = heapq.heappop(queue)
        mem = (state.position, tuple(state.food_list))
        #print(state.position, f"foodlist: {state.food_list}")
        if mem not in visited:
            visited.add(mem)
            if state.isWin():
                #print(time)
                return distance
            for successor in state.getSuccessorStates():
                if successor not in visited:
                    total_cost = distance + 1
                    greedy_cost = foodHeuristic(successor)
                    heapq.heappush(queue, (greedy_cost, next(counter), total_cost, successor))

    #print(time)
    return None
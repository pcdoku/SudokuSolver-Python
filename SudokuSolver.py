""""
https://github.com/LiorSinai/SudokuSolver-Python
31 May 2020

Sudoku Solver
Working on:
* supporting other grid sizes and box sizes

TODO: (in no particular order)
1) detect if there are multiple solutions
2) count # of solutions (up to some limit)
3) add optional constraints which apply to the whole puzzle:
    diagonal +
    diagonal -
    anti-knight
    anti-king
    non-consecutive
    disjoint groups
4) add optional constraints placed on the grid:
    Thermometers
    Kropki dots (ratios, differences)
    XV
    Quadruples
    Even or Odd digits
5) add option to apply constraints only to a fractal path or certain regions
6) add more strategies for the solver
7) decode https://www.f-puzzles.com/ exported url to import puzzle?
"""

from copy import deepcopy, copy
from typing import List, Tuple, Set
from itertools import combinations
import random
import time 
from SudokuGrid import SudokuGrid
import Sudoku

BOX_SIZE = 3

class SudokuSolver():
    def solveSudoku(self, grid: SudokuGrid, verbose=True, all_solutions=False, constraints=None):
        # idea based on https://dev.to/aspittel/how-i-finally-wrote-a-sudoku-solver-177g
        # Try each step until failure, and repeat:
        # 1) write numbers with only have 1 option
        # 2) write candidates with only 1 option/ 2 pairs
        # 3) with multiple options, take a guess and branch (backtrack)
        def solve(game: Sudoku, depth=0, progress_factor=1 ):
            nonlocal calls, depth_max, progress, progress_update, update_increment
            calls += 1
            depth_max = max(depth, depth_max)
            solved = False
            while not solved:
                print(str(game.grid))  
                solved = True  # assume solved
                edited = False  # if no edits, either done or stuck
                for i in range(game.grid.size):
                    for j in range(game.grid.size):
                        if game.grid.grid_list[i][j] == 0:
                            solved = False
                            options = game.grid.candidates[i][j] 
                            #options = game.find_options(i, j)
                            if len(options) == 0:
                                progress += progress_factor
                                return game.grid, False # this call is going nowhere
                            elif len(options) == 1:  # Step 1
                                #game.grid[i][j] = list(options)[0]
                                game.place_and_erase(i, j, list(options)[0]) # Step 2
                                #game.flush_candidates() # full grid cleaning
                                edited = True
                if not edited: # changed nothing in this round -> either done or stuck
                    if solved:
                        progress += progress_factor
                        solution_set.append(str(game.grid))
                        #print(len(solution_set), solution_set[-1])
                        return game.grid, True
                    else:
                        # Find the box with the least number of options and take a guess
                        # The erase() changes this dynamically in the previous for loop
                        min_guesses = (game.grid.size + 1, -1)
                        for i in range(game.grid.size):
                            for j in range(game.grid.size):
                                options = game.grid.candidates[i][j] 
                                #options = game.find_options(i, j)
                                if len(options) < min_guesses[0] and len(options) > 1:
                                    min_guesses = (len(options), (i, j))
                        i, j = min_guesses[1]
                        options = game.grid.candidates[i][j] 
                        #options = game.find_options(i, j) 
                        # backtracking check point:
                        progress_factor *= (1/len(options)) 
                        for y in options:
                            game_next = deepcopy(game)
                            #game_next.grid[i][j] = y
                            game_next.place_and_erase(i, j, y)
                            #game_next.flush_candidates() # full grid cleaning
                            grid_final, solved = solve(game_next, depth=depth+1, progress_factor=progress_factor)
                            if solved and not all_solutions:
                                break # return 1 solution
                            if progress > progress_update and verbose:
                                print("%.1f" %  (progress*100), end='...')
                                progress_update = ((progress//update_increment) + 1) * update_increment
                        return grid_final, solved
            return game.grid, solved
        
        calls, depth_max = 0, 0
        progress, update_increment, progress_update = 0, 0.01, 0.01
        solution_set = []

        # used to supress the unused variable warning
        progress = progress
        progress_update = progress_update

        game = Sudoku.Sudoku(grid, constraints) 
        print("after creation")
        print(str(game.grid))  
        game.flush_candidates()  # check for obvious candidates
        print("after flush candidates")
        print(str(game.grid))  
        
        possible, message = game.check_possible()
        if not possible:
            print('Error on board. %s' % message)
            info = {
                'calls': calls, 
                'max depth': depth_max, 
                'solutions': len(solution_set), 
                'solution set': solution_set
            }
            return grid, False, info

        grid_final, solved = solve(game, depth=0)

        if len(solution_set) >= 1:
            solved = True
            grid_final = SudokuGrid(solution_set[0])

        info = {
            'calls': calls, 
            'max depth': depth_max, 
            'solutions': len(solution_set), 
            'solution set': solution_set}
        return grid_final, solved, info

def batch_solve(file_name):
    print(f"\nSolving puzzles from {file_name}")
    puzzles = []
    with open(file_name, 'r') as f:
        puzzles = f.read().strip().split('\n')
    
    t0 = time.time()
    max_t = [0, -1] # time, k
    max_calls, max_depth = [0,0,-1], [0,0,-1]  #[calls, max depth, k]
    num_solved = 0
    mean_calls = 0
    for k, puzzle in enumerate(puzzles):
        tk0 = time.time()
        puzzle = SudokuGrid(puzzle)
        _, done, info = SudokuSolver().solveSudoku(puzzle, verbose=False, all_solutions=False)
        deltaTk = time.time() - tk0
        num_solved += done
        mean_calls = (mean_calls * k + info['calls']) / (k + 1) # update average
        ## set maximums
        max_t = max(max_t, [deltaTk, k])
        max_calls = max(max_calls, [info['calls'], info['max depth'], k])
        max_depth = max(max_depth, [info['calls'], info['max depth'], k], key=lambda x:x[1])
        if info['solutions'] > 1:
            print('error: puzzle %d has %d solution' % (k, info['solutions']))
    deltaT = time.time() - t0
    print(' ')
    print("number solved: %d/%d" % (num_solved, len(puzzles)))
    print("total time: %.5fs; average time: %.5fs," % (deltaT, deltaT/len(puzzles)))
    print("max time, # puzzle ", max_t)
    print("max calls, depth, # puzzle:", max_calls)
    print("calls, max(max depth), # puzzle:", max_depth)
    print("average calls: %.1f" % mean_calls)

if __name__ == '__main__':
    ''' Execute the puzzles in the puzzles '''
    batch_solve('sudoku_top95.txt')    # from https://norvig.com/sudoku.html. Solver at https://www.sudokuwiki.org/sudoku.htm can solve 67, but not 6 
    batch_solve('sudoku_hardest.txt')  # from https://norvig.com/sudoku.html  
    batch_solve('Sudoku_NY.txt')       # from the New York Times


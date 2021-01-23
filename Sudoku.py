from typing import List, Tuple, Set
from itertools import combinations
from SudokuGrid import SudokuGrid

class Sudoku():
    ''' Applies constraints and strategies to a grid '''
    def __init__(self, grid: SudokuGrid, constraints = None):
        #assert len(grid[0]) == n, "Grid is not square. n_rows=%d, n_columns=%d" % (n, len(grid[0]))
        self.grid = grid
        # create a grid of viable candidates for each position
        candidates = []
        for i in range(self.grid.size):
            row = []
            for j in range(self.grid.size):
                if grid.grid_list[i][j] == 0:
                    row.append(self.find_options(i, j))
                else:
                    row.append(set())
            candidates.append(row)
        self.grid.candidates = candidates
        self.is_nonconsecutive = False
        for c in constraints or []:
            if c == "nonconsecutive":
                self.is_nonconsecutive = True
                self.erase_all_nonconsecutive()

    def erase_all_nonconsecutive(self):  
        if not self.is_nonconsecutive:
            return                            
        grid_size = self.grid.size
        erased = []
        for i in range(grid_size):
            for j in range(grid_size): 
                if self.grid.grid_list[i][j] != 0:
                    erased += self.erase_consecutive_adjacent(i, j, self.grid.grid_list[i][j])
        self.constraint_propogation(erased)
        
    def __repr__(self) -> str:
        repr = ''
        for row in self.grid.grid_list:
            repr += str(row) + '\n'
        return repr

    def get_box(self, r: int, c: int) -> List[int]:
        box = []
        for i, j in self.grid.get_region_inds(r, c):
            box.append(self.grid.grid_list[i][j])
        return box

    def counting(self, arr:List[int]) -> List[int]:
        """ count occurances in an array """
        count = [0] * (self.grid.size + 1)
        for x in arr:
            count[x] += 1
        return count

    def all_unique(self, arr: List[int]) -> bool:
        """ verify that all numbers are used, and at most once """
        count = self.counting(arr)
        for c in count[1:]:  # ignore 0
            if c != 1:
                return False
        return True

    def is_consecutive(self,r1,c1,r2,c2):
        return (abs(self.grid.grid_list[r1][c1] - self.grid.grid_list[r2][c2]) == 1)

    def all_values(self, arr):
        count = self.counting(arr)
        missing = None
        for num, c in enumerate(count[1:]): # exclude 0:
            if c == 0:
                return False, num+1 # no value or candidate exists
        return True, missing

    def no_duplicates(self, arr):
        count = self.counting(arr)
        for c in count[1:]: # exclude 0:
            if c > 1:
                return False # no value or candidate exists
        return True
    
    def get_candidates(self, start, end):
        " get candidates within two corners of a rectangle/column/row"
        candidates = set()
        for i in range(start[0], end[0] + 1):
            for j in range(start[1], end[1] + 1) :
                candidates = candidates | self.grid.candidates[i][j]
        return candidates

    def check_possible(self):
        """ check if each row/column/box can have all unique elements"""
        # get rows
        rows_set = []
        for i in range(self.grid.size):
            inds = [(i, j) for j in range(self.grid.size)]
            rows_set.append(inds)
        # get columns
        cols_set = []
        for j in range(self.grid.size):
            inds = [(i, j) for i in range(self.grid.size)]
            cols_set.append(inds)
        # check rows and columns
        type = ['row', 'column']
        for t, inds_set in enumerate([rows_set, cols_set]):
            for k, inds in enumerate(inds_set):
                arr = [self.grid.grid_list[i][j] for i, j in inds]
                if not self.no_duplicates(arr):
                    return False, 'Duplicate values in %s %d' % (type[t], k)
                arr += list(self.get_candidates(inds[0], inds[-1]))
                possible, missing = self.all_values(arr)
                if not possible:
                    return False, '%d not placeable in %s %d' % (missing, type[t], k)
        # check boxes
        for i0 in range(0, self.grid.size, self.grid.box_height):
            for j0 in range(0, self.grid.size, self.grid.box_width):
                arr = self.get_box(i0, j0)[:]
                if not self.no_duplicates(arr):
                    return False, 'Duplicate values in box (%d, %d)' % (i0, j0)
                for i in range(i0, i0 + self.grid.box_height):
                    for j in range(j0, j0 + self.grid.box_width):
                        arr += list(self.grid.candidates[i][j])
                possible, missing = self.all_values(arr)
                if not possible:
                    return False, '%d not placeable in box (%d, %d)' % (missing, i0, j0)
        return True, None

    ## ------- Candidate functions -------- ##
    def place_and_erase(self, r: int, c: int, x: int, constraint_prop=True):
        """ remove x as a candidate in the grid in this row, column and box"""
        self.place(r,c,x)
        self.grid.candidates[r][c] = set()
        # remove candidate  x in neighbours
        inds_row = [(r, j) for j in range(self.grid.size)]
        inds_col = [(i, c) for i in range(self.grid.size)]
        inds_box = self.grid.get_region_inds(r, c)
        erased = [(r, c)]  # set of indices for constraint propogration
        erased += self.erase([x], inds_row + inds_col + inds_box, [])
        self.constraint_propogation(erased, constraint_prop=constraint_prop)

    def constraint_propogation(self, erased_indices, constraint_prop=True):    
        # constraint propogation, through every index that was changed
        while erased_indices and constraint_prop:
            i, j = erased_indices.pop()
            inds_row = [(i, j) for j in range(self.grid.size)]
            inds_col = [(i, j) for i in range(self.grid.size)]
            inds_box = self.grid.get_region_inds(i, j)
            erased_indices += self.hidden_naked_singles_pairs_triples([inds_row, inds_col, inds_box], types=[1, 2, 3])
            
            pointers = self.pointing_combos(inds_box)
            for line, inds_pointer, num in pointers:
                erased_indices += self.erase(num, line, inds_pointer)
        # keeps = self.box_line_reduction(inds_box) # doesn't work??
        # for inds_keep, nums in keeps:
        #     self.erase(nums, inds_box, inds_keep)
    
    def place(self, r: int, c: int, x: int):
         self.grid.grid_list[r][c] = x
         if self.is_nonconsecutive:
             self.erase_consecutive_adjacent(r, c, x)
         
    def erase_consecutive_adjacent(self, r: int, c: int, x: int):
        erased = []
        for row in range(r-1, r+1):
            for col in range(c-1, c+1):
                if row >= 0 and col >=0 and (row == r or col == c):
                    edited = False
                    if (x+1 in self.grid.candidates[row][col]):
                        self.grid.candidates[row][col].remove(x+1)
                        edited = True
                    if (x-1 in self.grid.candidates[row][col]):
                        self.grid.candidates[row][col].remove(x-1)
                        edited = True
                    if edited:
                        erased.append((row,col))   
        return erased                      
           
    def erase(self, nums, indices, keep):
        """ erase nums as candidates in indices, but not in keep"""
        erased = []
        for i, j in indices:
            edited = False
            if ((i, j) in keep): 
                continue
            for x in nums:
                if (x in self.grid.candidates[i][j]):
                    self.grid.candidates[i][j].remove(x)
                    edited = True
            if edited:
                erased.append((i,j))            
        return erased

    def set_candidates(self, nums, indices):
        """set candidates at indices. Remove all other candidates"""
        erased = []
        for i, j in indices:
            old = self.grid.candidates[i][j].intersection(nums) # beware triples where the whole triple is not in each box
            if self.grid.candidates[i][j] != old: 
                self.grid.candidates[i][j] = old.copy()
                erased.append((i, j)) # made changes here
        return erased
            
    def count_candidates(self, indices):
        count = [[] for _ in range(self.grid.size + 1)]
        # get counts
        for i, j in indices:
            for num in self.grid.candidates[i][j]:
                count[num].append((i, j))
        return count

    def get_unique(self, indices, type=(0, 1, 2)):
        # See documentation at https://www.sudokuwiki.org/Hidden_Candidates
        groups = self.count_candidates(indices)
        uniques = []  # final set of unique candidates to return
        uniques_temp = {2: [], 3: []} # potential unique candidates
        for num, group_inds in enumerate(groups):
            c = len(group_inds)
            if c == 1 and (1 in type):
                uniques.append((group_inds, [num]))
            if c == 2 and ((2 in type) or (3 in type)):
                uniques_temp[2].append(num)
            if c == 3 and (3 in type):
                uniques_temp[3].append(num)
        uniques_temp[3] += uniques_temp[2]
        # check for matching combos (both hidden and naked)
        for c in [2, 3]:
            if c not in type:
                continue
            for combo in list(combinations(uniques_temp[c], c)): # make every possible combination
                group_inds = set(groups[combo[0]])
                for k in range(1, c):
                    group_inds = group_inds | set(groups[combo[k]]) # if positions are shared, this will not change the length
                if len(group_inds) == c:
                    # unique combo (pair or triple) found 
                    uniques.append((list(group_inds), combo))
        return uniques

    def pointing_combos(self, inds_box):
        # See documentation https://www.sudokuwiki.org/Intersection_Removal
        # inds_box should come from self.get_inds_box()
        groups = self.count_candidates(inds_box)
        pointers = []
        for num, indices in enumerate(groups):
            # need a pair or triple
            if len(indices) == 2 or len(indices) == 3:
                row_same, col_same = True, True
                i0, j0 = indices[0]
                for i, j in indices[1:]:
                    row_same = row_same and (i == i0)
                    col_same = col_same and (j == j0)
                if row_same:
                    line = [(i0, j) for j in range(self.grid.size)]
                    pointers.append((line, indices, [num]))
                if col_same:
                    line = [(i, j0) for i in range(self.grid.size)]
                    pointers.append((line, indices, [num]))
        return pointers

    # TODO: not used
    def box_line_reduction(self, inds_box):
        # See documentation https://www.sudokuwiki.org/Intersection_Removal
        # inds_box should come from self.get_inds_box()
        keeps = []
        i0, j0 = inds_box[0]
        i1, j1 = min(i0 + self.grid.box_height, self.grid.size - 1), min(j0 + self.grid.box_width, self.grid.size - 1)
        # check rows
        for i in range(i0, i1 +  1):
            row = self.get_candidates((i, j0), (i, j1))
            line = self.get_candidates((i, 0), (i, j0 -1)) | self.get_candidates((i, j1 + 1), (i, self.grid.size - 1)) 
            uniques = row.difference(line)   
            if uniques:
                keeps.append(([(i, j) for j in range(j0, j1 + 1)], list(uniques)))
        # check columns
        for j in range(j0, j1 + 1):
            col = self.get_candidates((i0, j), (i1, j))
            line = self.get_candidates((0, j), (i0 - 1, j)) | self.get_candidates((i1 + 1, j), (self.grid.size - 1, j)) 
            uniques = col.difference(line)  
            if uniques:
                keeps.append(([(i, j) for i in range(i0, i1 + 1)], list(uniques)))
        return keeps


    def __get_indices_for_rows_and_columns(self):
        ''' get indices by row '''
        inds_set = []
        for i in range(self.grid.size):
            inds = [(i, j) for j in range(self.grid.size)]
            inds_set.append(inds)
        # check in column
        for j in range(self.grid.size):
            inds = [(i, j) for i in range(self.grid.size)]
            inds_set.append(inds)
        return inds_set

        
    def flush_candidates(self) -> None:
        """set candidates across the whole grid, according to logical strategies"""
        # get indices for each set
        inds_box = self.grid.get_indices_for_regions()
        inds_set = self.__get_indices_for_rows_and_columns()
        inds_set.extend(inds_box)
        for _ in range(1): # repeat this process in case changes are made
            # apply strategies   
            self.hidden_naked_singles_pairs_triples(inds_set, types=[1, 2])
            
            for inds in inds_box:
                # pointing pairs
                pointers = self.pointing_combos(inds)
                for line, inds_pointer, num in pointers:
                    self.erase(num, line, inds_pointer)
                # box-line reduction
                # keeps = self.box_line_reduction(inds)
                # for inds_keep, nums in keeps:
                #     self.erase(nums, inds, inds_keep)
        self.erase_all_nonconsecutive() # TODO: ????                

        
    def hidden_naked_singles_pairs_triples(self, indices_set, types):
        ''' use hidden/naked singles/pairs/triples to elimininate candidates
         indices_set is a list of the rows, columns, and boxes to perform this strategy on '''
        erased = []
        for inds in indices_set:
            uniques = self.get_unique(inds, types) 
            for inds_combo, combo in uniques:
                self.set_candidates(combo, inds_combo) # passing back the erased here doesn't seem to be very helpful
                erased += self.erase(combo, inds, inds_combo)
        return erased


    #=========== CONSTRAINTS ============

    def find_options(self, r: int, c: int) -> Set:
        ''' for a given cell return the possible digits by excluding digits in the same row, column, and box'''
        nums = set(range(1, self.grid.size + 1))
        set_row = set(self.grid.row(r))
        set_col = set(self.grid.col(c))
        set_box = set(self.get_box(r, c))
        used = set_row | set_col | set_box
        valid = nums.difference(used)
        return valid

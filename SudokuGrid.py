import math
from typing import List, Tuple, Set

# number of regions across x number of regions down
standard_regions = {
    4: (2, 2),
    6: (2, 3),
    9: (3, 3),
    12: (3, 4)
}

class SudokuGrid():
    def __init__(self, string: str = None, size: int = 9) -> List[List[int]]:
        ''' string must be consist of the digits 0-n where n is the number of rows and columns and 0 represents a cell without a given digit
            Optionally, the zero can be replaced with a period "."
            Only square grids are supported, and since only digits are allowed the maximum size grid is 9x9

            Auto detect common regions, in the future support custom defined regions
        '''
        self.candidates= []
        
        if string:
            self.size = int(math.sqrt(len(string)))
            if self.size != math.sqrt(len(string)):
                raise Exception(f'The grid string has {len(string)} characters which does not define a square grid.')
            if len([c for c in string if c != '.' and (c < '0' or c > chr(ord('0')+int(self.size)))]) > 0:
                raise Exception(f'The grid string contains characters other than 0..{self.size} or "."')
        else:
            if size < 3 or size > 9:
                raise Exception('Size parameter must be 3..9')
            self.size = size
            string = '0' * (size*size)

        self.grid_list = self.__unflatten(self.__str2arr(string)) if string else None  
        if self.size in standard_regions:
            self.regions_across = standard_regions[self.size][0]
            self.regions_down = standard_regions[self.size][1]
        else: # until you tell us differently
            self.regions_across = 3
            self.regions_down = 3
        self.box_width = self.size//self.regions_across 
        self.box_height = self.size//self.regions_down 
    
    def with_matrix(self, matrix):
        self.grid_list = matrix
        self.size = len(matrix)
        return self

    def get_region_inds(self, r: int, c: int) -> List[Tuple[int,int]]:
        ''' Currently only supports standard rectangular regions, "boxes" '''
        inds_region = []
        first_row = (r // self.box_height) * self.box_height  
        first_col = (c // self.box_width) * self.box_width  
        for row in range(first_row, first_row + self.box_height):
            for col in range(first_col, first_col + self.box_width):
                inds_region.append((row, col))
        return inds_region

    def get_indices_for_regions(self):
        ''' returns a list of regions and their cell indices '''
        inds_region = []
        for row in range(0, self.size, self.box_height):
            for col in range(0, self.size, self.box_width):
                inds =self.get_region_inds(row, col)
                inds_region.append(inds)
        return inds_region

    # TODO: unused
    def get_nonempty(self, A):
        A = A or self.grid_list
        n = len(A)
        m = len(A[0])
        nonempty = []
        for nm in range(n*m):
            i = nm // n
            j = nm % m
            if A[i][j] != 0:
                nonempty.append(nm)
        return nonempty

    def row(self, r: int) -> List[int]:
        return self.grid_list[r]

    def col(self, c: int) -> List[int]:
        return [row[c] for row in self.grid_list]  

    def print_candidate_grid(self):
        print(str(self))
        for box_row in range(self.regions_down):
            self.print_gridlines('=')
            for cell_row in range(self.box_height):
                if cell_row != 0:
                    self.print_gridlines('-')
                grid_row = box_row*self.box_height + cell_row
                for candidate_row in range(3):
                    for box_col in range(self.regions_across):
                        print("|", end='')
                        for cell_col in range(self.box_width):
                            grid_col = box_col*self.box_width + cell_col                                
                            c = self.candidates[grid_row][grid_col]                                
                            if cell_col != 0:
                                print(":", end='')
                            for candidate_col in range(3):
                                candidate = candidate_row*3+candidate_col+1
                                if candidate in c:
                                    print(str(candidate)+' ', end='')
                                elif candidate_row==1 and candidate_col==1 and self.grid_list[grid_row][grid_col] != 0:
                                    print(str(self.grid_list[grid_row][grid_col])+'*' , end='')
                                else:
                                    print("  ", end='')
                    print("|")
        self.print_gridlines('=')

    def print_gridlines(self,char='-'):
        for _ in range(self.regions_across):
            for _ in range(self.box_width):
                print(f"+{char*6}", end='')
        print("+")

    '''------------------------------- OVERRIDES -------------------------------'''

    def __str__(self):
        string = ''
        for digit in self.__flatten():
            string += str(digit)
        return string

    def __eq__(self, other):
        """ Check if 2 grids are equal or not"""
        n = len(self.grid_list)
        if n != len(other.grid_list):
            return False
        for i in range(n):
            for j in range(n):
                if self.grid_list[i][j] != other.grid_list[i][j]:
                    return False
        return True

    '''------------------------------- PRIVATE -------------------------------'''

    def __flatten(self):
        grid = self.grid_list.copy() # is copy needed?
        arr = []
        for row in grid:
            arr.extend(row)
        return arr

    def __unflatten(self, arr: List[int]=None):
        grid = []
        for i in range(0, len(arr), self.size):
            grid.append(arr[i:i+ self.size])
        return grid

    def __str2arr(self, string):
        arr =[]
        end = string.find('-')
        end = len(string) if end == -1 else end
        for c in string[0:end]:
            if c=='.':
                arr.append(0)
            else:
                arr.append(int(c))
        return arr # [int(c) for c in string]

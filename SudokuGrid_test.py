from SudokuGrid import SudokuGrid
import unittest

class SudokuGridTest(unittest.TestCase):
    def test_valid_4x4_grid(self):
        grid = SudokuGrid('1234432134122143')  
        self.assertEqual(grid.size, 4)      
        self.assertEqual(str(grid),'1234432134122143')     

    def test_valid_9x9_grid_with_zeros(self):
        grid = SudokuGrid('100020400035040900704000001800000000091032080000100097070900600000000000000450000')  
        self.assertEqual(grid.size, 9)        
        self.assertEqual(str(grid),'100020400035040900704000001800000000091032080000100097070900600000000000000450000')     

    def test_valid_9x9_grid_with_dots(self):
        grid = SudokuGrid('1...2.4...35.4.9..7.4.....18.........91.32.8....1...97.7.9..6..............45....')  
        self.assertEqual(grid.size, 9)   
        self.assertEqual(str(grid),'100020400035040900704000001800000000091032080000100097070900600000000000000450000')     

    def test_invalid_length_string(self):
        with self.assertRaises(Exception):
            SudokuGrid('123443213412214300')

    def test_invalid_digits(self):
        with self.assertRaises(Exception):
            SudokuGrid('1234432134122156')

    def test_empty_grid(self):
        grid = SudokuGrid(size=4)
        self.assertEqual(grid.size, 4)      
        self.assertEqual(str(grid),'0000000000000000')     

    def test_invalid_size(self):
        with self.assertRaises(Exception) as cm:
            SudokuGrid(size=10)
        self.assertEqual(str(cm.exception), 'Size parameter must be 3..9')

    def test_get_region_inds_with_9x9(self):
        grid = SudokuGrid(size=9)
        self.assertEqual(grid.get_region_inds(0,0),[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])
        self.assertEqual(grid.get_region_inds(2,2),[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])
        self.assertEqual(grid.get_region_inds(6,6),[(6, 6), (6, 7), (6, 8), (7, 6), (7, 7), (7, 8), (8, 6), (8, 7), (8, 8)])
        self.assertEqual(grid.get_region_inds(8,8),[(6, 6), (6, 7), (6, 8), (7, 6), (7, 7), (7, 8), (8, 6), (8, 7), (8, 8)])

    def test_get_region_inds_with_6x6(self):
        grid = SudokuGrid(size=6)
        self.assertEqual(grid.get_region_inds(0,0),[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)])
        self.assertEqual(grid.get_region_inds(1,2),[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)])
        self.assertEqual(grid.get_region_inds(4,3),[(4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)])
        self.assertEqual(grid.get_region_inds(5,5),[(4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)])

    def test_get_indices_for_9x9_regions(self):
        grid = SudokuGrid(size=9)
        regions = grid.get_indices_for_regions()
        self.assertEqual(len(regions),9)
        self.assertEqual(regions[4],[(3, 3), (3, 4), (3, 5), (4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)])
 
    def test_get_indices_for_6x6_regions(self):
        grid = SudokuGrid(size=6)
        regions = grid.get_indices_for_regions()
        self.assertEqual(len(regions),6)
        self.assertEqual(regions[0],[(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)])
        self.assertEqual(regions[5],[(4, 3), (4, 4), (4, 5), (5, 3), (5, 4), (5, 5)])
 
    def test_grid_list_for_6x6(self):
        grid = SudokuGrid(size=6)
        self.assertEqual(len(grid.grid_list),6)
        self.assertEqual(len(grid.grid_list[0]),6)

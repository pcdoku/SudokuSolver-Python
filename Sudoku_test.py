""""

31 May 2020

Sudoku Solver

"""
from Sudoku import Sudoku
from SudokuGrid import SudokuGrid
from SudokuSolver import SudokuSolver
import unittest

class SudokuTest(unittest.TestCase):
    #def setup(self):
    def candidates_equal(self, A, B): # B is a list
        """ Check if 2 grids are equal or not"""
        n = len(A)
        if n != len(B):
            return False
        for i in range(n):
            for j in range(n):
                if A[i][j] != B[i][j]:
                    return False
        return True

    def test_find_options(self):
        grid = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        s = Sudoku(SudokuGrid().with_matrix(grid))
        self.assertEqual(s.find_options(0, 2), {1, 2, 4})
        self.assertEqual(s.find_options(4, 4), {5})
        self.assertEqual(s.find_options(5, 1), {1, 5})
        self.assertEqual(s.find_options(8, 6), {1, 3, 4, 6})


    def test_candidates(self):
        grid = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        candidates = [
            [set(), set(), {1, 2, 4}, {2, 6}, set(), {8, 2, 4, 6}, {8, 1, 4, 9}, {1, 2, 4, 9}, {8, 2, 4}],
            [set(), {2, 4, 7}, {2, 4, 7}, set(), set(), set(), {8, 3, 4, 7}, {2, 3, 4}, {8, 2, 4, 7}],
            [{1, 2}, set(), set(), {2, 3}, {3, 4}, {2, 4}, {1, 3, 4, 5, 7}, set(), {2, 4, 7}],
            [set(), {1, 2, 5}, {1, 2, 5, 9}, {9, 5, 7}, set(), {1, 4, 7}, {9, 4, 5, 7}, {9, 2, 4, 5}, set()],
            [set(), {2, 5}, {9, 2, 5, 6}, set(), {5}, set(), {9, 5, 7}, {9, 2, 5}, set()],
            [set(), {1, 5}, {1, 3, 5, 9}, {9, 5}, set(), {1, 4}, {8, 9, 4, 5}, {9, 4, 5}, set()],
            [{1, 3, 9}, set(), {1, 3, 4, 5, 7, 9}, {3, 5, 7}, {3, 5}, {7}, set(), set(), {4}],
            [{2, 3}, {8, 2, 7}, {2, 3, 7}, set(), set(), set(), {3, 6}, {3}, set()],
            [{1, 2, 3}, {1, 2, 4, 5}, {1, 2, 3, 4, 5}, {2, 3, 5, 6}, set(), {2, 6}, {1, 3, 4, 6}, set(), set()]
        ]
        s = Sudoku(SudokuGrid().with_matrix(grid))
        self.assertTrue(self.candidates_equal(s.grid.candidates, candidates))
        # test uniques
        inds = [(0, j) for j in range(9)] # no unique candidates
        #self.assertEqual(s.get_unique(inds), [])
        self.assertEqual(s.get_unique(inds, type=[1]), [] )
        inds = [(7, j) for j in range(9)] # uniques: 8 at (7, 1)  and 6 at (7, 6)
        #self.assertEqual(s.get_unique(inds), [([(7, 6)], [6]), ([(7, 1)], [8])] ) #[(6, (7, 6)), (8, (7, 1))])
        self.assertEqual(s.get_unique(inds, type=[1]), [([(7, 6)], [6]), ([(7, 1)], [8])] )
        inds = s.grid.get_region_inds(5, 6)  # middle right box. unique 8 at (5,6)
        #self.assertEqual(s.get_unique(inds), [([(5, 6)], [8])])
        self.assertEqual(s.get_unique(inds, type=[1]), [([(5, 6)], [8])] )
        # test erase function
        s.place_and_erase(0, 2, 1, constraint_prop=False) 
        self.assertEqual(s.grid.candidates[0], [set(), set(), set(), {2, 6}, set(), {8, 2, 4, 6}, {8, 4, 9}, {2, 4, 9}, {8, 2, 4}])
        col = [s.grid.candidates[i][2] for i in range(9)]
        self.assertEqual(col, [set(), {2, 4, 7}, set(), {2, 5 ,9}, {2, 5, 6, 9}, {3, 5, 9}, {3, 4, 5, 7, 9}, {2, 3, 7}, {2, 3, 4, 5}])


    def test_candidates_advanced(self):
        grid = [
            [0, 8, 0, 0, 0, 1, 2, 0, 6],
            [0, 0, 0, 0, 2, 0, 0, 0, 0],
            [0, 2, 0, 3, 0, 5, 0, 4, 0],
            [0, 6, 0, 0, 1, 0, 9, 0, 0],
            [0, 0, 2, 0, 5, 0, 4, 0, 0],
            [0, 0, 8, 0, 0, 0, 0, 1, 0],
            [0, 3, 0, 7, 0, 4, 0, 5, 0],
            [0, 0, 0, 0, 3, 0, 0, 0, 0],
            [4, 0, 6, 1, 0, 0, 0, 8, 0]
        ] # June 7 Extreme 'https://www.sudokuwiki.org
        s = Sudoku(SudokuGrid().with_matrix(grid))
        candidates = [
            [{9, 3, 5, 7}, set(), {3, 4, 5, 7, 9}, {9, 4}, {9, 4, 7}, set(), set(), {9, 3, 7}, set()],
            [{1, 3, 5, 6, 7, 9}, {1, 4, 5, 7, 9}, {1, 3, 4, 5, 7, 9}, {8, 9, 4, 6}, set(), {8, 9, 6, 7}, {1, 3, 5, 7, 8}, {9, 3, 7}, {1, 3, 5, 7, 8, 9}],
            [{1, 9, 6, 7}, set(), {1, 9, 7}, set(), {8, 9, 6, 7}, set(), {8, 1, 7}, set(), {8, 1, 9, 7}],
            [{3, 5, 7}, set(), {3, 4, 5, 7}, {8, 2, 4}, set(), {8, 2, 3, 7}, set(), {2, 3, 7}, {2, 3, 5, 7, 8}],
            [{1, 3, 9, 7}, {1, 9, 7}, set(), {8, 9, 6}, set(), {3, 6, 7, 8, 9}, set(), {3, 6, 7}, {8, 3, 7}],
            [{9, 3, 5, 7}, {9, 4, 5, 7}, set(), {9, 2, 4, 6}, {9, 4, 6, 7}, {2, 3, 6, 7, 9}, {3, 5, 6, 7}, set(), {2, 3, 5, 7}],
            [{8, 1, 2, 9}, set(), {1, 9}, set(), {8, 9, 6}, set(), {1, 6}, set(), {1, 2, 9}],
            [{1, 2, 5, 7, 8, 9}, {1, 5, 9, 7}, {1, 5, 9, 7}, {2, 5, 6, 8, 9}, set(), {8, 9, 2, 6}, {1, 6, 7}, {9, 2, 6, 7}, {1, 2, 4, 7, 9}],
            [set(), {9, 5, 7}, set(), set(), {9}, {9, 2}, {3, 7}, set(), {9, 2, 3, 7}]
        ]
        self.assertTrue(self.candidates_equal(s.grid.candidates, candidates))
        inds = [(i, 0) for i in range(9)]
        #self.assertEqual(s.get_pairs(inds), [([(6, 0), (7, 0)], (2, 8))])
        uniques = s.get_unique(inds, type=[2])[0]
        uniques[0].sort()
        self.assertEqual(uniques, ([(6, 0), (7, 0)], (2, 8)) )
        grid = [
            [0, 0, 0, 0, 0, 1, 0, 3, 0],
            [2, 3, 1, 0, 9, 0, 0, 0, 0],
            [0, 6, 5, 0, 0, 3, 1, 0, 0],
            [6, 7, 8, 9, 2, 4, 3, 0, 0],
            [1, 0, 3, 0, 5, 0, 0, 0, 6],
            [0, 0, 0, 1, 3, 6, 7, 0, 0],
            [0, 0, 9, 3, 6, 0, 5, 7, 0],
            [0, 0, 6, 0, 1, 9, 8, 4, 3],
            [3, 0, 0, 0, 0, 0, 0, 0, 0]
        ] # https://www.sudokuwiki.org/Hidden_Candidates#HP
        s = Sudoku(SudokuGrid().with_matrix(grid))
        inds = [(0, j) for j in range(9)]
        uniques = s.get_unique(inds, type=[3])[0]
        uniques[0].sort()
        self.assertEqual(uniques, ([(0, 3), (0, 6), (0, 8)], (2, 5, 6)) )
        s.grid.candidates[0][8] = {2, 5}
        inds = [(i, 8) for i in range(9)]
        uniques = s.get_unique(inds, type=[3])[0]
        uniques[0].sort()
        self.assertEqual(uniques, ([(1, 8), (2, 8), (5, 8)], (4, 8, 7)) )    
       
    
    def test_impossible(self):
        # impossible
        puzzles = [
            '.....5.8....6.1.43..........1.5........1.6...3.......553.....61........4.........',  
            '12.......34...............5...........5..........................................',  
            '11.......34...............5...........5..........................................',
        ]
        for puzzle in puzzles:
            puzzle = SudokuGrid(puzzle)
            s = Sudoku(puzzle)
            s.flush_candidates()
            self.assertFalse(s.check_possible()[0])
        # possible
        puzzles = [
            '280070309600104007745080006064830100102009800000201930006050701508090020070402050',  
            '000010030009005008804006025000000600008004000120087000300900200065008000900000000',  
            '1.....................................5..........................................',
        ]
        for puzzle in [puzzles[1]]:
            puzzle = SudokuGrid(puzzle)
            s = Sudoku(puzzle)
            s.flush_candidates()
            self.assertTrue(s.check_possible()[0])


    # def check_solver(self):
    #     # first try a tiny dummy grid. Solution is not unique
    #     s = Sudoku()
    #     grid = [[0, 1, 0],
    #             [2, 3, 9],
    #             [0, 8, 5]]
    #     sol = [[4, 1, 6],
    #            [2, 3, 9],
    #            [7, 8, 5]]
    #     grid_sol, _ = solveSudoku(grid, num_boxes=1)
    #     #try the partial version of the NY grid
    #     mySol, _ = solveSudoku(easy_par)
    #     self.assertTrue(grid_equal(easy_sol, mySol))
    def test_solver_1(self):
        self.assert_solveable(
            '280070309600104007745080006064830100102009800000201930006050701508090020070402050',
            '281576349693124587745983216964835172132749865857261934426358791518697423379412658'
            )

    def test_solver_2(self):
        self.assert_solveable(
            '910780200027001894684000300000846001740059080009000050106093008000500706002070130',
            '913784265527361894684925317235846971741259683869137452176493528398512746452678139'
            )

    def test_solver_3(self):
        self.assert_solveable(
            # from https://dev.to/aspittel/how-i-finally-wrote-a-sudoku-solver-177g, very easy puzzle
            '530070000600195000098000060800060003400803001700020006060000280000419005000080079',
            '534678912672195348198342567859761423426853791713924856961537284287419635345286179'
            )            

    def test_solver_4(self):
        self.assert_solveable(
            # medium to hard Sudoku (some backtracking). From New York Times, 31 May 2020 - 2 June 2020
            '100020400035040900704000001800000000091032080000100097070900600000000000000450000',
            '189327465235641978764895321827569143491732586653184297372918654546273819918456732'
            )            

    def test_solver_5(self):
        self.assert_solveable(
            # medium to hard Sudoku (some backtracking). From New York Times, 31 May 2020 - 2 June 2020
            '000832067000600200800700010010020000509004700000008000007000940000005000402000500',
            '195832467743651298826749315318927654569314782274568139657283941931475826482196573'
            )            

    def test_solver_6(self):
        self.assert_solveable(
            # medium to hard Sudoku (some backtracking). From New York Times, 31 May 2020 - 2 June 2020
            '000010030009005008804006025000000600008004000120087000300900200065008000900000000',
            '752819436639245718814736925473592681598164372126387549387951264265478193941623857'
            )    

    def test_solver_7(self):
        self.assert_solveable(
            #https://www.nytimes.com/puzzles/sudoku/
            '106000050070030004090005200002060007000108000047020000000000803003200006000000002',
            '186742359275839164394615278812564937639178425547923681721456893953281746468397512'
            ) 

    def test_solver_8(self):
        self.assert_solveable(
            #https://theconversation.com/good-at-sudoku-heres-some-youll-never-complete-5234
            # 17 clue puzzle: minimum number of clues for a unique solution to be possible
            '000700000100000000000430200000000006000509000000000418000081000002000050040000300',
            '264715839137892645598436271423178596816549723759623418375281964982364157641957382'
            ) 

    def test_solver_9(self):
        self.assert_solveable(
            # have to make at least 3 guesses
            '800000000003600000070090200050007000000045700000100030001000068008500010090000400',
            '812753649943682175675491283154237896369845721287169534521974368438526917796318452'
            ) 

    def assert_expected_solver_output(self, puzzle, expected_done, solution_count, solution=None, constraints=None):
        puzzle_grid = SudokuGrid(puzzle)
        my_solution, done, info = SudokuSolver().solveSudoku(puzzle_grid, verbose=False, constraints=constraints)
        #self.assertEqual(info,"")
        self.assertEqual(done, expected_done)
        self.assertEqual(info['solutions'], solution_count)
        if solution:
            self.assertTrue(SudokuGrid(solution) == my_solution, msg=f'solution does not match. Actual: {my_solution}')

    def assert_solveable(self, puzzle, solution):
        self.assert_expected_solver_output(puzzle, True, 1, solution)

    def test_solver_unsolvable_1(self):
        self.assert_expected_solver_output(
            '999200000065074800070006900004000000050008704000030000000000600080000057006007089', False, 0
            ) 

    def test_non_consecutive_constraint(self):
        self.assert_expected_solver_output(
            # https://www.wired.com/2011/06/dr-sudoku-prescribes-nonconsecutive-sudoku/
            '000000400000000060000460000000000006060000040004000000000604000600000000040000000', True, 1,
            '726138495483795162159462738837249516261573849594816273372684951615927384948351627',
            ["classic","nonconsecutive"]
        )

    def test_solver_with_too_few_clues_returns_first_solution(self):
        self.assert_expected_solver_output(
            #https://theconversation.com/good-at-sudoku-heres-some-youll-never-complete-5234
            # 76215 solutions
            '000000000100000000000430200000000006000509000000000418000081000002000050040000300', True, 1
            ) 

    def test_solver_multiple_solutions_returns_first_solution(self):
        self.assert_expected_solver_output(
            # multiple solutions
            '080001206000020000020005040060010900002050400008000010030704050000000000406100080', True, 1
        )

    def test_solver_diabolical(self):
        self.assert_expected_solver_output(
            # May 24 Extreme -> requires multiple diabolical+extreme strategies 
            '003100720700000500050240030000720000006000800000014000060095080005000009049002600', True, 1,
            '693158724724963518851247936538726491416539872972814365267495183385671249149382657'
        )

    @unittest.skip("takes a long time to solve")
    def test_solver_worlds_hardest_puzzle(self):
        self.assert_expected_solver_output(
            # https://www.conceptispuzzles.com/index.aspx?uri=info/article/424
            '800000000003600000070090200050007000000045700000100030001000068008500010090000400', True, 1,
            '812753649943682175675491283154237896369845721287169534521974368438526917796318452'
        ) 

    def test_solver_ctc(self):
        self.assert_expected_solver_output(
            # https://cracking-the-cryptic.web.app/sudoku/PMhgbbQRRb
            '029000400000500100040000000000042000600000070500000000700300005010090000000000060', True, 1,
            '329816457867534192145279638931742586684153279572968314796321845418695723253487961'
        )


    def test_solve_6_x_6_sudoku(self):
        self.assert_expected_solver_output(
            '024310036200000600652430260103400500', True, 1,
            '524316136254341625652431265143413562'
        )

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    tests = unittest.TestLoader().discover('.', pattern='*test.py')
    runner.run(tests)
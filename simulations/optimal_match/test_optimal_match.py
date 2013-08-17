import unittest2 
import optimal_match 
import tempfile 
import numpy as np 

TOL = 0.00001

def same_vector(v1, v2): 
    r = []
    for x, y in zip(v1, v2): 
        r.append(abs(x - y) < TOL)
    return all(r)


class TestOptimalMatch(unittest2.TestCase): 
   

    def test(self): 
        self.assertEqual(1,1)

    def test_m_zero_b(self): 
        self.assertEqual(abs(optimal_match.m(0.0,0.0)) < TOL, True)
        
    def test_mm_qrange(self): 
        Q = [i/10.0 for i in range(0,10)]
        self.assertEqual(all([abs(optimal_match.mm(0,q) - q) < TOL for q in Q]), True)

    def test_numpy(self):
        a = np.array([[3,1], [1,2]])
        b = np.array([9,8])
        sol = np.linalg.solve(a, b)
        self.assertEquals(same_vector(sol, np.array([2.0,3.0])), True)

    def test_row_gen_two(self): 
         result = [-1.0, 1.0, 0.0]
         self.assertEquals(same_vector(optimal_match.create_row([1.0, 1.0],1,2), result), True)

    def test_row_gen_2_4(self): 
         result = [0.0, -1.0, 1.0, 0.0, 0.0]
         self.assertEquals(same_vector(optimal_match.create_row([1.0]*5,2,4), result), True)
         
    def test_last_row(self):
        result = [1]*10
        self.assertEquals(same_vector(optimal_match.create_row([1.0]*5,4,4), result), True)
    
    def test_create_matrix(self):
        'Not implemented yet'
        self.assertEqual(True, True)

    def test_create_column(self):
        result = np.array([0.0,1.0])
        test_case = optimal_match.create_column([1]*2, 2, 1.0)
        self.assertEqual(same_vector(test_case, result), True)  
     
    def test_solver(self):
        'Not implemented yet.' 
        Q = [1.0 - i/100.0 for i in range(0,10)]
        sol = optimal_match.solve_linear(Q, 3)
        self.assertEqual(True, True)

    def test_find_goat(self): 
        'Not implemented yet.' 
        Q = [1.0 - i/500.0 for i in range(0,500)]
        g = optimal_match.find_goat(Q, 3)
        self.assertEqual(True, True)
      

if __name__ == '__main__':
    unittest2.main()

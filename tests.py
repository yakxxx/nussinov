import unittest
from pprint import pprint
from nussinov import Nussinov


class NussinovTest(unittest.TestCase):
    
    def setUp(self):
        self.basic_data = 'ACGU'
        self.basic = Nussinov(self.basic_data)
    
    def test_compute_return(self):
        ret = self.basic.compute()
        self.assertIsInstance(ret, list)
        
    def test_init_matrix(self):
        self.basic._init_matrix()
        self.assertEqual(len(self.basic.matrix), len(self.basic_data))
        
        for i in xrange(len(self.basic_data)):
            for j in xrange(len(self.basic_data)):
                self.assertEqual(self.basic.matrix[i][j],0)
                
    def test_fill_diagonal(self):
        self.basic._fill_diagonal(1)
        self.assertEqual(self.basic.matrix[1][2], 1)
        self.basic._fill_diagonal(2)
        self.basic._fill_diagonal(3)
        self.assertEqual(self.basic.matrix[0][3], 2)
        
    def test_build_matrix(self):
        self.basic.build_matrix()
        self.assertEqual(self.basic.matrix[0][3], 2)
        self.assertEqual(self.basic.matrix[1][2], 1)
       
        
if __name__ == "__main__":
    unittest.main()
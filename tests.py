import unittest
from pprint import pprint
from nussinov import Nussinov
from file_reader import FileReader, WrongData


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
                if i-1 <= j:
                    self.assertEqual(self.basic.matrix[i][j], 0)
                else:
                    self.assertEqual(self.basic.matrix[i][j], -1)
                
    def test_fill_diagonal(self):
        self.basic._fill_diagonal(1)
        self.assertEqual(self.basic.matrix[1][2], 1)
        self.basic._fill_diagonal(2)
        self.basic._fill_diagonal(3)
        self.assertEqual(self.basic.matrix[0][3], 2)
        
    def test_build_matrix(self):
        self.basic._build_matrix()
        self.assertEqual(self.basic.matrix[0][3], 2)
        self.assertEqual(self.basic.matrix[1][2], 1)
       
    def test_generate_trace(self):
        self.basic._build_matrix()
        self.basic._generate_trace()
        
        
    def test_acceptance_01(self):
        nus = Nussinov('GGGAAAUCC')
        ret = nus.compute()
        self.assertEqual(len(ret), 3)
        self.assertIn(ret, ([(1,8), (2,7), (3,6)],
                            [(1,8), (2,7), (4,6)],
                            [(1,8), (2,7), (5,6)])
                      )
        
    def test_acceptance_02(self):
        nus = Nussinov('GGAAACCGAAAC')
        ret = nus.compute()
        self.assertEqual(len(ret), 3)
        self.assertIn(ret,([(0,6), (1,5), (7,11)],
                          [(0,11), (1,5), (6,7)])
                      )
        
    def test_acceptance_03(self):
        nus = Nussinov('GCGCGCGCGCGCGCGCGCGCGCGC')
        ret = nus.compute()
        self.assertEqual(len(ret), 12)
        
        
class FileReaderTest(unittest.TestCase):
    def setUp(self):
        self.fr = FileReader('test_data') 
           
    def test__check_line(self):
        self.assertRaises(WrongData, self.fr._check_line, 'AUAGCx')
        self.assertRaises(WrongData, self.fr._check_line, 'aUGCA')
        self.assertRaises(WrongData, self.fr._check_line, 'A')
        try:
            self.fr._check_line('ACGCGCGCGCGCGAAAUUUU')
        except:
            self.fail()
            
    def test_get_one_line(self):
        l = self.fr.get_one_line()
        self.assertEqual(l, 'GCGCGCGC')
    
    def test_iteration(self):
        count = 0
        for x in self.fr:
            count += 1
        self.assertEqual(count, 3)
        
        
if __name__ == "__main__":
    unittest.main()
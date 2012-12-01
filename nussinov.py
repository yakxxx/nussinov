
class Nussinov(object):
    def __init__(self, data):
        self.data = data
        self.data_len = len(data)
        self._init_matrix()
        self.trace = []
    
    def compute(self):
        self._build_matrix()
        self._generate_trace()
        return self.trace
    
    def _build_matrix(self):
        self._init_matrix()
        for d in xrange(1, self.data_len):
            self._fill_diagonal(d)
            
    def _init_matrix(self):
        data_len = len(self.data)
        
        self.matrix = [[ 0 if i-1 <= j else -1 for j in xrange(data_len)]
                            for i in xrange(data_len)]
        
    def _fill_diagonal(self, d):
        ''' @param d: index of OX axis where diagonal starts 
            This function assumes that previous diagonals are already computed, 
            so use it only in loops.
        '''
        i = 0
        for j in xrange(d, self.data_len):
            v = self.matrix[i+1][j-1] + int(self.is_base_pair(i,j))
            v = max(v, self.matrix[i+1][j])
            v = max(v, self.matrix[i][j-1])
            v = max([v] + [self.matrix[i][k] + self.matrix[k+1][j] for k in xrange(i+1,j)] )
            self.matrix[i][j] = v
            i += 1

    def is_base_pair(self, i, j):
        return self.data[i] + self.data[j] in ('AU','UA','GC','CG')
    
    def _generate_trace(self):
        return self._trace_req(0, self.data_len - 1)
        
    def _trace_req(self, i, j):
        if self.matrix[i][j] == -1 or i>=j:
            return
        if self.matrix[i][j] == self.matrix[i+1][j]:
            self._trace_req(i+1, j)
        elif self.matrix[i][j] == self.matrix[i][j-1]:
            self._trace_req(i, j-1)
        elif self.matrix[i][j] == self.matrix[i+1][j-1] + int(self.is_base_pair(i,j)):
            self.trace.append((i, j))
            self._trace_req(i+1, j-1)
        else:
            val, k = max([ (self.matrix[i][k] + self.matrix[k+1][j], k) \
                                for k in xrange(i+1,j) ])
            assert(self.matrix[i][j] == val)
            self._trace_req(i, k)
            self._trace_req(k+1, j)
            
            
            
            
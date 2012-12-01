class FileReader(object):
    
    def __init__(self, path):
        self.path = path
        self.file = open(path)
    
    def next(self):
        return self.get_one_line()
    
    def __iter__(self):
        return self
    
    def get_one_line(self):
        try:
            line = self.file.next()
            if line[-1] == '\n':
                line = line[0:-1]
        except StopIteration:
            self.file.close()
            raise
        
        self._check_line(line)
        return line
        
    def _check_line(self, line):
        if(len(line) < 2):
            raise WrongData('Input string to short')
        
        for i,x in enumerate(line):
            if x not in 'GCAU':
                raise WrongData('wrong symbol %s at position %d' % (x, i))
        
        
class WrongData(Exception):
    pass
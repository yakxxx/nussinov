#!/usr/bin/python

from file_reader import *
from nussinov import Nussinov


if __name__ == "__main__":
    input_path = 'test_data'
    output_path = 'out'
    out = open(output_path, 'w')
    
    reader = FileReader(input_path)
    
    for line in reader:
        nuss = Nussinov(line)
        ret = nuss.compute()
        out.write("%s %s\n" % (len(ret), ret))
    out.close()
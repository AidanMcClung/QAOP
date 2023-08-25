def hello(name):
    print("hello",name)
    
def testPringConfig():
    #import io
    with open('config.txt') as config_file:
        print(config_file.readline())
        print(config_file.readline())
        
def testFindSelf():
    import os
    #print(os.path.abspath(self.__file__))
    print(os.getcwd())
    
def makePracticeImage():
    import numpy as np
    practice_image = np.full((25,25),300)
    practice_image[10:15,10:15] = 1000
    practice_image[11:14,11:14] = 5000
    practice_image[12:13,12:13] = 15000
    return practice_image
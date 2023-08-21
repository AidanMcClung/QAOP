def hello(name):
    print("hello",name)
    
def testPringConfig():
    #import io
    with open('config.txt') as config_file:
        print(config_file.readline())
        print(config_file.readline())
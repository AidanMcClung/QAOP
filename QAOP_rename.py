import os

class renamer():
    
    def __init__(self,path = None):
        if path is not None:
            self.basepath = path
        
        
        
    def navigatePath(self):
        #First we need to figure out where we are and where the files we want are.
        self.basepath = ""
        print("First we must establish the path to where we want to go. The following are the current path options")
        print(os.listdir(self.basepath))
        choice = input("Please select an option to navigate to")
        try:
            options = os.listdir(self.basepath+'/'+choice)
            if options:
                self.basepath = self.basepath+'/'+choice
        except:
            print('error')


class newSub:
    def __init__(self,name="", id=0, date_sub="", type=""):
        self.name = name
        self.ids = id
        self.date_sub = date_sub
        self.type = type
        with open("your_file.txt","a") as first:
            first.write(self.name,self.ids,self.date_sub,self.type)


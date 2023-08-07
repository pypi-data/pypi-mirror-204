import math
class point:
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y
    def show(self):
        return self.x
        return self.y
    def __add__(self,p):
        return(self.x+p.x,self.y+p.y)
    def __sub__(self,p):
        return(self.x-p.x,self.y-p.y)
    def __mult__(self,p):
        return(self.x * p.x,self.y * p.y)
    def __eq__(self,p):
         return(self.x==p.x,self.y==p.y)
    def __repro__():
        return "point(self.x,self.y)"
    def distance(p1,p2):
        return math.hypot(p2.x-p1.x,p2.y-p1.y)
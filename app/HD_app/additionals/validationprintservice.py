import os

# Validacja print --------------------------------------------
class ValidationPrintService():
    def __init__(self,cla,typ="CBV"):
        self.typ = typ
        self.left = 20
        self.right = 40
        self.center = self.right+self.left
        self.cla = cla
        self.red = '\033[91m'
        self.pink= '\033[45m'
        self.green= '\033[42m'
        self.green_text = '\033[32m'
        self.yellow = '\033[43m'
        self.yellow_text = '\033[33m'
        self.turq = '\033[46m'
        self.blue = '\033[44m'
        self.end = '\033[0m'
        self.initial_print()
    def initial_print(self):
        print(" ")
        if self.typ == "SIGNAL":
            print(self.turq+self.cla.center(self.center," ")+self.end)
        if self.typ == "CBV":    
            print(self.pink+self.cla.center(self.center," ")+self.end)
        print("~".center(self.center,"~"))
    def signal_print(self):
        print(" ")
        print(self.turq+self.cla.center(self.center," ")+self.end)
        print("~".center(self.center,"~"))
    def print_green(self,msg,state):
        self.msg = str(msg)
        self.state = str(state)
        print(self.msg.ljust(self.left,".")+self.green_text+self.state.rjust(self.right,".")+self.end)
    def print_turq(self,msg,state):
        self.msg = str(msg)
        self.state = str(state)
        print(self.msg.ljust(self.left,".")+self.turq+self.state.rjust(self.right,".")+self.end)
    def print_red(self,msg,state):
        self.msg = str(msg)
        self.state = str(state)
        print(self.msg.ljust(self.left,".")+self.red+self.state.rjust(self.right,".")+self.end)
    def print_blue(self,msg,state):
        self.msg = str(msg)
        self.state = str(state)
        print(self.msg.ljust(self.left,".")+self.blue+self.state.rjust(self.right,".")+self.end)
    def print_get(self):
        print("Method ".ljust(self.left,".")+"GET".rjust(self.right,"."))
    def print_created(self):
        print("Created? ".ljust(self.left,".")+"YES".rjust(self.right,"."))
    def print_post(self):
        print("Method ".ljust(self.left,".")+"POST".rjust(self.right,"."))
    def set_request(self,request):
        self.request = request
        print("Requesting ".ljust(self.left,".")+str(self.request.user).rjust(self.right,"."))
    def set_signal_kwargs(self,**kwargs):
        self.instance = kwargs['i']
        self.created = kwargs['c']
        self.sender = kwargs['s']
        print("Instancja ".ljust(self.left,".")+str(self.instance).rjust(self.right,"."))
        print("Created? ".ljust(self.left,".")+str(self.created).rjust(self.right,"."))
        print("Sender model ".ljust(self.left,".")+str(self.sender.__name__).rjust(self.right,"."))

import socket

if __name__ =="__main__":

class jausmessage:
    unsigned short
    def __init__(self):
    #Default constructor for the message
    self

class QueneEmptyExc():
  "Quene is Empty Exception"
  pass
class receiveStack:
  "The Class for the receiving stack"
  def __init__(self, socket_obj):
    self.msgstack =[]
    is(socket_obj
    self.socket=socket_obj
  def pullMessage(self):
    return self.msgstack.pop(0);
  def pushMessage(self, msg):
    self.msgstack.append(msg);
    return true
  def update(self):
    self.socket.read

class transmitStack:
  "The Class for the transmiting stack"
  def __init__(self):
    self.msgstack =[]
  def pushMessage(self, msg):
    self.msgstack
    return true
  def sendMessage(self, num=1):
    return true

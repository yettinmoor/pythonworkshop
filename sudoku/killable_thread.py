
# Python program using 
# traces to kill threads 
# https://www.geeksforgeeks.org/python-different-ways-to-kill-a-thread/
  
import sys 
import trace 
import threading 
import time 


class thread_with_trace(threading.Thread): 
  def __init__(self, *args, **keywords): 
    threading.Thread.__init__(self, *args, **keywords) 
    self.killed = False
  
  def start(self): 
    self.__run_backup = self.run 
    self.run = self.__run       
    threading.Thread.start(self) 

  def run(self):
    if self._target is not None:
      self._return = self._target(*self._args, **self._kwargs)
  
  def __run(self): 
    sys.settrace(self.globaltrace) 
    self.__run_backup() 
    self.run = self.__run_backup 
  
  def globaltrace(self, frame, event, arg): 
    if event == 'call': 
      return self.localtrace 
    else: 
      return None
  
  def localtrace(self, frame, event, arg): 
    if self.killed: 
      if event == 'line': 
        raise SystemExit() 
    return self.localtrace 
  
  def kill(self): 
    self.killed = True
  
  def get_return(self):
    if self._return:
      return self._return

class InsuffiiantAmount(Exception):
    def __init__(self, arg):
      self.message = arg
      
      
class MaxAmount(Exception):
     def __init__(self, arg):
      self.message = arg
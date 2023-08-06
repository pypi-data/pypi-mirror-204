import os

from ..provider import Provider
from ....path import bids

DEFAULT_NAME = "00OUTPUTS"
DEFAULT_DIR = os.getenv("PYSOLVE_OUTPUTS", DEFAULT_NAME)

def path(bid, sid, limit, problem):
   return os.path.join(
      DEFAULT_DIR, 
      bids.name(bid,limit),
      sid,
      problem).rstrip("/")

class Outputs(Provider):
   
   def register(self, solver):
      solver.providers.append(self)
      self.solver = solver
   
   def path(self, instance, strategy):
      (bid, problem) = instance
      return path(bid, strategy, self.solver.limits.spec, problem) + ".out"
   
   def query(self, instance, strategy):
      f = self.path(instance, strategy)
      #print("QUERY", instance, strategy, f)
      if not os.path.isfile(f):
         return None
      output = open(f).read()
      result = self.solver.process(output)
      self.solver.update(instance, strategy, output, result, store=False)
      return result

   def store(self, instance, strategy, output, result):
      #print("STORE", instance, strategy, result)
      f = self.path(instance, strategy)
      os.makedirs(os.path.dirname(f), exist_ok=True)
      open(f,"w").write(output)


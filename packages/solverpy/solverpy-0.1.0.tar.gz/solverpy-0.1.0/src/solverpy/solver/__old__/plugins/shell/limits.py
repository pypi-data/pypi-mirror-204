from ..updater import Updater

def make(fun, arg):
   return fun % arg if isinstance(fun, str) else fun(arg)

class Limits(Updater):

   def __init__(self, spec, limits):
      lims = {x[0]:x[1:] for x in spec.split("-") if x}
      self.timeout = int(lims["T"]) if "T" in lims else None
      try:
         lims = [make(limits[x],y) for (x,y) in lims.items() if limits[x]]
      except:
         raise Exception(f"pysolve: Invalid limit string: {spec}")
      self.args = " ".join(lims)
      self.spec = spec
   
   def register(self, solver):
      super().register(solver)
      solver.limits = self

   def shell(self, cmd):
      return f"{cmd} {self.args}" if self.args else cmd

   def update(self, instance, strategy, output, result):
      if self.timeout:
         result["timeout"] = self.timeout


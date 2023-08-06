from .shellsolver import ShellSolver
from .plugins.status.smt import Smt
from .plugins.shell.time import Time

SMT_OK = frozenset([
   'sat', 
   'unsat',
])

SMT_FAILED = frozenset([
   'unknown', 
   'timeout',
])

SMT_ALL = SMT_OK | SMT_FAILED

class SmtSolver(ShellSolver):

   def __init__(self, cmd, plugins=[], wait=None):
      plugins = plugins + [ Time(), Smt() ] 
      ShellSolver.__init__(self, cmd, plugins, wait)

   def valid(self, result):
      return super().valid(result) and result["STATUS"] in SMT_ALL

   def status(self, result):
      return self.valid(result) and result["STATUS"] in SMT_OK


from .shellsolver import ShellSolver
from .plugins.status.tptp import Tptp
from .plugins.shell.time import Time

TPTP_OK = frozenset([
   'Satisfiable', 
   'Unsatisfiable', 
   'Theorem', 
   'CounterSatisfiable', 
   'ContradictoryAxioms',
])

TPTP_FAILED = frozenset([
   'ResourceOut', 
   'GaveUp',
   'Timeout',
])

TPTP_ALL = TPTP_OK | TPTP_FAILED

INCOMPLETE_OK = frozenset([
   'Unsatisfiable', 
   'Theorem',
   'ContradictoryAxioms',
])

INCOMPLETE_FAILED = frozenset([
   'ResourceOut', 
   'GaveUp', 
   'Timeout',
   'Satisfiable', 
   'CounterSatisfiable', 
])

class TptpSolver(ShellSolver):

   def __init__(self, cmd, plugins=[], complete=True, wait=None):
      plugins = plugins + [ Time(), Tptp() ] 
      ShellSolver.__init__(self, cmd, plugins, wait)
      self.complete = complete

   def ok(self):
      return (TPTP_OK if self.complete else INCOMPLETE_OK)

   def failed(self):
      return (TPTP_FAILED if self.complete else INCOMPLETE_FAILED)

   def valid(self, result):
      return super().valid(result) and result["STATUS"] in TPTP_ALL

   def status(self, result):
      return self.valid(result) and result["STATUS"] in self.ok()


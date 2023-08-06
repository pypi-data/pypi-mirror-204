import re
from ..smtsolver import SmtSolver
from ..plugins.shell.limits import Limits
from .. import process
from ...tools import human

Z3_BINARY = "z3"

Z3_STATIC = "-smt2 -st"

Z3_LIMITS = {
   "T": "-T:%s",
   "M": "-memory:%s",
}

Z3_PAT = re.compile(r"^.:([a-z-]*)\s*([0-9.]*)", flags=re.MULTILINE)

class Z3(SmtSolver):
   
   def __init__(self, limit=None, binary=Z3_BINARY, static=Z3_STATIC, plugins=[]):
      cmd = f"{binary} {static}"
      limits = [Limits(limit, Z3_LIMITS)] if limit else []
      SmtSolver.__init__(self, cmd, plugins+limits, wait=1)

   def process(self, output):
      result = process.keyval(Z3_PAT, output)
      result = process.mapval(result, human.numeric)
      return result


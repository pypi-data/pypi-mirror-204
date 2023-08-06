import re

from ..tptpsolver import TptpSolver
from ..plugins.shell.limits import Limits
from .. import process
from ...tools import human


V_BINARY = "vampire"

V_STATIC = "--proof tptp -stat full --input_syntax tptp"

V_LIMITS = {
   "T": "--time_limit %ss",
   "M": "--memory_limit %s",
}

V_PAT = re.compile(r"^% (.*): ([0-9.]*).*$", re.MULTILINE)

V_TABLE = {
   "Active clauses"    : "Active",
   "Passive clauses"   : "Passive",
   "Generated clauses" : "Generated",
   "Initial clauses   ": "Initial",
   "Time elapsed"      : "Runtime",
   "Memory used [KB]"  : "Memory",
   "Split clauses"     : "Splits",
}

class Vampire(TptpSolver):

   def __init__(self, limit=None, binary=V_BINARY, static=V_STATIC, complete=True, plugins=[]):
      cmd = f"{binary} {static}"
      limits = [Limits(limit, V_LIMITS)] if limit else []
      TptpSolver.__init__(self, cmd, plugins+limits, complete, wait=1)

   def process(self, output):
      result = process.keyval(V_PAT, output, V_TABLE)
      result = process.mapval(result, human.numeric)
      return result


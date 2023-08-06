import re

from ..tptpsolver import TptpSolver
from ..plugins.shell.limits import Limits
from .. import process
from ...tools import human


L_BINARY = "lash"

#L_STATIC = "-p tstp -m mode0 -M %s" % getenv("LASH_MODE_DIR", "./modes")
L_STATIC = "-p tstp"

L_PAT = re.compile(r"^% (Steps|Mode): (\S*)$", flags=re.MULTILINE)

L_LIMITS = {
   "T": None,
}

L_TABLE = {
   "Steps": "Steps",
   "Mode": "Mode",
}

class Lash(TptpSolver):

   def __init__(self, limit=None, binary=L_BINARY, static=L_STATIC, complete=True, plugins=[]):
      cmd = f"{binary} {static}"
      limits = [Limits(limit, L_LIMITS)] if limit else []
      TptpSolver.__init__(self, cmd, plugins+limits, complete, wait=0)

   def process(self, output):
      result = process.keyval(L_PAT, output, L_TABLE)
      result = process.mapval(result, human.numeric)
      return result



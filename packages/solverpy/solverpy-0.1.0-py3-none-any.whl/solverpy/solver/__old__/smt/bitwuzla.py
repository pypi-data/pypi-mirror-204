import re
from ..smtsolver import SmtSolver
from ..plugins.shell.limits import Limits
from .. import process
from ...tools import human

BWZ_BINARY = "bitwuzla"

BWZ_STATIC = "-v"

BWZ_LIMITS = {
   "T": "-t=%s",
}

BWZ_TABLE = {
   "variable substitutions"               : "SubstVar",
   "uninterpreted function substitutions" : "SubstUf",
   "embedded constraint substitutions"    : "SubstEc",
   "AIG vectors"                          : "AigVec",
   "AIG ANDs"                             : "AigAnd",
   "AIG variables"                        : "AigVar",
   "CNF variables"                        : "CnfVar",
   "CNF clauses"                          : "CnfCls",
   "CNF literals"                         : "CnfLit",
   "cached (add)"                         : "RwcAdd",
   "cached (get)"                         : "RwcGet",
   "udpated"                              : "RwcUpd",
}

BWZ_KEYS = "|".join(BWZ_TABLE.keys()).replace("(","[(]").replace(")","[)]")

#BWZ_PAT = re.compile(r"^\[bitwuzla>core\]\s*(\d+) ([a-zA-Z ]*)\b", flags=re.MULTILINE)
BWZ_PAT = re.compile(r"^\[bitwuzla>core\]\s*(\d+) (%s)" % BWZ_KEYS, flags=re.MULTILINE)

class Bitwuzla(SmtSolver):
   
   def __init__(self, limit=None, binary=BWZ_BINARY, static=BWZ_STATIC, plugins=[]):
      cmd = f"{binary} {static}"
      limits = [Limits(limit, BWZ_LIMITS)] if limit else []
      SmtSolver.__init__(self, cmd, plugins+limits, wait=1)

   def process(self, output):
      result = process.valkey(BWZ_PAT, output, BWZ_TABLE)
      result = process.mapval(result, human.numeric)
      return result


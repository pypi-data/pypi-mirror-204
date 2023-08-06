import re

from ..updater import Updater
from ... import process

SMT_STATUS = re.compile(r"^(sat|unsat|unknown|timeout)$", re.MULTILINE)

class Smt(Updater):

   def __init__(self):
      pass

   def shell(self, cmd):
      return cmd

   def update(self, instance, strategy, output, result):
      result["STATUS"] = process.single(SMT_STATUS, output, "error")


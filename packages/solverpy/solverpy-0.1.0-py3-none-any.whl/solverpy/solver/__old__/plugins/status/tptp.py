import re

from ..updater import Updater
from ... import process

TPTP_STATUS = re.compile(r"^[#%] SZS status (\S*)", re.MULTILINE)

class Tptp(Updater):

   def __init__(self):
      pass

   def shell(self, cmd):
      return cmd

   def update(self, instance, strategy, output, result):
      result["STATUS"] = process.single(TPTP_STATUS, output, "Error")


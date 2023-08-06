import re

from ..updater import Updater
from ... import process

# real 0.01
# user 0.01
# sys 0.00

TIME_CMD = "/usr/bin/env time -p"

TIME_PAT = re.compile(r"^(real|user|sys) ([0-9.]*)$", re.MULTILINE)

TIME_TABLE = {
   "real": "REALTIME",
   "user": "USERTIME",
   "sys" : "SYSTIME",
}

class Time(Updater):

   def __init__(self):
      self.prefix = TIME_CMD

   def shell(self, cmd):
      return f"{self.prefix} {cmd}"

   def update(self, instance, strategy, output, result):
      res = process.keyval(TIME_PAT, output, TIME_TABLE)
      res = process.mapval(res, float)
      result["RUNTIME"] = res["REALTIME"] - res["SYSTIME"]
      result["USERTIME"] = res["USERTIME"]


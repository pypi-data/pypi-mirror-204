from ..updater import Updater 

TIMEOUT_CMD = "timeout --kill-after=1 --foreground %s"

class Timeout(Updater):

   def register(self, solver):
      solver.updaters.insert(0, self)

   def __init__(self, timeout):
      self.prefix = TIMEOUT_CMD % timeout 

   def shell(self, cmd):
      return f"{self.prefix} {cmd}"

   def update(self, instance, strategy, output, result):
      pass


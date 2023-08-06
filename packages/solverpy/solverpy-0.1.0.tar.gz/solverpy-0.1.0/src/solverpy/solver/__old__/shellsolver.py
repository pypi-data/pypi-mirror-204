import subprocess
from .solver import Solver
from .plugins.shell.timeout import Timeout

class ShellSolver(Solver):

   def __init__(self, cmd, plugins=[], wait=None):
      self.limits = None
      Solver.__init__(self, plugins)
      if (wait is not None) and self.limits and self.limits.timeout:
         Timeout(self.limits.timeout+wait).register(self)
      self.cmd = self.shell(cmd)

   def run(self, instance, strategy):
      cmd = self.command(instance, strategy)
      try:
         output = subprocess.check_output(cmd, shell=True, 
            stderr=subprocess.STDOUT)
      except subprocess.CalledProcessError as e:
         output = e.output
      return output.decode()

   def command(self, instance, strategy):
      (instance, strategy) = self.translate(instance, strategy)
      return f"{self.cmd} {strategy} {instance}"

   def process(self, output):
      raise NotImlementedError()
   
   def timeouted(self, result):
      raise NotImlementedError()

   def valid(self, result):
      return ("STATUS" in result) and ("RUNTIME" in result)

   def solved(self, result, limit=None):
      if not self.valid(result):
         return None
      status = self.status(result)
      if not limit:
         # no limit is specified
         if self.limits and self.limits.timeout:
            # but there is a limit for this solver
            limit = self.limits.timeout
         else:
            # no limits are available
            return status
      # now we have `limit`
      runtime = result["RUNTIME"]
      if status:
         # solved problem will stay solved with higher limits
         return runtime <= limit
      else:
         # timed out run ...
         if runtime > limit:
            # ... will time out with smaller limits
            return False
         else: # TODO: what with `GaveUp`?
            # ... but we don't know what happens with higher limits
            return None

   # plugins control:

   def translate(self, instance, strategy):
      for plugin in self.translators:
         (instance, strategy) = plugin.translate(instance, strategy)
      return (instance, strategy)

   def shell(self, cmd):
      for plugin in self.updaters:
         cmd = plugin.shell(cmd)
      return cmd


from .solver import Solver

class LimitedSolver(Solver):
   
   def __init__(self, cmd, plugins=[], wait=None):
      """
      Setup the Timeout plugin and store limits.
      """
      self.limits = None
      Solver.__init__(self, plugins)
      if (wait is not None) and self.limits and self.limits.timeout:
         Timeout(self.limits.timeout+wait).register(self)
      self.cmd = self.shell(cmd)
   
   def permanent(self, result):
      raise NotImlementedError()
   
   def valid(self, result):
      return ("status" in result) and ("runtime" in result)
   
   def uptodate(self, result):
      """
      Is the result valid with this configuration of limits?
      """

      if not self.valid(result):
         return False

      cutoff = self.limits.timeout
      if self.permanent(result):
         # the result is valid if we have enough time 
         # (permanent results are valid for all timeouts > runtime)
         return result["runtime"] <= cutoff
      else:
         # recompute if we have more time than last runtime
         # (impermanent stays impermanent with timeout <= runtime)
         return result["runtime"] > cutoff

   def simulate(self, result):
      """
      Translate the result to the result yielded by this configuration, if that
      is possible without launching the solver.

      Permanent results always gives some result (non-None).  Only the Status
      can change to TIMEOUT if not enough time is provided.

      Impermanent status can be re-used if a longer timeout than the current
      timeout have been tried.
      """
      
      cutoff = self.limits.timeout
      if self.permanent(result):
         if result["runtime"] > cutoff:
            # the status is permanent, but we don't have enough time
            return dict(result, status="TIMEOUT", runtime=cutoff)
      else:
         if result["runtime"] <= cutoff:
            # the result needs to be recomputed since we have more time
            return None
      return result # the result is already updated


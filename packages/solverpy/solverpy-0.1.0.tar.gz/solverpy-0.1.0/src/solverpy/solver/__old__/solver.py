import time

def updated(call):
   def inner(self, instance, strategy):
      result = self.query(instance, strategy)
      if result: 
         return result
      # the original "call"
      (output, result) = call(self, instance, strategy)
      # 
      self.update(instance, strategy, output, result)
      if not self.valid(result):
         print(f"Error: solverpy: FAILED evaluation of {strategy} on {instance}")
      return result
   return inner

class Solver:

   def __init__(self, plugins=[]):
      self.providers = []
      self.updaters = []
      self.translators = []
      self.init(plugins)

   @updated
   def solve(self, instance, strategy):
      output = self.run(instance, strategy)
      result = self.process(output)
      return (output, result)

   # abstract methods:

   def run(self, instance, strategy):
      raise NotImlementedError()

   def process(self, output):
      raise NotImlementedError()

   def solved(self, result, limit=None):
      raise NotImlementedError()

   # plugins control:

   def init(self, plugins):
      for plugin in plugins:
         plugin.register(self)

   def query(self, instance, strategy):
      for plugin in self.providers:
         result = plugin.query(instance, strategy)
         if result: # TODO: and self.solved(result)
            return result
      return None

   def store(self, instance, strategy, output, result):
      for plugin in self.providers:
         plugin.store(instance, strategy, output, result)

   def update(self, instance, strategy, output, result):
      for plugin in self.updaters:
         plugin.update(instance, strategy, output, result)


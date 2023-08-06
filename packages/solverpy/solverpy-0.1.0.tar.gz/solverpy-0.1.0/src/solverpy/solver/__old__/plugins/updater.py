from .plugin import Plugin

class Updater(Plugin):

   def register(self, solver):
      solver.updaters.append(self)
   
   def shell(self, cmd):
      return cmd

   def update(self, instance, strategy, output, result):
      pass


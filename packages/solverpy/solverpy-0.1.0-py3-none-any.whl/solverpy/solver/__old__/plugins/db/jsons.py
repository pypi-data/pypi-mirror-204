import os
import json

from ..provider import Provider
from ....path import bids
from multiprocessing import Manager

DEFAULT_NAME = "00JSONS"
DEFAULT_DIR = os.getenv("PYSOLVE_JSONS", DEFAULT_NAME)

def path(bid, sid):
   return os.path.join(
      DEFAULT_DIR, 
      bids.name(bid),
      sid).rstrip("/") + ".json"

class Jsons(Provider):
  
   def __init__(self, bid, sid):
      self.bid = bid
      self.sid = sid
      man = Manager()
      self.cache = self.load() # thread-local copy / not synced
      self.results = man.list() # shared list 

   def register(self, solver):
      solver.providers.append(self)
   
   def query(self, instance, strategy):
      (bid, p) = instance
      if not self.check(bid, strategy):
         raise Exception("Error: Query on invalid bid/sid in Jsons.query.")
      return self.cache[p] if p in self.cache else None

   def store(self, instance, strategy, output, result):
      (bid, p) = instance
      if not self.check(bid, strategy):
         raise Exception("Error: Store on invalid bid/sid in Jsons.store.")
      self.results.append((p, result))

   def check(self, bid, sid):
      return (self.bid == bid) and (self.sid == sid)

   def flush(self):
      self.cache.update(dict(self.results))
      while self.results:
         self.results.pop()
      f = path(self.bid, self.sid)
      os.makedirs(os.path.dirname(f), exist_ok=True)
      with open(f,"w") as fw:
         json.dump(self.cache, fw, indent=3, sort_keys=True)

   def load(self):
      f = path(self.bid, self.sid)
      ret = json.load(open(f)) if os.path.isfile(f) else {}
      return ret



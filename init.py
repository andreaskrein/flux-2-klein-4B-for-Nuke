import os
import runpy
import sys
import types

module = types.ModuleType("tokenizerF2k4B")
module.update_group = runpy.run_path(
    os.path.join(os.path.dirname(__file__), "tokenizer.py")
)["update_group"]
sys.modules["tokenizerF2k4B"] = module
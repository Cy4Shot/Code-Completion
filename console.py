import rich
from rich.prompt import Prompt, IntPrompt
from rich.traceback import install

print()
install()

def print(*args, **kwargs):
  rich.print(*args, **kwargs)
  
def choose(choices, message):
  return Prompt.ask(message, choices=choices)

def prompt_int(message, **kwargs):
  return IntPrompt.ask(message, **kwargs)
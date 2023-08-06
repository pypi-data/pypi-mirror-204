"""Firepup650's PYPI Package"""
import os, sys, termios, tty, time
import random as r
import fkeycapture as fkey
def clear() -> None:
  """# Function: clear
    Clears the screen
  # Inputs:
    None

  # Returns:
    None

  # Raises:
    None"""
  os.system("clear")
def cmd(command: str) -> int:
  """# Function: cmd
    Runs bash commands
  # Inputs:
    command: str - The command to run
  
  # Returns:
    int - Status code returned by the command
  
  # Raises:
    None"""
  status = os.system(command)
  return status
def randint(low: int = 0, high: int = 10) -> int:
  """# Funcion: randint
    A safe randint function
  # Inputs:
    low: int - The bottom number, defaults to 0
    high: int - The top number, defaults to 10
  
  # Returns:
    int - A number between high and low
  
  # Raises:
    None"""
  try:
    out = r.randint(low, high)
  except:
    out = r.randint(high, low)
  return out
def e(code: any = 0) -> None:
  """# Function: e
    Exits with the provided code
  # Inputs:
    code: any - The status code to exit with, defaults to 0
  
  # Returns:
    None
    
  # Raises:
    None"""
  sys.exit(code)
def gp(keycount: int = 1, chars: list = ["1" ,"2"], bytes: bool = False) -> str or bytes:
  """# Function: gp
    Get keys and print them.
  # Inputs:
    keycount: int - Number of keys to get, defaults to 1
    chars: list - List of keys to accept, defaults to ["1", "2"]
  
  # Returns:
    str or bytes - Keys pressed
  
  # Raises:
    None"""
  got = 0
  keys = ""
  while got < keycount:
    key = fkey.getchars(1, chars)
    keys = f"{keys}{key}"
    print(key,end="",flush=True)
  print()
  if not bytes:
    return keys
  else:
    return keys.encode()
def printt(text: str, delay: float = 0.1, newline: bool = True) -> None:
  """# Function: printt
    Print out animated text!
  # Inputs:
    text: str - Text to print (could technicaly be a list)
    delay: float - How long to delay between characters, defaults to 0.1
    newline: bool - Wether or not to add a newline at the end of the text, defaults to True
  
  # Returns:
    None
  
  # Raises:
    None"""
  # Store the current terminal settings
  original_terminal_settings = termios.tcgetattr(sys.stdin)
  # Change terminal settings to prevent key interruptions
  tty.setcbreak(sys.stdin)
  for char in text:
    print(char, end='', flush=True)
    time.sleep(delay)
  if newline:
    print()
  # Restore the original terminal settings
  termios.tcsetattr(sys.stdin, termios.TCSADRAIN,original_terminal_settings)
def sleep(seconds: float = 0.5) -> None:
  """# Function: sleep
    Calls `time.sleep(seconds)`
  # Inputs:
    seconds: float - How long to sleep for (in seconds), defaults to 0.5
  
  # Returns:
    None
  
  # Raises:
    None"""
  time.sleep(seconds)
def rseed(seed: any = None, version: int = 2) -> None:
  """# Function: rseed
    reseed the random number generator
  # Inputs:
    seed: any - The seed, defaults to None
    version: int - Version of the seed (1 or 2), defaults to 2
  
  # Returns:
    None
  
  # Raises:
    None"""
  r.seed(seed, version)
def robj(sequence: any) -> object:
  """# Function: robj
    Returns a random object from the provided sequence
  # Input:
    sequence: Sequence[object] - Any valid sequence
  
  # Returns:
    object - A random object from the provided sequence
  
  # Raises:
    None"""
  r.choice(sequence)
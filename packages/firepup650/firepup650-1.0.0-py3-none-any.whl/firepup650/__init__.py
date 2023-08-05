"""Firepup650's PYPI Package"""
import os, sys
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
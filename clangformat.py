import requests
import os
import subprocess
import pathlib

if not os.path.exists(".clang-format"):
  source = "https://gist.githubusercontent.com/u16rogue/18f2f60a3341491a684bd37f84d0c8d5/raw"
  print(f"Requesting clang format from \"{source}\"...")
  r = requests.get(source)
  if r.status_code != 200:
    print(f"Invalid status code {r.status_code}")
    exit(1)
  with open(".clang-format", "w") as file:
    file.write(r.text)
  print(".clang-format generated!")

ext_filter = [".hpp", ".cpp", ".c", ".h", ".cc"]
exclude_dir = [".vs", ".cache", "build", "deps", ".git", ".vscode"]
real_cwd = os.getcwd()
def recursive_formatter(path):
  path = os.path.abspath(path)
  args = ["clang-format", "-i", "-style=file"]
  targets = []
  # Iterate each directory
  with os.scandir(path) as scan:
    for i in scan:
      if any(exd in f"{i}" for exd in exclude_dir):
        continue
      # Recursively iterate
      i = os.path.abspath(i)
      if os.path.isdir(i):
        recursive_formatter(i) 
        continue
      # If its a file grab its suffix (file extension)
      elif os.path.isfile(i):
        sfx = pathlib.Path(i).suffix
        # If the suffix isnt in the targets yet and is one of the filter add it to targets
        if not sfx in targets and sfx in ext_filter:
          targets.append(sfx)
  # Only run formatter in directories with actual files to format
  if os.path.isdir(path) and len(targets) != 0:
    # Reformat the target strings to be consumed by clang format
    for t in targets:
      args.append(os.path.join(path, f"*{t}"))
    print(f"Running on {targets} - \"{path}\"...", end="")
    if subprocess.run(args).returncode != 0:
      print("Failed!")
      return
    print("OK!")
  return
 
print("Running formatter...")
recursive_formatter(real_cwd)

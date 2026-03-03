import os

for name in os.listdir("."):
    if os.path.isdir(name):
        print(name)
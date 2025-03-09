import os

path = 'folder1/folder2'
if not os.path.exists(path):
    os.makedirs(path)

# listsys.py
from collections import namedtuple
"""
# visual structures
[Documents, Music, File] (nid: 0, 1, 2), (gid: 0), (pid: None) (cid: 1, 4)
 |          |
 |          +-> [Playlist, Favorites] (id: 8, 9), (gid: 4), (pid: 0), (cid: None)
 |                         |
 |                         +-> [] ()
 |
 +-> [File, Folder, Directory] (id: 3, 4, 5), (gid: 1), (pid: 0), (cid: 2, 3)
            |       |
            |       +-> [Image] (id: 7), (gid: 3), (pid: 1), (cid: None)
            |
            +-> [Text] (id: 6), (gid: 2), (pid: 1), (cid: None)
------
[
    (nid: 0, gid: 0, pid: !, cid: 1, name: Documents),
    (nid: 1, gid: 0, pid: !, cid: 4, name: Music),
    (nid: 2, gid: 0, pid: !, cid: !, name File),
    (nid: 3, gid: 1, pid: 0, cid: !, name: File),
    (nid: 4, gid: 1, pid: 0, cid: 2, name: Folder),
    (nid: 5, gid: 1, pid: 0, cid: 3, name: Directory),
    (nid: 6, gid: 2, pid: 1, cid: !, name: Text),
    (nid: 7, gid: 3, pid: 1, cid: !, name: Image),
    (nid: 8, gid: 4, pid: 0, cid: !, name: Playlist),
    (nid: 9, gid: 4, pid: 0, cid: 5, name; Favorites)
]
"""
node = namedtuple("Node", "nid gid pid cid name")
dirsort = lambda x: (x.cid is None, x.name)
dirfilter = lambda l, i: list(filter(lambda x: x.gid == i, l))

def inorder_print(l, curdir, level=0):
    if not curdir:
        return
    for file_or_folder in sorted(curdir, key=dirsort):
        print(" " * (level * 4), file_or_folder.nid, file_or_folder.name)
        if file_or_folder.cid:
            subdir = dirfilter(l, file_or_folder.cid)
            inorder_print(l, subdir, level+1)

def preorder_print(l, curdir, level=0):
    pass

def postfix_print(l, curdir, level=0):
    pass

if __name__ == "__main__":
    l = [
        node(1, 0, None, 4, "Music/"),
        node(0, 0, None, 1, "Documents/"),
        node(2, 0, None, None, "File"),
        node(3, 1, 0, None, "File"),
        node(4, 1, 0, 2, "Folder/"),
        node(5, 1, 0, 3, "Directory/"),
        node(6, 2, 1, None, "Text"),
        node(10, 2, 1, None, "Abstract"),
        node(7, 3, 1, None, "Image"),
        node(8, 4, 0, None, "Playlist"),
        node(9, 4, 0, 5, "Favorites/")
    ]

    current_directory_id = 0
    current_directory = dirfilter(l, current_directory_id)
    inorder_print(l, current_directory)
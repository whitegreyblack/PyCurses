# parser.py
import os
import yaml
from system import *
"""
Documents:
  - File
  - Folder:
    - Text
  - Directory:
    - Image
Music:
  - Playlist
  - Favorites: []

# After yaml.load():
Since the nodes themselves only hold a name and type, we have to iterate 
through the structure and build the nodes manually. Once they are built
the should be held in a list with nodes(nid, gid, pid, cid, name).

dict(list(dict(list())))

{
    'Documents': [
        'File', 
        { 'Folder': [ 'Text' ] }, 
        { 'Directory': [ 'Image' ] }
    ], 
    'Music': [
        'Playlist', 
        { 'Favorites': [] }
    ]
}

# From yaml, file structure can go into either hashsys, listsys or hashlistsys
# depending on how efficient the structures are. Need time testings to 
# determine which of the three is the most efficient.
"""

filepath = "system" + os.path.sep + "structure.yaml"
node = namedtuple("Node", "nid gid pid cid name")

def parse(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return yaml.safe_load(data)

def deserialize(data, i=0, sublevel=1):
    s, t = [], []
    for k, v in data.items():
        s.append((k, v, 0, i, '$'))
        i += 1
        while s:
            k, v, l, j, p = s.pop(0)
            if v is not None:
                t.append(node(j, l, p, sublevel, k+"/"))
                if isinstance(v, list):
                    for f in v:
                        if isinstance(f, str):
                            s.append((f, None, sublevel, i, j))
                            i += 1
                        else:
                            for fk, fv in f.items():
                                s.append((fk, fv, sublevel, i, j))
                                i += 1
                sublevel += 1
            else:
                t.append(node(j, l, p, None, k))
    return t

def serialize_list(data):
    pass

def serialize_hash(data):
    pass

def serialize_hashlist(data):
    pass

def to_hashsys(t):
    max_cid = max(-1 if not n.cid else n.cid for n in t)
    d = dict({ i: dirfilter(t, i) for i in range(max_cid) })
    return d

def to_hashlistsys(t):
    d, l = dict(), list()
    max_cid = max(-1 if not n.cid else n.cid for n in t)
    for i in range(max_cid):
        d[i] = set()
        ns = [n for n in dirfilter(t, i)]
        for n in ns:
            d[i].add(n.nid)
            l.append(n)
    return d, l

if __name__ == "__main__":
    # print("""
    # Documents/:
    # - File
    # - Folder/:
    #     - Text
    # - Directory/:
    #     - Image
    # Music/:
    # - Playlist/
    # - Favorites/: []"""[1:])
    structure = parse(filepath)
    # print(structure)
    
    t = deserialize(structure)
    # print_inorder(t)
    print_inorder_indent_tree(t)

    # d = to_hashsys(t)
    # print(d)
    
    # d, l = to_hashlistsys(t)
    # print(d)

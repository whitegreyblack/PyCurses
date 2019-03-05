# parser.py
import yaml
from collections import namedtuple
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

filepath = "system\structure.yaml"
node = namedtuple("Node", "nid gid pid cid name")
dirsort = lambda x: (x.cid is None, x.name)
dirfilter = lambda l, i: list(filter(lambda x: x.gid == i, l))

def parse(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return yaml.safe_load(data)

def deserialize(data, i=0, sublevel=1):
    t = []
    s = []
    # print('n g p c')
    for k, v in data.items():
        s.append((k, v, 0, i, '$'))
        i += 1
        while s:
            k, v, l, j, p = s.pop(0)
            if v:
                # print(j, l, p, sublevel, k)
                t.append(node(j, l, p, sublevel, k))
                if isinstance(v, list):
                    for f in v:
                        if isinstance(f, str):
                            s.append((f, None, sublevel, i, j))
                            i += 1
                        else:
                            for fk, fv in f.items():
                                s.append((fk, fv, sublevel, i, j))
                                i += 1
                elif isinstance(v, dict):
                    for vk, vv in v.items():
                        s.append((vk, vv, sublevel, i, j))
                        i += 1
                sublevel += 1
            else:
                # print(j, l, p, '$', k)
                t.append(node(j, l, p, sublevel, k))
    print()
    for n in t:
        print(el_repr(n))
    print()
    return t

def el_repr(n):
    return f"{n.nid} {n.gid} {n.cid} {n.name}"

def elements(t, i):
    elms = sorted(dirfilter(t, i), key=dirsort, reverse=True)
    print([el_repr(e) for e in elms])
    return elms

def print_inorder(t):
    *ns, n = elements(t, 0)
    while n:
        print(n.nid, n.cid, n.name)
        if n.cid:
            for e in elements(t, n.cid):
                ns.append(e)
            print([el_repr(n) for n in ns])
        n = None
        if ns:
            n = ns.pop()
    # for n in ns:
    #     print(n.nid, n.cid, n.name)

def deserialize_inorder_group(data):
    # initial iteration list
    l = []
    index = 0
    level = 0
    d = [(k, v, level) for k, v in data.items()]
    while d:
        k, v, l = d.pop(0)
        print(l, k)
        if v and isinstance(v, list):
            for f in v:
                if isinstance(f, str):
                    d.append((f, None, l+1))
                else:
                    for fk, fv in f.items():
                        d.append((fk, fv, l+1))
        elif v and isinstance(v, dict):
            for vk, vv in v.items():
                d.append((vk, vv, l+1))

def deserialize_inorder_level(data):
    # initial iteration list
    l = []
    level = 0
    d = [(k, v, level) for k, v in data.items()]
    while d:
        k, v, l = d.pop(0)
        print(l, k)
        if v and isinstance(v, list):
            for f in v:
                if isinstance(f, str):
                    d.insert(0, (f, None, l+1))
                else:
                    for fk, fv in f.items():
                        d.insert(0, (fk, fv, l+1))
        elif v and isinstance(v, dict):
            for vk, vv in v.items():
                d.insert(0, (vk, vv, l+1))

def serialize_list(data):
    pass

def deserialize_hash(data):
    pass

def serialize_hash(data):
    pass

if __name__ == "__main__":
    print("""
    Documents/:
    - File
    - Folder/:
        - Text
    - Directory/:
        - Image
    Music/:
    - Playlist/
    - Favorites/: []"""[1:])
    structure = parse(filepath)
    # print(structure)

    # print("Traverse inorder after printing entire group ('BFS')")
    # deserialize_inorder_group(structure)
    # print()
    # print("Traverse inorder after printing entire level ('DFS')")
    # deserialize_inorder_level(structure)

    print_inorder(deserialize(structure))
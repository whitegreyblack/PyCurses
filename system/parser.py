import yaml
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

After yaml.load():

dict(list(dict(list())))

{
    'Documents': [
        'File', {
            'Folder': [
                'Text'
            ]
        }, {
            'Directory': [
                'Image'
            ]
        }
    ], 
    'Music': [
        'Playlist', {
            'Favorites': []
        }
    ]
}
"""
filepath = "system\structure.yaml"

def parse(filepath):
    with open(filepath, 'r') as f:
        data = f.read()
    return yaml.safe_load(data)

def deserialize(data):
    # using list
    # using hash
    pass

def deserialize_list_inorder(data):
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
                    d.append((f, None, l+1))
                else:
                    for fk, fv in f.items():
                        d.append((fk, fv, l+1))
        elif v and isinstance(v, dict):
            for vk, vv in v.items():
                d.append((vk, vv, l+1))


def deserialize_list_preorder(data):
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
    structure = parse(filepath)
    print(structure)

    deserialize_list_inorder(structure)
    print()
    deserialize_list_preorder(structure)
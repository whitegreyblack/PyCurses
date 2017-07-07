import sys
import yaml
import reciept_yaml

if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit(-1)

    with open(sys.argv[1]) as f:
        obj = yaml.load(f.read())
        tot = sum([obj.prod[k] for k in obj.prod.keys()])
        print(obj.sub, obj.tax, obj.tot)
        if tot != obj.sub:
            print("Subtotal Error")
        if tot+obj.tax != obj.tot:
            print("Total Error")

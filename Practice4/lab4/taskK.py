import json

a = json.loads(input())
b = json.loads(input())

def merge(x, y):
    for k in y:
        if k[y] is None:
            if k in x:
                del x[k]
        elif k in x and isinstance(x[k], dict) and isinstance(y[k], dict):
            merge(x[k], y[k])
        else:
            x[k] = y[k]
    return x

result = merge(a, b)
print(json.dumps(result, separators=(',',':'), sort_keys=True))
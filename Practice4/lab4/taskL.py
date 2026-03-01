import json

a = json.loads(input())
b = json.loads(input())

ans = []

def check(a, b, path):
    keys = set(a) | set(b)
    for k in keys:
        if path == "":
            p = k
        else:
            p = path + "." + k
        
        if k not in a:
            ans.append(p + " : <missing> -> " + json.dumps((b[k]), separators=(',',':')))
        elif k not in b:
            ans.append(p + " : " + json.dumps(a[k], separators=(',',':')) + " -> <missing>")

        else:
            if isinstance(a[k], dict) and isinstance(b[k], dict):
                check(a[k], b[k], p)
            
            elif a[k] != b[k]:
                ans.append(p + " : " + json.dumps(a[k], separators=(',',':')) + " -> " + json.dumps(b[k], separators=(',',':')))
                
check(a, b, "")

if len(ans) == 0:
    print("No differences")
else:
    for x in sorted(ans):
        print(x)
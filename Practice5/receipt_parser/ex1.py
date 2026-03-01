for line in open("Practice5/receipt_parser/raw.txt"):
    name, price = line.split()
    print(name, "->", price)
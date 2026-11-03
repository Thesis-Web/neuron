p = "/home/james/cortex/cortex.py"; s = open(p).read()
old = '''NUM = re.compile(r"\\d[\\w.%]*")'''
new = '''NUM = re.compile(r"(?<![\\w.])\\d[\\w.%]*")   # a value starts a token: c10.1, c18 and run401 are labels, not values (C17.2)'''
assert s.count(old) == 1, s.count(old); s = s.replace(old, new); open(p, "w").write(s); print("numbers: labels are not values")

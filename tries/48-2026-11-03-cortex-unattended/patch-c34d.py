p = "/home/james/cortex/cortex.py"; s = open(p).read()
old = '''    return [x.rstrip(".,;:") for x in (NUM_CLOCK if clock else NUM).findall(t) if x.rstrip(".,;:")]
NUM_CLOCK = re.compile(r"(?<![\\w.])\\d[\\w.%:]*")
'''
new = '''    return [y for y in (x.strip("'\\"()[]{}").rstrip(".,;:") for x in (NUM_CLOCK if clock else NUM).findall(t)) if y]   # quotes and brackets around a number are punctuation
NUM_CLOCK = re.compile(r"(?<![\\w.])\\d[\\w.%:]*")
'''
assert s.count(old) == 1; s = s.replace(old, new); open(p, "w").write(s); print("patched c34d")

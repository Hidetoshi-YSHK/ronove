import re

SPEC_FILE = "ronove.spec"
LINE_TO_INSERT = "          Tree('resources',prefix='resources'),\n"

lines = []
with open(SPEC_FILE, "r") as f:
    lines = f.readlines()

index = None
pattern = re.compile(r'^exe')
for i, line in enumerate(lines):
    if pattern.search(line):
        index = i
        break

if index:
    lines.insert(index + 1, LINE_TO_INSERT)

with open(SPEC_FILE, "w") as f:
    f.writelines(lines)
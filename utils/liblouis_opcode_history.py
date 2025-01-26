# Build a table of opcodes through different versions of Liblouis
# Note: run at the root of the Liblouis repo
import re
import json
import subprocess
import os

versions = {}

tags = subprocess.check_output(["git", "tag"]).decode("OEM").split("\n")
for tag in tags:
    if re.fullmatch("^v[\\d.]*$", tag.strip()):
        subprocess.call(["git", "reset", "--hard", tag.strip()], stdout=subprocess.DEVNULL)
        with open(os.path.join("doc", "liblouis.texi"), "r", encoding="utf-8") as f:
            fc = f.read()
            opcodes = [m[0] for m in re.findall(r"@opcode\{(?P<code>[^},]*)(,[^}]*)*\}", fc)]
            depr_opcodes = [m[0] for m in re.findall(r"@deprecatedopcode\{(?P<code>[^},]*)(,[^}]*)*\}", fc)]
            versions[tag.strip()] = {"opcodes": opcodes, "depr_opcodes": depr_opcodes}

with open("opcode_history.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(versions, indent=2))

# Sort versions by semantic version
vks = list(versions.keys())
vks.sort(key = lambda x: [int(i) for i in re.findall(r"v([\d]*)\.([\d]*)\.([\d]*)", x)[0]])

opcodes = set()
for v in versions.keys():
    for c in versions[v]["opcodes"]:
        opcodes.add(c)
    for c in versions[v]["depr_opcodes"]:
        opcodes.add(c)

opcode_lives = {}
for c in opcodes:
    created = ""
    deprecated = ""
    removed = ""
    for v in vks:
        if c in versions[v]["opcodes"]:
            if created == "":
                created = v
        elif c in versions[v]["depr_opcodes"]:
            if deprecated == "":
                deprecated = v
        else:
            if created != "":
                removed = v
    if deprecated == "":
        if removed == "":
            deprecated = "not yet"
        else:
            deprecated = "was not deprecated before removal"
    if removed == "":
        removed = "not yet"
    opcode_lives[c] = {
        "created": created,
        "deprecated": deprecated,
        "removed": removed
    }

with open("opcode_lives.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(opcode_lives, indent=2))

#@author
#@category Analysis
#@keybinding
#@menupath
#@toolbar

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor
from ghidra.program.model.pcode import PcodeOp

import json

results = []

def get_callee_name(op):
    inp0 = op.getInput(0)
    if inp0 is None:
        return None
    try:
        return inp0.getAddress().toString()
    except:
        return str(inp0)

decomp = DecompInterface()
decomp.openProgram(currentProgram)

fm = currentProgram.getFunctionManager()
funcs = fm.getFunctions(True)

monitor = ConsoleTaskMonitor()

for func in funcs:

    res = decomp.decompileFunction(func, 60, monitor)
    if not res.decompileCompleted():
        continue

    hf = res.getHighFunction()
    if hf is None:
        continue

    ops = hf.getPcodeOps()

    while ops.hasNext():
        op = ops.next()

        if op.getOpcode() != PcodeOp.CALL:
            continue

        callee = get_callee_name(op)

        if callee is None:
            continue

        # match fgets (PLT or resolved name)
        if "fgets" not in callee:
            continue

        entry = {
            "func": func.getName(),
            "addr": str(op.getSeqnum().getTarget()),
            "callee": callee,
            "buf": None,
            "size": None,
            "stream": None
        }

        # fgets(buf, size, stream)
        if op.getNumInputs() >= 4:
            try:
                entry["buf"] = str(op.getInput(1))
                entry["size"] = str(op.getInput(2))
                entry["stream"] = str(op.getInput(3))
            except:
                pass

        results.append(entry)

# dump results
print(json.dumps(results, indent=2))

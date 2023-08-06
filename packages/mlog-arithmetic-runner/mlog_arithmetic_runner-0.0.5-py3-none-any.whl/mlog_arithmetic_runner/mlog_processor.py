from .memory import MemoryCell
from .arithmetic_operators import arithmetic_operators


def convert_to_float(obj):
    if isinstance(obj, float):
        return obj
    if isinstance(obj, int):
        return float(obj)
    return 0 if obj is None else 1


class MlogProcessor:
    def __init__(self, ipt=2, memory_cells=0, memory_banks=0):
        self.ipt = ipt
        self.instructions_executed = 0
        self.current_line = 0
        self.next_line = 0
        self.memory_cells = memory_cells
        self.memory_banks = memory_banks
        self.code = []
        self.constants = {
            "true": 1,
            "false": 0,
            "null": None
        }
        self.lambda_variables = {
            "@tick": lambda: self.instructions_executed // self.ipt,
            "@time": lambda: (self.instructions_executed // self.ipt) / 60.0,
            "@counter": lambda: self.current_line + 1,
            "@ipt": lambda: self.ipt,
            # getlink get cells/banks
            "@links": lambda: self.memory_cells + self.memory_banks,
        }
        self.variables = {}
        self.reset()

    def assemble_code(self, mlog_code: str):

        rawCode = self.solveLabel(mlog_code)

        for tokens in rawCode:
            self.code.append(tuple(tokens))

    def solveLabel(self, mlog_code):
        rawCode = []
        labels = {}
        todel = []
        for line in mlog_code.splitlines():
            tokens = line.split()
            if len(tokens) <= 0:
                continue
            rawCode.append(tokens)
        for j in range(len(rawCode)):
            tokens = rawCode[j]
            if len(tokens) == 1 & tokens[0].endswith(":"):
                labels[tokens[0].strip(":")] = rawCode[j + 1]
                todel.append(tokens)
        for label in todel:
            rawCode.remove(label)
        for label in labels.keys():
            index = rawCode.index(labels.get(label))
            for tokens in rawCode:
                if (tokens[0] == "jump") & (tokens[1] == label):
                    tokens[1] = index
        return rawCode

    def reset(self):
        self.current_line = 0
        self.instructions_executed = 0
        self.constants = {
            "true": 1,
            "false": 0,
            "null": None
        }
        self.variables = {}
        for i in range(self.memory_cells):
            self.constants[f"cell{i + 1}"] = MemoryCell(64)
        for i in range(self.memory_banks):
            self.constants[f"bank{i + 1}"] = MemoryCell(512)

    def get_variable(self, name: str):
        if name.startswith("@"):
            return self.lambda_variables.get(name, lambda: None)()
        if name in self.constants:
            return self.constants[name]
        if name in self.variables:
            return self.variables[name]
        try:
            return float(name)
        except ValueError:
            return None

    def set_variable(self, name: str, value):
        if name.startswith("@"):
            if name == "@counter":
                self.next_line = int(value)
            return
        self.variables[name] = value

    def run_one_instruction(self) -> bool:
        "Return False on self-loop or past-the-end."
        self.next_line = self.current_line + 1
        if self.current_line >= len(self.code):
            return False
        tokens = self.code[self.current_line]
        if tokens[0] == "set":
            self.set_variable(tokens[1], self.get_variable(tokens[2]))
        elif tokens[0] == "op":
            op = tokens[1]
            var_a = convert_to_float(self.get_variable(tokens[3]))
            var_b = convert_to_float(self.get_variable(tokens[4]))
            runner = arithmetic_operators.get(op, lambda a, b: None)
            self.set_variable(tokens[2], runner(var_a, var_b))
        elif tokens[0] == "jump":
            dest, op = int(tokens[1]), tokens[2]
            var_a = self.get_variable(tokens[3])
            var_b = self.get_variable(tokens[4])
            runner = arithmetic_operators.get(op, lambda a, b: False)
            if runner(var_a, var_b):
                self.next_line = dest
        elif tokens[0] == "end":
            self.next_line = 0
        elif tokens[0] == "write":
            value = convert_to_float(self.get_variable(tokens[1]))
            mem: MemoryCell = self.get_variable(tokens[2])
            pos = self.get_variable(tokens[3])
            if isinstance(mem, MemoryCell):
                mem.write(pos, value)
        elif tokens[0] == "read":
            mem: MemoryCell = self.get_variable(tokens[2])
            pos = self.get_variable(tokens[3])
            if isinstance(mem, MemoryCell):
                self.set_variable(tokens[1], mem.read(pos))
        elif tokens[0] == "getlink":
            # getlink get memory cells/banks ONLY
            link_id = int(self.get_variable(tokens[2]))
            if link_id >= self.get_variable("@links") or link_id < 0:
                self.set_variable(tokens[1], None)
            elif link_id < self.memory_cells:
                self.set_variable(tokens[1], self.get_variable(f"cell{link_id + 1}"))
            else:
                self.set_variable(tokens[1], self.get_variable(f"bank{link_id - self.memory_cells + 1}"))
        else:
            raise ValueError(f"Unsupported instruction {tokens[0]}")
        self.instructions_executed += 1
        # Self-loop detected
        if self.next_line == self.current_line:
            return False
        self.current_line = self.next_line
        return True

    def run_with_limit(self, limit: int, stop_if_past_the_end=True) -> int:
        """\
Return actual cycles we had ran, stop on self-loops.
Suppose we have such mlog code:
    set a 42
    jump 1 always 0 0
run_with_limit(1) executes only "set a 42"
run_with_limit(2) (or 3, 4...) stops after executing "jump 1 always 0 0"
"""
        code_length = len(self.code)
        while self.instructions_executed < limit:
            should_continue = self.run_one_instruction()
            if not should_continue:
                break
            if self.current_line == code_length:
                if stop_if_past_the_end:
                    break
                else:
                    self.current_line = 0
        return self.instructions_executed

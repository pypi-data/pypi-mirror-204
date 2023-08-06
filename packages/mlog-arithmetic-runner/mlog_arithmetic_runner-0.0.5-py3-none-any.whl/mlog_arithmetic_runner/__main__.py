import argparse
import json
import sys
from .mlog_processor import MlogProcessor

parser = argparse.ArgumentParser(prog="mlog_arithmetic_runner",
                                 description="Reads some mlog code from stdin, runs it, and generates JSON report")
parser.add_argument("--limit", type=int, default=int(1e8),
                    help="Max instructions/cycles allowed, something like TimeLimit")
parser.add_argument("--continue-if-past-the-end", action="store_true")
parser.add_argument("--ipt", type=int, default=2,
                    help="Instructions per tick. 2 for micro-processor, 8 for logic-processor, 25 for hyper-processor")
parser.add_argument("--memory-banks", type=int, default=0,
                    help="Memory bank count")
parser.add_argument("--memory-cells", type=int, default=0,
                    help="Memory cell count")
parser.add_argument("--json-indent", type=int, default=4,
                    help="JSON indent, set 0 to disable")
parser.add_argument("--json-dump-memory-blocks", action="store_true",
                    help="dump all memory content in JSON report")


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = parser.parse_args(argv)
    processor = MlogProcessor(args.ipt, args.memory_cells, args.memory_banks)
    stop_if_past_the_end = not bool(args.continue_if_past_the_end)
    # Drain sys.stdin
    processor.assemble_code(sys.stdin.read())
    cycles = 0
    success = True
    reason = ""
    try:
        cycles = processor.run_with_limit(args.limit, stop_if_past_the_end)
    except BaseException as exception:
        success = False
        reason = str(exception)

    report_dict = {
        "cycles": cycles,
        "success": success,
        "reason": reason,
        "variables": processor.variables,
        "memory_blocks": {},
    }
    if args.json_dump_memory_blocks:
        contents = {}
        for i in range(processor.memory_cells):
            name = f"cell{i+1}"
            contents[name] = processor.get_variable(name).memory
        for i in range(processor.memory_banks):
            name = f"bank{i+1}"
            contents[name] = processor.get_variable(name).memory
        report_dict["memory_blocks"] = contents
    indent = None if args.json_indent <= 0 else args.json_indent
    json.dump(report_dict, sys.stdout, ensure_ascii=True, indent=indent, skipkeys=True,
              default=lambda obj: "<Object>")


if __name__ == "__main__":
    main()
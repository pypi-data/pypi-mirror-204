import argparse
from typing import List, Any, Dict

import sys

import json_stream_parser


_skip_obj = object()


# Define a context manager to temporarily modify global variables
class TempGlobalVars:
    def __init__(self, temp_globals: Dict[str, Any]):
        self.old_globals = globals().copy()
        for k in list(globals().keys()):
            del globals()[k]
        for k, v in temp_globals.items():
            temp_globals[k] = v

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for k in list(globals().keys()):
            del globals()[k]
        for k, v in self.old_globals.items():
            globals()[k] = v


def _strip_trailing_newline(line: str):
    if line.endswith('\n'):
        return line[:-1]
    else:
        return line


def _exec_transform(obj, func_strs: List[str], imported_modules: Dict[str, Any]):
    result = obj

    for i, func_str in enumerate(func_strs):
        # Compile the argv
        code = compile(func_str, f'function-in-cmdline-{i}', 'eval')
        curr_locals = {'self': result,
                       'skip': _skip_obj}
        eval_result = eval(code, imported_modules, curr_locals)

        with TempGlobalVars(imported_modules):
            # If the result is a function, execute it; otherwise treat it as an expression
            if callable(eval_result):
                result = eval_result(result)
            else:
                result = eval_result

    return result


def _print_if_not_skip(obj, **kwargs):
    if obj is not _skip_obj:
        print(obj, **kwargs)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('functions', nargs='+', help='list of functions to apply')
    parser.add_argument('-s', '--slurp', action='store_true', help='process input as a single array')
    parser.add_argument('-r', '--raw', action='store_true', help='process non-JSON / plaintext data')
    parser.add_argument('-i', '--import', dest='imports', action='append', default=[], help='import packages')
    args = parser.parse_args()

    # Import packages if specified
    imported_modules = {}
    for import_str in args.imports:
        import_str = import_str.strip()
        if import_str.startswith('from '):
            exec(import_str, globals(), imported_modules)
        else:
            exec(f"import {import_str}", globals(), imported_modules)

    # Define functions to be applied
    func_strs = []
    for func_str in args.functions:
        if func_str.startswith('.'):
            func_str = 'lambda self: self' + func_str
        func_strs.append(func_str)

    if args.raw:
        if args.slurp:
            lines = list(map(_strip_trailing_newline, sys.stdin))
            _print_if_not_skip(_exec_transform(lines, func_strs, imported_modules))

        else:
            for line in sys.stdin:
                line = _strip_trailing_newline(line)
                _print_if_not_skip(_exec_transform(line, func_strs, imported_modules))

    else:
        if args.slurp:
            objs = list(json_stream_parser.load_iter(sys.stdin))
            _print_if_not_skip(_exec_transform(objs, func_strs, imported_modules))

        else:
            for obj in json_stream_parser.load_iter(sys.stdin):
                _print_if_not_skip(_exec_transform(obj, func_strs, imported_modules))

    return 0


if __name__ == '__main__':
    exit(main())

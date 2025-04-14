import inspect
import json
import os
import types
from functools import wraps

call_chains = {}
call_list = []
first_test = 0
first_call = 0


def trace_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)

    return wrapper


def get_class_from_frame(fr):
    args, _, _, value_dict = inspect.getargvalues(fr)
    if len(args) and args[0] == 'self':
        instance = value_dict.get('self', None)
        if instance:
            return instance.__class__.__name__
    return None


def decorate_module_functions(module, module_name, test_folder):
    for attr_name in dir(module):
        attr = getattr(module, attr_name)
        if isinstance(attr, types.FunctionType) and not attr_name.startswith("__"):
            wrapped_func = trace_calls(attr)

            def tracefunc(frame, event, arg, indent=[0]):
                global first_test, first_call
                file_name = os.path.basename(frame.f_code.co_filename).replace(".py", "")
                function_name = frame.f_code.co_name
                class_name = get_class_from_frame(frame)
                full_test_name = f"{test_folder}.{file_name}.{function_name}"

                if class_name:
                    full_test_name += f"[{class_name}]"

                if event == "call":
                    indent[0] += 1
                    if first_test and first_test.startswith(f"{test_folder}."):
                        if first_call == 0:
                            call_chains[first_test].append([{full_test_name: indent[0]}])
                            first_call = full_test_name
                        else:
                            call_chains[first_test][-1].append({full_test_name: indent[0]})
                    if function_name.startswith("test_"):
                        call_chains.setdefault(full_test_name, [])
                        first_test = full_test_name
                elif event == "return":
                    if full_test_name == first_test:
                        first_test = 0
                    elif full_test_name == first_call:
                        first_call = 0
                    indent[0] -= 1
                return tracefunc

            import sys
            sys.setprofile(tracefunc)
            wrapped_func()


def save_call_chains_to_json(output_file):
    with open(output_file, "w") as f:
        json.dump(call_chains, f, indent=4)
    print(f"Call chains saved: {output_file}")


def convert_call_chains(call_chains):
    converted = {}
    for test_name, call_list in call_chains.items():
        chains = []
        for call_chain in call_list:
            path = []
            for i, call in enumerate(call_chain):
                name, indent = next(iter(call.items()))
                name = name.split(".", 1)[-1]
                while path and path[-1][1] >= indent:
                    path.pop()
                path.append((name, indent))
                is_last = i == len(call_chain) - 1
                next_indent = list(call_chain[i + 1].values())[0] if not is_last else None
                if is_last or next_indent <= indent:
                    new_chain = [n for n, _ in path]
                    if new_chain not in chains:
                        chains.append(new_chain)
        converted[test_name] = chains
    return converted


def trace_test_files(test_folder, output_file):
    global call_chains
    test_files = [f for f in os.listdir(test_folder) if f.startswith("test_") and f.endswith(".py")]

    for test_file in test_files:
        module_name = test_file[:-3]
        module = __import__(f"{test_folder}.{module_name}", fromlist=["*"])
        decorate_module_functions(module, module_name, test_folder)
        if hasattr(module, "__main__"):
            module.__main__()

    call_chains = convert_call_chains(call_chains)
    save_call_chains_to_json(output_file)


if __name__ == "__main__":
    TEST_FOLDER = "tests"
    OUTPUT_FILE = "callchains.json"
    trace_test_files(TEST_FOLDER, OUTPUT_FILE)

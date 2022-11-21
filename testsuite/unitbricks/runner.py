import importlib.util
from os import listdir
from os.path import isfile, join
from unitbricks import reset_time

def run_tests(path):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    total = 0
    success = 0
    failure = 0
    for file in files:
        (s, f, t) = run_module(f'{path}/{file}')
        total = total + t
        success = success + s
        failure = failure + f

    print(f"\n{success}/{total} OK, {failure}/{total} failed")
    return success == total

def run_module(path):
    name = path.replace('/', '_').replace('.py', '')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    tests = list(filter(lambda attr: attr[:5] == 'test_', dir(module)))
    results = list(map(lambda test: run_test(name, module, test), tests))

    total = len(tests)
    success = len(list(filter(lambda result: result, results)))
    failure = len(list(filter(lambda result: not result, results)))

    print(f"=== Module {name}: {success}/{total} OK, {failure}/{total} failed")

    return (success, failure, total)

def run_test(modname, module, test):
    print(f'\n== Test {modname}/{test}"\n')

    func = getattr(module, test)
    try:
        reset_environment()
        result = func()
        if result == None:
            return True
        else:
            return result
    except Exception as ex:
        print('Error:', ex)
        return False

def reset_environment():
    reset_time()
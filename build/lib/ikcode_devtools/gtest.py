import inspect

__all__ = ["gTest", "gtest_registry"]

gtest_registry = {}

def generate_test_code(func_name, test_type, args):
    arg_list = ", ".join("None" for _ in args)

    if test_type == "debug":
        code = f"""def test_{func_name}_debug():
    print("Running {func_name} with args: {arg_list}")
    result = {func_name}({arg_list})
    print("Result:", result)
    # TODO: Add asserts here
"""
    elif test_type == "run":
        code = f"""def test_{func_name}_run():
    result = {func_name}({arg_list})
    assert result == "expected_value"  # TODO: Set expected value
"""
    elif test_type == "exception":
        code = f"""import pytest

def test_{func_name}_raises():
    with pytest.raises(Exception):
        {func_name}({arg_list})
"""
    elif test_type == "print":
        code = f"""def test_{func_name}_print():
    print("Calling {func_name}({arg_list})")
    result = {func_name}({arg_list})
    print("Output:", result)
"""
    elif test_type == "type_check":
        code = f"""def test_{func_name}_type_check():
    result = {func_name}({arg_list})
    assert isinstance(result, ExpectedType)  # Replace ExpectedType accordingly
"""
    elif test_type == "no_exception":
        code = f"""def test_{func_name}_no_exception():
    try:
        {func_name}({arg_list})
    except Exception as e:
        assert False, f"Unexpected exception raised: {{e}}"
"""
    elif test_type == "side_effect":
        code = f"""def test_{func_name}_side_effect():
    # TODO: Setup preconditions
    {func_name}({arg_list})
    # TODO: Assert side effects here
"""
    elif test_type == "performance":
        code = f"""import time

def test_{func_name}_performance():
    start = time.time()
    {func_name}({arg_list})
    end = time.time()
    print(f"Execution time: {{end - start}} seconds")
    # TODO: Add performance assertions
"""
    elif test_type == "parametrized":
        code = f"""import pytest

@pytest.mark.parametrize("args, expected", [
    # TODO: Add test cases as tuples of (args, expected)
])
def test_{func_name}_parametrized(args, expected):
    result = {func_name}(*args)
    assert result == expected
"""
    else:
        code = f"""def test_{func_name}():
    # TODO: Replace with your test
    pass
"""

    return code

def gTest(func):
    func_name = func.__name__
    sig = inspect.signature(func)
    args = list(sig.parameters.keys())

    # Generate test codes for multiple test types
    test_types = ["run", "debug", "exception", "print", "type_check"]
    all_test_codes = {}

    for t in test_types:
        all_test_codes[t] = generate_test_code(func_name, t, args)

    # Store a dict with args and all test codes keyed by test type
    gtest_registry[func_name] = {
        "args": args,
        "tests": all_test_codes
    }

    return func

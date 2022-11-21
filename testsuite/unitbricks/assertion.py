
def assert_equals(expected, given, name=""):
    if expected != given:
        raise AssertionError(f"Assertion: expected {expected} but got {given}: {name}")

def assert_true(given, name=""):
    assert_equals(True, given, name)

def assert_false(given, name=""):
    assert_equals(False, given, name)

def assert_less(max, given, name=""):
    if given >= max:
        raise AssertionError(f"Assertion: expected less than {max} but got {given}: {name}")

def assert_less_equals(max, given, name=""):
    if given > max:
        raise AssertionError(f"Assertion: expected less than or equals {max} but got {given}: {name}")

def assert_more(min, given, name=""):
    if given >= min:
        raise AssertionError(f"Assertion: expected more than {min} but got {given}: {name}")

def assert_more_equals(min, given, name=""):
    if given > min:
        raise AssertionError(f"Assertion: expected more than or equals {min} but got {given}: {name}")

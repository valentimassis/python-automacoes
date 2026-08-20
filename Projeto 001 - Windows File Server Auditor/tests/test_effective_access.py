from wfsa.analyzers.access import calculate_effective_access


def test_full_and_full_is_full():
    assert calculate_effective_access("FULL", "FULL") == "FULL"


def test_full_and_modify_is_modify():
    assert calculate_effective_access("FULL", "MODIFY") == "MODIFY"


def test_full_and_read_is_read():
    assert calculate_effective_access("FULL", "READ") == "READ"


def test_modify_and_full_is_modify():
    assert calculate_effective_access("MODIFY", "FULL") == "MODIFY"


def test_modify_and_modify_is_modify():
    assert calculate_effective_access("MODIFY", "MODIFY") == "MODIFY"


def test_modify_and_read_is_read():
    assert calculate_effective_access("MODIFY", "READ") == "READ"


def test_read_and_full_is_read():
    assert calculate_effective_access("READ", "FULL") == "READ"


def test_read_and_modify_is_read():
    assert calculate_effective_access("READ", "MODIFY") == "READ"


def test_read_and_read_is_read():
    assert calculate_effective_access("READ", "READ") == "READ"

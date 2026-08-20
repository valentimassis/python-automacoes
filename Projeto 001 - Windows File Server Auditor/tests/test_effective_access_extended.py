from wfsa.analyzers.access import calculate_effective_access


def test_write_and_full_is_write():
    assert calculate_effective_access("WRITE", "FULL") == "WRITE"


def test_full_and_write_is_write():
    assert calculate_effective_access("FULL", "WRITE") == "WRITE"


def test_read_execute_and_full_is_read_execute():
    assert calculate_effective_access("READ_EXECUTE", "FULL") == "READ_EXECUTE"


def test_full_and_read_execute_is_read_execute():
    assert calculate_effective_access("FULL", "READ_EXECUTE") == "READ_EXECUTE"


def test_modify_and_write_is_write():
    assert calculate_effective_access("MODIFY", "WRITE") == "WRITE"


def test_write_and_modify_is_write():
    assert calculate_effective_access("WRITE", "MODIFY") == "WRITE"

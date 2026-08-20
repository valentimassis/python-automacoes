from wfsa.analyzers.access import normalize_access_right


def test_normalize_full():
    assert normalize_access_right("Full") == "FULL"


def test_normalize_full_control():
    assert normalize_access_right("FullControl") == "FULL"


def test_normalize_modify():
    assert normalize_access_right("Modify") == "MODIFY"


def test_normalize_read():
    assert normalize_access_right("Read") == "READ"


def test_normalize_write():
    assert normalize_access_right("Write") == "WRITE"


def test_normalize_read_and_execute():
    assert normalize_access_right("ReadAndExecute") == "READ_EXECUTE"

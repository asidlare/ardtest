from models.fizzbuzz import valid_params, fizzbuzz, fizzbuzz_full
import io
import pytest


def test_valid_params():
    with pytest.raises(TypeError):
        valid_params(1)
    assert valid_params(1, 3) is True, "all validation conditions fulfilled"
    assert valid_params(1, 10000) is True, "all validation conditions fulfilled, max values"
    assert valid_params(3, 1) is False, "swapped values"
    assert valid_params(1, 1) is False, "equal values"
    assert valid_params(0, 1) is False, "too small first value"
    assert valid_params(1, 10001) is False, "too big second value"


def test_fizzbuzz():
    with pytest.raises(TypeError):
        fizzbuzz(1)
    with pytest.raises(ValueError):
        fizzbuzz(3, 1)
    assert fizzbuzz(1, 3) == [1, 2, 'Fizz'], 'range from 1 to 3'
    assert fizzbuzz(9, 16) == ['Fizz', 'Buzz', 11, 'Fizz', 13, 14, 'FizzBuzz', 16], 'range from 9 to 16'


def test_fizzbuzz_full(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO("1\n3\n"))
    fizzbuzz_full()
    output = capsys.readouterr()
    assert output.out == 'Output:\n1\n2\nFizz\n', 'test output, integer args'
    assert output.err == '', 'test stderr, integer args'
    # -----------------------------------------------------------------------
    monkeypatch.setattr('sys.stdin', io.StringIO("a\n1\nb\nc\n3\n"))
    fizzbuzz_full()
    output = capsys.readouterr()
    assert output.out == "Output:\n1\n2\nFizz\n", 'test output, integer args + string args'
    assert output.err == "", 'test stderr, integer args + string args'
    # -----------------------------------------------------------------------
    monkeypatch.setattr('sys.stdin', io.StringIO("3\n1\n"))
    with pytest.raises(ValueError):
        fizzbuzz_full()
    output = capsys.readouterr()
    assert output.out == "Output:\n", 'test output, swapped args'
    assert output.err == "", 'test output, swapped args'

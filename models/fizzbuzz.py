import typing
from typing import List


def valid_params(n: int, m: int) -> bool:
    """
    Functions checks if inserted params are correct.
    :param n: start value
    :param m: stop value
    :return: bool
    """
    if isinstance(n, int) and isinstance(m, int):
        if 1 <= n < m <= 10000:
            return True
    return False


def fizzbuzz(n: int, m: int) -> List[str]:
    """
    This function operates on list containing integers from n to m.
    In case the number can be divided by 3 or 5 without rest, the number is replaced by proper string.
    :param n: int start value
    :param m: int stop value
    :return: List[str]
    """
    output = []
    if valid_params(n, m):
        for x in range(n, m + 1):
            if x % 3 == 0:
                if x % 5 == 0:
                    output.append('FizzBuzz')
                    continue
                output.append('Fizz')
            elif x % 5 == 0:
                output.append('Buzz')
            else:
                output.append(x)
    else:
        raise ValueError('Numbers not correct. They should fulfill requirements 1 <= n < m <= 10000')

    return output


def fizzbuzz_full():
    """
    This function reads 2 integers from input and runs fizzbuzz function.
    At the end the result is printed.
    :return:
    """
    inp = []
    while len(inp) < 2:
        try:
            inp.append(int(input()))
        except ValueError:
            pass
    print("Output:")
    print(*fizzbuzz(*inp), sep="\n")


if __name__ == '__main__':
    fizzbuzz_full()

import os
from collections import defaultdict
import typing
from typing import Dict

here = os.path.abspath(os.path.dirname(__file__))
tmpdir = os.path.join(here, '..', 'tmp')


def _csv_data(filename: str):
    """
    It is generator which opens a file, read header and saves rows after strip and split.
    :param filename: str:
    :return: None
    """
    filename = os.path.join(tmpdir, filename)
    try:
        with open(filename, 'r') as file:
            file.readline()
            for l in file.readlines():
                line = l.strip().split(",")
                yield line
    except FileNotFoundError:
        raise FileNotFoundError(f"File {filename} does not exist!")


def valuate():
    """
    The goal of this function is to return data about top products.
    Three files are read to valuate (all of them are placed in tmp folder in app directory):
    :inputfile currencies.csv - currency with factor
    :inputfile data.csv - raw products data containing many entries (instances) of product
    :inputfile matchings.csv - information how many meaningful instances of product use in calculations
    :return: Dict top products aggregated data
    """
    currency = dict()
    for row in _csv_data('currencies.csv'):
        try:
            currency[row[0]] = float(row[1])
        except IndexError:
            raise IndexError(f"Too short line in file currencies.csv")

    data = defaultdict(list)
    for row in _csv_data('data.csv'):
        try:
            x = float(row[1]) * currency[row[2]] * float(row[3])
            data[row[4]].append(x)
        except IndexError:
            raise IndexError(f"Too short line in file data.csv")
        except KeyError:
            raise KeyError(f"Currency {row[2]} not present in file currency.csv")

    output = []
    for row in _csv_data('matchings.csv'):
        try:
            topnum = min(int(row[1]), len(data[row[0]]))
            if row[0] in data and len(data[row[0]]) >= topnum:
                topsum = sum(
                    prize for it, prize in enumerate(sorted(data[row[0]], reverse=True))
                    if it < topnum
                )
                top = [
                    row[0],
                    topsum,
                    round(topsum / topnum, 2) if topnum > 0 else 0,
                    'PLN',
                    len(data[row[0]]) - topnum
                ]
                output.append(top)
        except IndexError:
            raise IndexError(f"Too short line in file matchings.csv")
    return output


def valuation_service():
    """
    Function to write valuation data to file top_products.csv. File is located in tmp directory.
    :return:
    """
    valuation = valuate()
    with open(os.path.join(tmpdir, 'top_products.csv'), 'w') as f:
        f.write('matching_id,total_price,avg_price,currency,ignored_products_count\n')
        for line in valuation:
            f.write(",".join(map(str, line)) + '\n')


if __name__ == '__main__':
    valuation_service()

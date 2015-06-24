"""
Tools for parsing reservoir storage summary data, e.g.
http://cdec.water.ca.gov/cgi-progs/reservoirs/STORAGEW.12

"""

import lxml.html
import pandas as pd


def tc(e):
    return e.text_content().strip()


def get_table(url):
    """
    Return HTML table from URL.

    """
    xpath = '//*[@id="main_content"]/div/div[1]/table[1]'
    return lxml.html.parse(url).xpath(xpath)[0]


def parse_fields(row):
    """
    Parse a table header row to get field names.
    Converts years to ints.

    """
    cells = row.getchildren()

    fields = [tc(c) for c in cells[:4]]
    fields.extend(int(tc(c)) for c in cells[4:])

    return fields


def parse_row(row):
    """
    Parse a data row converting numbers to floats.

    """
    cells = row.getchildren()

    data = [tc(cells[0]), int(tc(cells[1]))]
    data.extend(float(tc(c)) for c in cells[2:])

    return data


def table_to_frame(table):
    """
    Turn HTML table of storagew reservoir data into a DataFrame.

    """
    rows = table.getchildren()

    fields = parse_fields(rows[1])
    data = [parse_row(r) for r in rows[3:-4]]

    return pd.DataFrame(data, columns=fields)


def load_storagew(url, year=None, month=None):
    """
    Load STORAGEW data from a URL into a DataFrame.

    Parameters
    ----------
    url : str
        URL of STORAGEW data on CDEC
    year : object, optional
        If provided a "year" column will be added to the data with this value.
    month : any, optional
        If provided a "month" column will be added to the data with this value.

    Returns
    -------
    data : pandas.DataFrame

    """
    df = table_to_frame(get_table(url))

    if year:
        df['year'] = year

    if month:
        df['month'] = month

    return df

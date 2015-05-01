"""
Load PRECIPOUT data even a URL, e.g.
http://cdec.water.ca.gov/cgi-progs/reports/PRECIPOUT

"""

import lxml.html
import pandas as pd

# constants
REGION = 'region'
SUBREGION = 'subregion'
DATAROW = 'datarow'


def get_table(url):
    """
    Return HTML table from URL.

    """
    xpath = '//*[@id="main_content"]/div/div[1]/table'
    return lxml.html.parse(url).xpath(xpath)[0]


def row_type(row):
    """
    Categorize a row.

    """
    cells = row.iterchildren()

    if next(cells).tag == 'th':
        # first cell is a <th> element
        return REGION
    elif next(cells).text_content().strip() == '&nbsp':
        # second cell is empty
        return SUBREGION
    else:
        return DATAROW


def get_region(row):
    """
    Get region name from a REGION row.

    """
    return row.text_content().strip()


def get_subregion(row):
    """
    Parse subregion and month names from SUBREGION row.

    """
    cell_text = [cell.text_content().strip() for cell in row]
    return cell_text[0], cell_text[3:]


def get_elev_abbrev(cell):
    """
    Parse elevation and station abbreviation.

    """
    tc = cell.text_content().strip()
    return int(tc[:-6]), tc[-4:-1]


def get_precip_data(cell):
    """
    Parse a precip data cell.

    """
    tc = [s.strip() for s in cell.itertext()]
    for i, t in enumerate(tc):
        if t in {'---', ''}:
            tc[i] = float('nan')
        elif t.endswith('%'):
            tc[i] = float(t[:-1])
        else:
            tc[i] = float(t)
    return tc


def iter_months(months, cells):
    """
    Iterate over months and month data cells.

    """
    for m, c in zip(months, cells):
        yield m, get_precip_data(c)


def table_to_frame(table):
    """
    Turn HTML table of precip data into a DataFrame.

    """
    datarows = []
    rows = table.iterchildren()

    while True:
        try:
            r = next(rows)
        except StopIteration:
            break

        rt = row_type(r)

        if rt == REGION:
            region = get_region(r)
            next(rows)  # burn the "Station Elev." rows
        elif rt == SUBREGION:
            subregion, months = get_subregion(r)
        elif rt == DATAROW:
            cells = r.iterchildren()

            station = next(cells).text_content().strip()
            elev, abbrev = get_elev_abbrev(next(cells))
            next(cells)  # burn the Precip Average %-avg cell

            for m, values in iter_months(months, cells):
                dr = [region, subregion, station, abbrev, elev, m]
                datarows.append(dr + list(values))

    return pd.DataFrame(datarows, columns=[
        'region', 'subregion', 'station', 'abbreviation', 'elevation',
        'month', 'precip', 'avg precip', 'pct of avg'])


def load_precipout(url, year=None):
    """
    Load PRECIPOUT data from a URL into a DataFrame.

    Parameters
    ----------
    url : str
        URL of a PRECIPOUT table.
    year : int, optional
        If provided a column called 'year' will be added to the
        returned DataFrame containing this value.

    Returns
    -------
    data : pandas.DataFrame

    """
    df = table_to_frame(get_table(url))

    if year:
        df['year'] = year

    return df

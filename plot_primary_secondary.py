import csv
import sys

import matplotlib.pyplot
import numpy

NUM_ARGS = 2
USAGE_STR = 'python plot_primary_secondary.py [projections csv] [output png]'


def parse_row(target):
    year_str = target['scenario'].replace('businessAsUsual', '')
    
    if year_str == '':
        year = 2050
    else:
        year = int(year_str)
    
    return {
        'year': year,
        'primaryProductionMT': float(target['primaryProductionMT']),
        'secondaryProductionMT': float(target['secondaryProductionMT'])
    }


def load_data(source_loc):
    with open(source_loc) as f:
        all_rows = csv.DictReader(f)
        global_rows = filter(lambda x: x['region'] == 'global', all_rows)
        bau_rows = filter(lambda x: x['scenario'].startswith('businessAsUsual'), global_rows)
        rows_parsed = map(parse_row, bau_rows)
        return sorted(rows_parsed, key=lambda x: x['year'])


def main():
    if len(sys.argv) != NUM_ARGS + 1:
        print(USAGE_STR)
        sys.exit(1)
    
    source_loc = sys.argv[1]
    destination_loc = sys.argv[2]

    source_data = load_data(source_loc)

    fig, ax = matplotlib.pyplot.subplots()
    global_floor = numpy.zeros(len(source_data))

    ax.bar(
        [x['year'] for x in source_data],
        [x['secondaryProductionMT'] for x in source_data],
        color='#707070',
        label='Secondary'
    )
    ax.bar(
        [x['year'] for x in source_data],
        [x['primaryProductionMT'] for x in source_data],
        color='#C0C0C0',
        bottom=[x['secondaryProductionMT'] for x in source_data],
        label='Primary'
    )
    
    ax.set_title('BAU Global Primary and Secondary Production')
    ax.set_xlabel('Year')
    ax.set_ylabel('Million Metric Tons')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    ax.legend(loc='upper left')
    
    fig.savefig(destination_loc)


if __name__ == '__main__':
    main()

import csv
import sys

import matplotlib.pyplot
import numpy

NUM_ARGS = 2
USAGE_STR = 'python plot_china_linear_comparison.py [projections csv] [output png]'
RELATIVE = False
FIX_AXIS = True


def parse_row(target):
    return {
        'year': int(target['year']),
        'chinaConsumptionCurve': float(target['chinaConsumptionCurve']),
        'chinaConsumptionML': float(target['chinaConsumptionML']),
        'chinaPopulation': float(target['chinaPopulation'])
    }


def make_relative(targets):
    record_2010 = list(filter(lambda x: x['year'] == 2010, targets))[0]

    def make_relative_inner(target):

        def get_relative(key):
            prior = record_2010[key]
            after = target[key]
            return (after - prior) / prior * 100

        return {
            'year': int(target['year']),
            'chinaConsumptionCurve': get_relative('chinaConsumptionCurve'),
            'chinaConsumptionML': get_relative('chinaConsumptionML'),
            'chinaPopulation': get_relative('chinaPopulation')
        }
    
    return [make_relative_inner(x) for x in targets]


def load_data(source_loc):
    with open(source_loc) as f:
        all_rows = csv.DictReader(f)
        rows_parsed = map(parse_row, all_rows)
        return sorted(rows_parsed, key=lambda x: x['year'])


def main():
    if len(sys.argv) != NUM_ARGS + 1:
        print(USAGE_STR)
        sys.exit(1)
    
    source_loc = sys.argv[1]
    destination_loc = sys.argv[2]

    source_data_abs = load_data(source_loc)
    
    if RELATIVE:
        source_data = make_relative(source_data_abs)
    else:
        source_data = source_data_abs

    fig, ax = matplotlib.pyplot.subplots(nrows=1, ncols=1, figsize=(10, 7))
    fig.subplots_adjust(left=0.2, right=0.8)
    
    china_ax = ax
    china_sub_ax = china_ax.twinx()

    source_data_actual = list(filter(lambda x: x['year'] <= 2021, source_data))
    source_data_project = list(filter(lambda x: x['year'] >= 2021, source_data))

    ml_plot = china_ax.plot(
        [x['year'] for x in source_data_actual],
        [x['chinaConsumptionML'] for x in source_data_actual],
        color='#1f78b4',
        label='Actual Consumption'
    )

    china_ax.plot(
        [x['year'] for x in source_data_project],
        [x['chinaConsumptionML'] for x in source_data_project],
        color='#1f78b4',
        linestyle='dotted',
        label='ML Consumption'
    )

    curve_plot = china_ax.plot(
        [x['year'] for x in source_data_project],
        [x['chinaConsumptionCurve'] for x in source_data_project],
        color='#a6cee3',
        linestyle='dotted',
        label='Polynomial Consumption'
    )

    china_sub_ax.plot(
        [x['year'] for x in source_data_actual],
        [x['chinaPopulation'] for x in source_data_actual],
        color='#33a02c',
        label='Population'
    )

    pop_plot = china_sub_ax.plot(
        [x['year'] for x in source_data_project],
        [x['chinaPopulation'] for x in source_data_project],
        color='#33a02c',
        linestyle='dotted',
        label='Pop Projection'
    )

    if RELATIVE:
        china_ax.set_title('Change in China Consumption & Population from 2010')
        china_ax.set_xlabel('Year')
        china_ax.set_ylabel('% Change Consumption (Polynomial Extrapolation)', color='#1f78b4')
        china_sub_ax.set_ylabel('% Change Population (UN Projections)', color='#33a02c')
    else:
        china_ax.set_title('China Consumption and Population')
        china_ax.set_xlabel('Year')
        china_ax.set_ylabel('Consumption (MMT, Polynomial Extrapolation)', color='#1f78b4')
        china_sub_ax.set_ylabel('Population (Millions, UN Projections)', color='#33a02c')

    if FIX_AXIS:
        if RELATIVE:
            china_ax.set_ylim([-600, 600])
            china_sub_ax.set_ylim([-10, 10])
        else:
            china_ax.set_ylim([0, 600])
            china_sub_ax.set_ylim([0, 1500])

    for label in china_ax.yaxis.get_ticklabels():
        label.set_color('#1f78b4')
    
    for label in china_sub_ax.yaxis.get_ticklabels():
        label.set_color('#33a02c')

    china_ax.yaxis.set_ticks_position('none') 
    china_sub_ax.yaxis.set_ticks_position('none') 

    for ax in [china_ax, china_sub_ax]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
    
    china_ax.legend(loc='center right')
    china_sub_ax.legend(loc='upper left')
    
    fig.savefig(destination_loc)


if __name__ == '__main__':
    main()

import sys

import matplotlib.pyplot
import pandas

NUM_ARGS = 2
USAGE_STR = 'python plot_nafta_polynomial.py [input] [output]'


def main():
    if len(sys.argv) != NUM_ARGS + 1:
        print(USAGE_STR)
        sys.exit(1)
    
    input_loc = sys.argv[1]
    output_loc = sys.argv[2]

    frame_all = pandas.read_csv(input_loc)
    frame = frame_all[frame_all['region'] == 'nafta'].copy().reset_index()
    frame.sort_values('year')

    fig, ax = matplotlib.pyplot.subplots(1, 1, figsize=(10, 7))

    def apply_floor(target):
        return 0 if target < 0 else target

    frame['consumptionAgricultureMT'] = frame['consumptionAgricultureMT'].apply(apply_floor)
    frame['consumptionConstructionMT'] = frame['consumptionConstructionMT'].apply(apply_floor)
    frame['consumptionElectronicMT'] = frame['consumptionElectronicMT'].apply(apply_floor)
    frame['consumptionHouseholdLeisureSportsMT'] = frame['consumptionHouseholdLeisureSportsMT'].apply(apply_floor)
    frame['consumptionPackagingMT'] = frame['consumptionPackagingMT'].apply(apply_floor)
    frame['consumptionTransportationMT'] = frame['consumptionTransportationMT'].apply(apply_floor)
    frame['consumptionTextileMT'] = frame['consumptionTextileMT'].apply(apply_floor)
    frame['consumptionOtherMT'] = frame['consumptionOtherMT'].apply(apply_floor)
    
    ax.plot(
        frame['year'],
        frame['consumptionAgricultureMT'],
        label='Agriculture',
        color='#fdbf6f',
        linestyle='dotted'
    )

    ax.plot(
        frame['year'],
        frame['consumptionConstructionMT'],
        label='Construction',
        color='#1f78b4',
        linestyle='dotted'
    )

    ax.plot(
        frame['year'],
        frame['consumptionElectronicMT'],
        label='Electronic',
        color='#fb9a99'
    )

    ax.plot(
        frame['year'],
        frame['consumptionHouseholdLeisureSportsMT'],
        label='HLS',
        color='#b2df8a',
        linestyle='dotted'
    )

    ax.plot(
        frame['year'],
        frame['consumptionPackagingMT'],
        label='Packaging',
        color='#a6cee3',
        linestyle='dotted'
    )

    ax.plot(
        frame['year'],
        frame['consumptionTransportationMT'],
        label='Transportation',
        color='#e31a1c',
        linestyle='dotted'
    )

    ax.plot(
        frame['year'],
        frame['consumptionTextileMT'],
        label='Textile',
        color='#33a02c',
        linestyle='dotted'
    )

    ax.plot(
        frame['year'],
        frame['consumptionOtherMT'],
        label='Other',
        color='#ff7f00',
        linestyle='dotted'
    )

    ax.legend()

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    ax.set_xlabel('Year')
    ax.set_ylabel('Consumption (MMT)')
    ax.set_title('NAFTA in Polynomial Model')

    fig.savefig(output_loc)


if __name__ == '__main__':
    main()

import sys
import sqlite3

import matplotlib.pyplot
import pandas
import sklearn.linear_model
import sklearn.pipeline

NUM_ARGS = 5
USAGE_STR = 'python plot_out_sample.py [consumption] [waste] [trade] [waste trade] [output img]'


def plot_ml_performance(target, title, max_val, ax, show_legend):
    target.groupby('type')['validOutSampleTarget'].min().sort_values().plot.bar(ax=ax)
    ax.set_title('Out-Sample MAE for ' + title)
    ax.set_xlabel('')
    ax.set_ylabel('MAE (MMT)')
    
    ax.spines[['left', 'right', 'top']].set_visible(False)


def main():
    if len(sys.argv) != NUM_ARGS + 1:
        print(USAGE_STR)
        sys.exit(1)
    
    consumption_loc = sys.argv[1]
    waste_loc = sys.argv[2]
    trade_loc = sys.argv[3]
    waste_trade_loc = sys.argv[4]
    output_loc = sys.argv[5]

    fig, ax = matplotlib.pyplot.subplots(2, 2, figsize=(10, 7))

    fig.tight_layout(h_pad=11, w_pad=4)
    fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)

    plot_ml_performance(
        pandas.read_csv(consumption_loc),
        'Consumption',
        2.75,
        ax[0][0],
        False
    )

    plot_ml_performance(
        pandas.read_csv(waste_loc),
        'Waste',
        0.05,
        ax[0][1],
        True
    )

    plot_ml_performance(
        pandas.read_csv(trade_loc),
        'Goods Trade',
        6,
        ax[1][0],
        False
    )

    plot_ml_performance(
        pandas.read_csv(waste_trade_loc),
        'Waste Trade',
        3,
        ax[1][1],
        False
    )

    fig.savefig(output_loc)


if __name__ == '__main__':
    main()

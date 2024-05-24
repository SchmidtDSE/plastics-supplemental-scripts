import sqlite3
import sys

import matplotlib.pyplot
import pandas
import sklearn.linear_model
import sklearn.pipeline

NUM_ARGS = 5
USAGE_STR = 'python plot_in_sample.py [consumption] [waste] [trade] [waste trade] [output img]'
ML_COLORS = {
    'linear': '#b2df8a',
    'svr': '#fb9a99',
    'tree': '#a6cee3',
    'adaboost': '#1f78b4',
    'random forest': '#33a02c'
}


def plot_ml_performance(target, title, max_val, ax, show_legend):
    type_names = target['type'].unique()
    for type_name in type_names:
        subset = target[target['type'] == type_name]
        ax.scatter(
            subset['trainInSampleTarget'],
            subset['validInSampleTarget'],
            color=ML_COLORS[type_name],
            alpha=0.5
        )
    
    ax.set_xlim([0, max_val])
    ax.set_ylim([0, max_val])
    ax.set_xlabel('In-Sample Training MAE (MMT)')
    ax.set_ylabel('In-Sample Validation MAE (MMT)')
    ax.set_title('Individual Models for ' + title)
    
    ax.spines[['right', 'top']].set_visible(False)
    
    if show_legend:
        ax.legend(type_names)


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

    fig.tight_layout(h_pad=4, w_pad=2)

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

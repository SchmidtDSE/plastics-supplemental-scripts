import csv
import sys

USAGE_STR = 'python find_top_models.py [consumption] [goods trade] [waste] [waste trade] [output]'
NUM_ARGS = 5


def execute_task(task):
    loc = task['loc']
    with open(loc, 'r') as f:
        rows = csv.DictReader(f)
        rf_rows = filter(lambda x: x['type'] == 'random forest', rows)
        min_row = min(rf_rows, key=lambda x: float(x['validOutSampleTarget']))

        test_mae = float(min_row['testOutSampleTarget'])
        test_mae_str = '%.2f' % test_mae
        estimators = int(min_row['estimators'])
        depth = int(min_row['depth'])
        max_features_raw = min_row['max_features']
        max_feature = 'all' if str(max_features_raw) == '1' else max_features_raw

        return {
            'Model': task['name'],
            'Test MAE (MMT)': test_mae_str,
            'Estimators': estimators,
            'Max Depth': depth,
            'Max Features': max_feature
        }


def main():
    if len(sys.argv) != NUM_ARGS + 1:
        print(USAGE_STR)
        sys.exit(1)
    
    tasks = [
        {'name': 'Consumption', 'loc': sys.argv[1]},
        {'name': 'Goods Trade', 'loc': sys.argv[2]},
        {'name': 'Waste', 'loc': sys.argv[3]},
        {'name': 'Waste Trade', 'loc': sys.argv[4]}
    ]

    task_results = map(execute_task, tasks)

    output_loc = sys.argv[5]
    with open(output_loc, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'Model',
            'Test MAE (MMT)',
            'Estimators',
            'Max Depth',
            'Max Features'
        ])
        writer.writeheader()
        writer.writerows(task_results)


if __name__ == '__main__':
    main()

import csv
import json
import sys

USAGE_STR = 'python find_top_models.py [sweep] [output]'
NUM_ARGS = 2


def main():
    if len(sys.argv) != NUM_ARGS + 1:
        print(USAGE_STR)
        sys.exit(1)
    
    input_loc = sys.argv[1]
    output_loc = sys.argv[2]

    with open(input_loc, 'r') as f:
        rows = csv.DictReader(f)
        rf_rows = filter(lambda x: x['algorithm'] == 'random forest', rows)
        min_row = min(rf_rows, key=lambda x: float(x['validationMae']))
    
    with open(output_loc, 'w') as f:
        json.dump(min_row, f)


if __name__ == '__main__':
    main()

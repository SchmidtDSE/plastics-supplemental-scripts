import csv
import json
import random
import statistics
import sys

import sklearn.ensemble
import toolz.itertoolz

USAGE_STR = 'python run_sims.py [config] [data] [num trials] [output] [errorMode]'
NUM_ARGS = 5

OUTPUT_COLS = [
    'trainMae',
    'trainMdae',
    'testMae',
    'testMdae',
    'testMaeChina',
    'testMdaeChina',
    'testMaeEU30',
    'testMdaeEU30',
    'testMaeNAFTA',
    'testMdaeNAFTA',
    'testMaeROW',
    'testMdaeROW'
]
SET_ASSIGNS = ['test', 'train', 'train', 'train', 'train', 'train']


def run_trial(estimators, max_depth, max_features, train_inputs_cols, train_outputs, train_records,
    test_inputs_cols, test_outputs, test_records, eval_func):
    model = sklearn.ensemble.RandomForestRegressor(
        n_estimators=estimators,
        max_depth=max_depth,
        max_features=max_features
    )
    model.fit(train_inputs_cols, train_outputs)

    def evaluate(inputs, outputs, records):
        predictions = model.predict(inputs)
        deltas = map(
            lambda x: eval_func(x[0], x[1], x[2]),
            zip(predictions, outputs, records)
        )
        deltas_realized = list(deltas)
        return {
            'mdae': statistics.median(deltas_realized),
            'mae': statistics.mean(deltas_realized)
        }

    def get_test_sub_eval(inputs, outputs, records, flag):
        paired = zip(inputs, outputs, records)
        allowed_pairs = filter(lambda x: int(x[2][flag]) == 1, paired)
        allowed_inputs, allowed_outputs, allowed_records = zip(*allowed_pairs)
        return evaluate(allowed_inputs, allowed_outputs, allowed_records)

    train_eval = evaluate(
        train_inputs_cols,
        train_outputs,
        train_records
    )
    test_eval = evaluate(
        test_inputs_cols,
        test_outputs,
        test_records
    )

    china_sub_eval = get_test_sub_eval(
        test_inputs_cols,
        test_outputs,
        test_records,
        'flagChina'
    )
    eu30_sub_eval = get_test_sub_eval(
        test_inputs_cols,
        test_outputs,
        test_records,
        'flagEU30'
    )
    nafta_sub_eval = get_test_sub_eval(
        test_inputs_cols,
        test_outputs,
        test_records,
        'flagNafta'
    )
    row_sub_eval = get_test_sub_eval(
        test_inputs_cols,
        test_outputs,
        test_records,
        'flagRow'
    )

    return {
        'trainMae': train_eval['mae'],
        'trainMdae': train_eval['mdae'],
        'testMae': test_eval['mae'],
        'testMdae': test_eval['mdae'],
        'testMaeChina': china_sub_eval['mae'],
        'testMdaeChina': china_sub_eval['mdae'],
        'testMaeEU30': eu30_sub_eval['mae'],
        'testMdaeEU30': eu30_sub_eval['mdae'],
        'testMaeNAFTA': nafta_sub_eval['mae'],
        'testMdaeNAFTA': nafta_sub_eval['mdae'],
        'testMaeROW': row_sub_eval['mae'],
        'testMdaeROW': row_sub_eval['mdae']
    }


def make_split(inputs_cols, outputs, records):
    paired = zip(inputs_cols, outputs, records)
    paired_dict = map(lambda x: {
        'inputs': x[0],
        'output': x[1],
        'record': x[2]
    }, paired)
    labeled = map(lambda x: {
        'label': random.choice(SET_ASSIGNS),
        'inputs': x['inputs'],
        'output': x['output'],
        'record': x['record']
    }, paired_dict)
    
    grouped = toolz.itertoolz.groupby(lambda x: x['label'], labeled)
    
    train_dict = grouped['train']
    test_dict = grouped['test']

    def unnest_from_dict(target):
        tuple_nest = map(
            lambda x: (x['inputs'], x['output'], x['record']),
            target
        )
        tuple_unnest = zip(*tuple_nest)
        return tuple_unnest
    
    train_inputs, train_outputs, train_records = unnest_from_dict(train_dict)
    test_inputs, test_outputs, test_records = unnest_from_dict(test_dict)

    return {
        'trainInputs': train_inputs,
        'trainOutputs': train_outputs,
        'trainRecords': train_records,
        'testInputs': test_inputs,
        'testOutputs': test_outputs,
        'testRecords': test_records
    }


def run_trails(estimators, max_depth, max_features, inputs_cols, outputs, records, num_trials,
    eval_func):
    trail_nums = range(0, num_trials)

    def run_trial_inner():
        split = make_split(inputs_cols, outputs, records)

        train_inputs_cols = split['trainInputs']
        train_outputs = split['trainOutputs']
        train_records = split['trainRecords']
        test_inputs_cols = split['testInputs']
        test_outputs = split['testOutputs']
        test_records = split['testRecords']
        
        return run_trial(
            estimators,
            max_depth,
            max_features,
            train_inputs_cols,
            train_outputs,
            train_records,
            test_inputs_cols,
            test_outputs,
            test_records,
            eval_func
        )

    return map(lambda x: run_trial_inner(), trail_nums)


def get_inputs(targets, input_cols):
    vectors = map(
        lambda record: [record[col] for col in input_cols],
        targets
    )
    return list(vectors)


def simple_error(predicted, actual, record):
    return abs(float(predicted) - float(actual))


def convert_error_mt(predicted, actual, record):
    predicted_target = float(1 + predicted) * float(record['beforeConsumptionMT'])
    actual_target = float(record['afterConsumptionMT'])
    return abs(actual_target - predicted_target)


def main():
    if len(sys.argv) != NUM_ARGS + 1:
        print(USAGE_STR)
        sys.exit(1)

    config_path = sys.argv[1]
    data_path = sys.argv[2]
    num_trials = int(sys.argv[3])
    output_loc = sys.argv[4]
    error_mode = sys.argv[5]

    with open(config_path) as f:
        config = json.load(f)

    with open(data_path) as f:
        input_dicts = list(csv.DictReader(f))

    input_attrs = config['inputs']
    output_attr = config['response']
    estimators = config['estimators']
    max_depth = config['depth']
    max_features = config['maxFeatures']
    
    inputs_cols = get_inputs(input_dicts, input_attrs)
    outputs = [record[output_attr] for record in input_dicts]

    if error_mode == 'mt':
        eval_func = convert_error_mt
    else:
        eval_func = simple_error

    trials = run_trails(
        estimators,
        max_depth,
        max_features,
        inputs_cols,
        outputs,
        input_dicts,
        num_trials,
        eval_func
    )

    with open(output_loc, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_COLS)
        writer.writeheader()
        writer.writerows(trials)


if __name__ == '__main__':
    main()

import sys

NUM_ARGS = 3
USAGE_STR = 'python make_policy_brief_csv.py [scenarios csv] [ghg csv] [output loc]'

INDIVIDUAL_SCENARIOS = [
    'banPsPackaging',
    'banSingleUse',
    'banWasteTrade',
    'capVirgin',
    'minimumPackagingReuse',
    'minimumRecycledContent',
    'minimumRecyclingRate',
    'recyclingInvestment',
    'reducedAdditives',
    'taxVirgin',
    'wasteInvestment'
]

COMBINED_SCENARIOS = ['highAmbition', 'businessAsUsual']

ALLOWED_SCENARIOS = set(INDIVIDUAL_SCENARIOS) + set(COMBINED_SCENARIOS)

REGION = 'global'


def parse_scenario_row(target):
    return {
        'scenario': target['scenario'],
        'region': target['region'],
        'mismanagedMT': float(target['eolMismanagedMT']),
        'primaryMT': float(target['primaryProductionMT']),
        'secondaryMT': float(target['secondaryProductionMT'])
    }


def get_ghg(target):
    return float(target['endGhg'])


def main():
    if len(sys.argv) != NUM_ARGS + 1:
        print(USAGE_STR)
        sys.exit(1)
    
    scenarios_loc = sys.argv[1]
    ghg_loc = sys.argv[2]
    output_loc = sys.argv[3]

    rows_by_scenario = {}

    with open(scenarios_loc) as f:
        scenarios_rows = csv.DictReader(f)
        parsed_rows = map(parse_scenario_row, scenarios_rows)
        global_rows = filter(lambda x: x['region'] == REGION, parsed_rows)
        allowed_rows = filter(lambda x: x['scenario'] in ALLOWED_SCENARIOS, global_rows)

        for row in allowed_rows:
            rows_by_scenario[row['scenario']] = row
    
    with open(ghg_loc) as f:
        ghg_rows = csv.DictReader(f)
        ghg_by_intervention = dict(map(lambda x: (x['intervention'], get_ghg(x)), ghg_rows))
    
    def get_output_row(intervention):
        base_row = rows_by_scenario[intervention]
        ghg = ghg_by_intervention[intervention]
        
        return {
            'scenario': target['scenario'],
            'region': target['region'],
            'mismanagedMT': target['mismanagedMT'],
            'primaryMT': target['primaryMT'],
            'secondaryMT': target['secondaryMT'],
            'ghgMT': ghg
        }
    
    output_rows = map(get_output_row, sorted(ALLOWED_SCENARIOS))

    with open(output_loc, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'scenario',
            'region',
            'mismanagedMT',
            'primaryMT',
            'secondaryMT',
            'ghgMT'
        ])
        writer.writeheader()
        writer.writerows(output_rows)


if __name__ == '__main__':
    main()

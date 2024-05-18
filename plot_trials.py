import csv
import statistics
import sys

import sketchingpy

FONT_SRC = 'workspace/PublicSans-Regular.otf'
USAGE_STR = 'python plot_trials.py [consumption] [waste] [trade] [waste trade] [output]'
NUM_ARGS = 5
REGIONS = ['Global', 'China', 'EU30', 'NAFTA', 'ROW']
TYPES = ['Consumption', 'Waste', 'Trade', 'Waste Trade']
CONSUMPTION_RANGE = [0, 4]
OTHER_RANGE = [0, 4]


def get_type_x(type_name):
    return 620 / len(TYPES) * TYPES.index(type_name) + 50


def get_region_y(region):
    return 500 / len(REGIONS) * REGIONS.index(region) + 70


def get_x(value, type_name):
    is_consumption = type_name == 'Consumption'
    width = 620 / len(TYPES) - 10
    if is_consumption:
        extent = CONSUMPTION_RANGE[1] - CONSUMPTION_RANGE[0]
        return width / extent * (value - CONSUMPTION_RANGE[0])
    else:
        extent = OTHER_RANGE[1] - OTHER_RANGE[0]
        return width / extent * (value - OTHER_RANGE[0]) 


def get_y(percent):
    height = 500 / len(REGIONS) - 10
    return height / 1.1 * (1.1 - percent)


def draw_meta_axis(sketch):
    sketch.push_transform()
    sketch.push_style()

    width = 620 / len(TYPES)

    for type_name in TYPES:
        sketch.set_text_font(FONT_SRC, 14)
        sketch.set_text_align('center', 'bottom')
        sketch.set_fill('#000000')
        sketch.clear_stroke()
        sketch.draw_text(
            get_type_x(type_name) + width / 2 - 5,
            65,
            type_name
        )
        
        sketch.clear_fill()
        sketch.set_stroke('#000000')
        sketch.draw_line(
            get_type_x(type_name),
            65,
            get_type_x(type_name) + width - 5,
            65
        )

        is_consumption = type_name == 'Consumption'

        if is_consumption:
            data_color = '#1f78b4'
            target_range = CONSUMPTION_RANGE
            units = 'MMT'
        else:
            data_color = '#33a02c'
            target_range = OTHER_RANGE
            units = '%'

        sketch.set_text_font(FONT_SRC, 10)
        sketch.set_fill(data_color)
        sketch.clear_stroke()
        
        sketch.set_text_align('left', 'top')
        sketch.draw_text(
            get_type_x(type_name),
            585,
            target_range[0]
        )
        
        sketch.set_text_align('right', 'top')
        sketch.draw_text(
            get_type_x(type_name) + width - 5,
            585,
            target_range[1]
        )

        sketch.set_text_align('center', 'top')
        sketch.draw_text(
            get_type_x(type_name) + width / 2,
            585,
            units
        )

        sketch.clear_fill()
        sketch.set_stroke(data_color)
        sketch.draw_line(
            get_type_x(type_name),
            580,
            get_type_x(type_name) + width - 5,
            580
        )

    sketch.set_fill('#000000')
    sketch.clear_stroke()
    sketch.set_angle_mode('degrees')
    
    for region in REGIONS:
        region_y = get_region_y(region)
        
        sketch.push_transform()

        sketch.translate(30, region_y + 500 / len(REGIONS) * 0.5)
        sketch.rotate(-90)
        sketch.set_text_font(FONT_SRC, 14)
        sketch.set_text_align('center', 'center')
        sketch.set_fill('#000000')
        sketch.clear_stroke()
        sketch.draw_text(0, 0, region)

        sketch.pop_transform()

        sketch.set_text_font(FONT_SRC, 10)
        sketch.set_text_align('left', 'center')
        sketch.set_fill('#909090')
        sketch.clear_stroke()
        sketch.draw_text(677, region_y + get_y(0), '0%')
        sketch.draw_text(677, region_y + get_y(0.9), '100%')

        sketch.clear_fill()
        sketch.set_stroke('#C0C0C0')
        sketch.draw_line(
            673,
            region_y + get_y(0),
            673,
            region_y + get_y(0.9)
        )

    sketch.pop_style()
    sketch.pop_transform()


def draw_summary(sketch, summary, type_name, region):
    sketch.push_transform()
    sketch.push_style()

    sketch.translate(
        get_type_x(type_name),
        get_region_y(region)
    )

    is_consumption = type_name == 'Consumption'

    if is_consumption:
        data_color = '#1f78b4'
    else:
        data_color = '#33a02c'

    sketch.set_rect_mode('corners')
    sketch.set_fill(data_color)
    sketch.clear_stroke()

    for bin_val, percent in summary['percents'].items():
        height = get_y(percent)
        sketch.draw_rect(
            get_x(bin_val, type_name),
            get_y(percent),
            get_x(bin_val, type_name) + 2,
            get_y(0)
        )

    mean_val = summary['mean']
    mean_x = get_x(mean_val, type_name)
    sketch.set_text_font(FONT_SRC, 10)
    sketch.set_text_align('center', 'top')
    sketch.draw_text(mean_x, get_y(0) + 2, 'mean: %.1f' % mean_val)

    sketch.clear_fill()
    sketch.set_stroke('#C0C0C0')
    sketch.draw_line(
        0,
        get_y(0),
        620 / len(TYPES) - 5,
        get_y(0)
    )
    sketch.draw_line(
        0,
        get_y(0),
        0,
        get_y(0) - 3
    )
    sketch.draw_line(
        620 / len(TYPES) - 5,
        get_y(0),
        620 / len(TYPES) - 5,
        get_y(0) - 3
    )


    sketch.pop_style()
    sketch.pop_transform()


def load_summary(sketch, loc, type_name, region):
    is_consumption = type_name == 'Consumption'

    if is_consumption:
        target_range = CONSUMPTION_RANGE
    else:
        target_range = OTHER_RANGE

    records = sketch.get_data_layer().get_csv(loc)
    
    target_min = target_range[0]
    target_max = target_range[1]
    target_bin_size = (target_max - target_min) / 30

    def get_bin(value):
        bin_num = round((value - target_min) / target_bin_size)
        return target_min + bin_num * target_bin_size

    if region == 'Global':
        postfix = ''
    else:
        postfix = region

    values_unshifted = map(
        lambda x: float(x['testMae' + postfix]),
        records
    )

    if is_consumption:
        values = values_unshifted
    else:
        values = map(lambda x: x * 100, values_unshifted)

    values_realized = list(values)

    counts = {}
    for value in values_realized:
        value_bin = get_bin(value)
        counts[value_bin] = counts.get(value_bin, 0) + 1

    total = sum(counts.values())
    percents = dict(map(lambda x: (x[0], x[1] / total), counts.items()))

    return {
        'percents': percents,
        'mean': statistics.mean(values_realized)
    }


def draw_title(sketch):
    sketch.push_transform()
    sketch.push_style()

    sketch.set_text_font(FONT_SRC, 23)
    sketch.set_text_align('center', 'bottom')
    sketch.clear_stroke()
    sketch.set_fill('#000000')
    sketch.draw_text(360, 30, 'MAE in 100 Retraining Trials with New Test Splits')

    sketch.pop_style()
    sketch.pop_transform()


def main():
    if len(sys.argv) != NUM_ARGS + 1:
        print(USAGE_STR)
        sys.exit(1)
    
    consumption_loc = sys.argv[1]
    waste_loc = sys.argv[2]
    trade_loc = sys.argv[3]
    waste_trade_loc = sys.argv[4]
    output_loc = sys.argv[5]

    sketch = sketchingpy.Sketch2DStatic(720, 600)
    sketch.clear('#FFFFFF')
    draw_meta_axis(sketch)

    for region in REGIONS:
        for type_name in TYPES:
            name = {
                'Consumption': 'consumption_sim.csv',
                'Waste': 'waste_sim.csv',
                'Trade': 'trade_sim.csv',
                'Waste Trade': 'waste_trade_sim.csv'
            }[type_name]
            loc = 'workspace/%s' % name
            summary = load_summary(sketch, loc, type_name, region)
            draw_summary(sketch, summary, type_name, region)

    draw_title(sketch)

    sketch.save_image(output_loc)


if __name__ == '__main__':
    main()

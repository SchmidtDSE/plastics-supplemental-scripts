mkdir workspace

echo "== Pulling data =="
wget https://global-plastics-tool.org/datapipeline.zip
unzip datapipeline.zip
mv output upstream_outputs

wget https://global-plastics-tool.org/standalone_tasks/scenarios_overview.csv
mv scenarios_overview.csv upstream_outputs

echo "== Querying database =="
sqlite3 ./upstream_outputs/combined.db < ./sql/instance_consumption_displaced.sql
mv instance_consumption_displaced.csv ./workspace
sqlite3 ./upstream_outputs/combined.db < ./sql/instance_trade_displaced.sql
mv instance_trade_displaced.csv ./workspace
sqlite3 ./upstream_outputs/combined.db < ./sql/instance_waste_displaced.sql
mv instance_waste_displaced.csv ./workspace
sqlite3 ./upstream_outputs/combined.db < ./sql/instance_waste_trade_displaced.sql
mv instance_waste_trade_displaced.csv ./workspace
sqlite3 ./upstream_outputs/combined.db < ./sql/china_population_consumption.sql
mv china_population_consumption.csv ./workspace
sqlite3 ./upstream_outputs/combined.db < ./sql/china_population_consumption_compare.sql
mv china_population_consumption_compare.csv ./workspace

echo "== Getting GHG supplement =="
wget https://global-plastics-tool.org/data/ghg-pipeline.zip
unzip ghg-pipeline.zip
mv deploy upstream_outputs_ghg

echo "== Getting snapshots =="
wget https://global-plastics-tool.org/data/ghg-snapshot.csv
mv ghg-snapshot.csv ./upstream_outputs_ghg/ghg-snapshot.csv

wget https://global-plastics-tool.org/standalone_tasks/scenarios_overview.csv
mv scenarios_overview.csv ./upstream_outputs/scenarios_overview.csv

echo "== Gathering assets =="
wget https://github.com/uswds/public-sans/releases/download/v2.001/public-sans-v2.001.zip
mkdir fonts
mv public-sans-v2.001.zip fonts
cd fonts
unzip public-sans-v2.001.zip
cd ..
mv fonts/fonts/otf/PublicSans-Regular.otf workspace/PublicSans-Regular.otf

echo "== Building output dir =="
mkdir outputs

echo "== Running sims =="
bash run_sims.sh

echo "== Build derivative datasets =="
python find_top_models.py ./upstream_outputs/consumption_sweep.csv ./upstream_outputs/trade_sweep.csv ./upstream_outputs/waste_sweep.csv ./upstream_outputs/wasteTrade_sweep.csv ./outputs/main_performance.csv
python find_top_model_ghg.py ./upstream_outputs_ghg/sweep.csv ./outputs/ghg_model.json
python make_policy_brief_csv.py ./upstream_outputs/scenarios_overview.csv ./upstream_outputs_ghg/ghg-snapshot.csv ./outputs/policy_breif.csv

echo "== Building plots =="
bash make_trial_plot.sh
python plot_primary_secondary.py ./upstream_outputs/scenarios_overview.csv ./outputs/primary_secondary.png
python plot_china_linear.py ./workspace/china_population_consumption.csv ./outputs/china_population_consumption_linear.png
python plot_in_sample.py ./upstream_outputs/consumption_sweep.csv ./upstream_outputs/waste_sweep.csv ./upstream_outputs/trade_sweep.csv ./upstream_outputs/wasteTrade_sweep.csv ./outputs/in_sample.png
python plot_nafta_polynomial.py ./upstream_outputs/overview_curve.csv ./outputs/nafta_polynomial.png
python plot_in_sample.py ./upstream_outputs/consumption_sweep.csv ./upstream_outputs/waste_sweep.csv ./upstream_outputs/trade_sweep.csv ./upstream_outputs/wasteTrade_sweep.csv ./outputs/in_sample.png
python plot_out_sample.py ./upstream_outputs/consumption_sweep.csv ./upstream_outputs/waste_sweep.csv ./upstream_outputs/trade_sweep.csv ./upstream_outputs/wasteTrade_sweep.csv ./outputs/out_sample.png

echo "== Capture direct copy =="
cp ./upstream_outputs_ghg/out_sample_test.txt ./outputs/ghg_out_sample_mae.txt

echo "== Confirm output =="
[ ! -e outputs/trials.png ] && exit 1;
[ ! -e outputs/primary_secondary.png ] && exit 2;
[ ! -e outputs/china_population_consumption_linear.png ] && exit 3;
[ ! -e outputs/in_sample.png ] && exit 4;
[ ! -e outputs/nafta_polynomial.png ] && exit 5;
[ ! -e outputs/in_sample.png ] && exit 6;
[ ! -e outputs/out_sample.png ] && exit 7;
[ ! -e outputs/main_performance.csv ] && exit 8;
[ ! -e outputs/ghg_model.json ] && exit 9;
[ ! -e outputs/ghg_out_sample_mae.txt ] && exit 10;
echo "Output OK"

echo "== Preparing output =="
zip -r outputs.zip outputs

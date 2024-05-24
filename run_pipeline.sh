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

echo "== Building plots =="
bash make_trial_plot.sh
python plot_primary_secondary.py ./upstream_outputs/scenarios_overview.csv ./outputs/primary_secondary.png
python plot_china_linear.py ./workspace/china_population_consumption.csv ./outputs/china_population_consumption_linear.png
python plot_in_sample.py ./upstream_outputs/consumption_sweep.csv ./upstream_outputs/waste_sweep.csv ./upstream_outputs/trade_sweep.csv ./upstream_outputs/wasteTrade_sweep.csv ./outputs/in_sample.png

echo "== Confirm output =="
[ ! -e outputs/trials.png ] && exit 1;
[ ! -e outputs/primary_secondary.png ] && exit 2;
[ ! -e outputs/china_population_consumption_linear.png ] && exit 3;
[ ! -e outputs/in_sample.png ] && exit 4;
echo "Output OK"

echo "== Preparing output =="
zip -r outputs.zip outputs

mkdir workspace

echo "== Pulling data =="
wget https://global-plastics-tool.org/datapipeline.zip
unzip datapipeline.zip
mv output upstream_outputs

echo "== Querying database =="
sqlite3 ./upstream_outputs/combined.db < ./sql/instance_consumption_displaced.sql
mv instance_consumption_displaced.csv ./workspace
sqlite3 ./upstream_outputs/combined.db < ./sql/instance_trade_displaced.sql
mv instance_trade_displaced.csv ./workspace
sqlite3 ./upstream_outputs/combined.db < ./sql/instance_waste_displaced.sql
mv instance_waste_displaced.csv ./workspace
sqlite3 ./upstream_outputs/combined.db < ./sql/instance_waste_trade_displaced.sql
mv instance_waste_trade_displaced.csv ./workspace

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

echo "== Confirm output =="
[ ! -e outputs/trials.png ] && exit 1;
echo "Output OK"

echo "== Preparing output =="
zip -r outputs.zip outputs

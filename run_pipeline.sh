mkdir workspace
mkdir outputs

echo "== Pulling data =="
wget https://global-plastics-tool.org/datapipeline.zip
unzip https://global-plastics-tool.org/datapipeline.zip

echo "== Querying database =="

echo "== Running sims =="
bash run_sims.sh

echo "== Building plots =="
bash make_trial_plot.sh

echo "== Preparing output =="
zip -r outputs.zip outputs

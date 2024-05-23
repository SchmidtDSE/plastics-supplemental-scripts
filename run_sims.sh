python3 run_sims.py ./config/consumption_config.json ./workspace/instance_consumption_displaced.csv 100 ./workspace/consumption_sim.csv mt
python3 run_sims.py ./config/trade_config.json ./workspace/instance_trade_displaced.csv 100 ./workspace/trade_sim.csv percent
python3 run_sims.py ./config/waste_trade_config.json ./workspace/instance_waste_trade_displaced.csv 100 ./workspace/waste_trade_sim.csv percent
python3 run_sims.py ./config/waste_config.json ./workspace/instance_waste_displaced.csv 100 ./workspace/waste_sim.csv percent

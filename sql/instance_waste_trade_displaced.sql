.headers on
.mode csv
.output instance_waste_trade_displaced.csv
SELECT
    years,
    popChange,
    gdpChange,
    afterGdp,
    afterPopulation,
    beforePercent,
    afterPercent,
    flagChina,
    flagEU30,
    flagNafta,
    flagRow,
    flagSword,
    beforeYear,
    afterYear,
    afterTotalConsumption,
    beforeTotalConsumption
FROM
    instance_waste_trade_displaced
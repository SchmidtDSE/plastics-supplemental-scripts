.mode csv
.output instance_trade_displaced.csv
SELECT
    years,
    popChange,
    gdpChange,
    afterGdp,
    afterPopulation,
    flagChina,
    flagEU30,
    flagNafta,
    flagRow,
    flagArticles,
    flagFibers,
    flagGoods,
    flagResin,
    beforePercent,
    afterPercent,
    beforeYear,
    afterYear,
    beforeTotalConsumption,
    afterTotalConsumption
FROM
    instance_trade_displaced
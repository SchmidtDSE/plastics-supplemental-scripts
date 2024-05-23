.headers on
.mode csv
.output instance_waste_displaced.csv
SELECT
    years,
    popChange,
    gdpChange,
    afterGdp,
    afterPopulation,
    beforePercent,
    flagChina,
    flagEU30,
    flagNafta,
    flagRow,
    flagRecycling,
    flagIncineration,
    flagLandfill,
    flagMismanaged,
    afterPercent,
    beforeYear,
    afterYear
FROM
    instance_waste_displaced
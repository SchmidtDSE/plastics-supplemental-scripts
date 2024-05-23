.headers on
.mode csv
.output instance_consumption_displaced.csv
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
    flagAgriculture,
    flagConstruction,
    flagElectronic,
    flagHouseholdLeisureSports,
    flagOther,
    flagPackaging,
    flagTextile,
    flagTransportation,
    consumptionChange,
    beforeConsumptionMT,
    afterConsumptionMT,
    beforeYear,
    afterYear
FROM
    instance_consumption_displaced
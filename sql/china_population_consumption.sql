.headers on
.mode csv
.output china_population_consumption.csv
SELECT
	consumption_summary.year AS year,
	consumption_summary.totalConsumption AS totalConsumption,
	consumption_summary.chinaConsumption AS chinaConsumption,
	population_summary.totalPopulation AS totalPopulation,
	population_summary.chinaPopulation AS chinaPopulation
FROM
	(
		SELECT
			year,
			sum(
				consumptionAgricultureMT +
				consumptionConstructionMT +
				consumptionElectronicMT +
				consumptionHouseholdLeisureSportsMT +
				consumptionOtherMT +
				consumptionPackagingMT +
				consumptionTextileMT +
				consumptionTransportationMT
			) AS totalConsumption,
			sum(
				(
					consumptionAgricultureMT +
					consumptionConstructionMT +
					consumptionElectronicMT +
					consumptionHouseholdLeisureSportsMT +
					consumptionOtherMT +
					consumptionPackagingMT +
					consumptionTextileMT +
					consumptionTransportationMT
				) * (
					CASE
						WHEN region = 'china' THEN 1
						ELSE 0
					END
				)
			) AS chinaConsumption
		FROM
			project_curve
		WHERE
			year >= 2000
		GROUP BY
			year
	) consumption_summary
INNER JOIN
	(
		SELECT
			year,
			sum(
				population
			) AS totalPopulation,
			sum(
				(
					population
				) * (
					CASE
						WHEN region = 'china' THEN 1
						ELSE 0
					END
				)
			) AS chinaPopulation
		FROM
			population
		WHERE
			year >= 2000
		GROUP BY
			year
	) population_summary
ON
	consumption_summary.year = population_summary.year

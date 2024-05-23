.headers on
.mode csv
.output china_population_consumption_compare.csv
SELECT
	before_ml.year AS year,
	before_ml.chinaConsumption AS chinaConsumptionCurve,
	ml_summary.chinaConsumption AS chinaConsumptionML,
	before_ml.chinaPopulation AS chinaPopulation
FROM
	(
		SELECT
			consumption_summary_curve.year AS year,
			consumption_summary_curve.chinaConsumption AS chinaConsumption,
			population_summary.chinaPopulation AS chinaPopulation
		FROM
			(
				SELECT
					year,
					sum(
						(
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
			) consumption_summary_curve
		INNER JOIN
			(
				SELECT
					year,
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
			consumption_summary_curve.year = population_summary.year
	) before_ml
INNER JOIN
	(
		SELECT
			year,
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
			project_ml
		WHERE
			year >= 2000
		GROUP BY
			year
	) ml_summary
ON
	ml_summary.year = before_ml.year
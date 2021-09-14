-- SQL ProcBench Scalar UDF 05: "Morning to Evening Ratio"

WITH t(depCount) AS (
  SELECT DISTINCT cd_dep_count FROM customer_demographics
) SELECT t.depCount, dbo.morningToEveRatio(t.depCount) FROM t;

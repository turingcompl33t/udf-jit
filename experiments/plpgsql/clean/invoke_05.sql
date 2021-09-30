-- SQL ProcBench Scalar UDF 05: "Morning to Evening Ratio"
--
-- Modifications: Original version uses a subquery to select 
-- distinct values of cd_dep_count from customer_demographics.
-- I rewrote this to use a CTE to emulate the functionality.
-- This still results in an error during code generation, so 
-- the current version does not merely select unique values.

WITH t(dep) AS (SELECT DISTINCT cd_dep_count FROM customer_demographics) SELECT dep, morningToEveRatio(dep) FROM t;

-- SQL ProcBench Scalar UDF 05: "Morning to Evening Ratio"
--
-- Modifications: Original version uses a subquery to select 
-- distinct values of cd_dep_count from customer_demographics.
-- I rewrote this to use a CTE to emulate the functionality.
-- This still results in an error during code generation, so 
-- the current version does not merely select unique values.
--
-- The original invoking query proved WAY too slow (even with
-- scale factor 1 @ 1% it did not complete all night...) so I
-- re-introduced the CTE with a limit to limit the number of
-- rows over which the UDF is invoked.

WITH t(dep) AS (SELECT cd_dep_count FROM customer_demographics LIMIT 10) SELECT dep, morningToEveRatio(dep) FROM t;

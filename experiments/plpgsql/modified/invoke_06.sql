-- SQL ProcBench Scalar UDF 06: "Total Discount"
--
-- Modifications: The original version of this invoking query
-- used a SELECT DISTINCT. It appears that this feature is not
-- fully supported in NoisePage, so I removed it.
--
-- In place of SELECT DISTINCT I inserted a LIMIT to limit the
-- number of rows over which the UDF is invoked.

WITH t(manufacturer_id) AS (SELECT i_manufact_id FROM item LIMIT 10) SELECT manufacturer_id, totalDiscount(manufacturer_id) FROM t;

-- SQL ProcBench Scalar UDF 06: "Total Discount"
--
-- Modifications: The original version of this invoking query
-- used a SELECT DISTINCT. It appears that this feature is not
-- fully supported in NoisePage, so I removed it.

SELECT i_manufact_id, totalDiscount(i_manufact_id) FROM item;

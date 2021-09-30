-- SQL ProcBench Scalar UDF 13: "Max Purchase Channel"
--
-- Modifications: Introduced CTE with LIMIT to limit
-- the number of rows over which the UDF is invoked.

SELECT c_customer_sk, maxPurchaseChannel(c_customer_sk, 2000, 2020) FROM customer;

-- SQL ProcBench Scalar UDF 13: "Max Purchase Channel"

WITH t(customer_id) AS (SELECT c_customer_sk FROM customer LIMIT 10) SELECT customer_id, maxPurchaseChannel(customer_id, 2000, 2020) FROM t;

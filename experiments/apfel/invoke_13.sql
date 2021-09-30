-- SQL ProcBench Scalar UDF 13: "Max Purchase Channel"

SELECT c_customer_sk, maxPurchaseChannel(c_customer_sk, 2000, 2020) FROM customer;

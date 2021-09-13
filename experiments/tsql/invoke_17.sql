-- SQL ProcBench Scalar UDF 17: "Preferred Channel WRT Count"

SELECT c_customer_sk, dbo.preferredChannel(c_customer_sk) FROM customer

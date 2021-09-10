-- SQL ProcBench Scalar UDF 18: "Preferred Channel WRT Expenditure"

SELECT c_customer_sk, dbo.preferredChannel_wrtExpenditure(c_customer_sk) FROM customer

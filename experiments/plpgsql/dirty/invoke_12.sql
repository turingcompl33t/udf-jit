-- SQL ProcBench Scalar UDF 12: "Increase in Web Spending"
--
-- TODO: Can NoisePage handle this subquery?
-- TODO: Can NoisePage handle INTERECT?

SELECT c_customer_sk, increaseInWebSpending(c_customer_sk) 
FROM customer
WHERE c_customer_sk IN
	(SELECT ws_bill_customer_sk
	FROM web_sales_history, date_dim
	WHERE d_date_sk = ws_sold_date_sk
	    AND d_year = 2000

	INTERSECT

	SELECT ws_bill_customer_sk
	FROM web_sales_history, date_dim
	WHERE d_date_sk = ws_sold_date_sk
		AND d_year = 2001
	)
	AND increaseInWebSpending(c_customer_sk) > 0;

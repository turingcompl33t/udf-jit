-- SQL ProcBench Scalar UDF 12: "Increase in Web Spending"

SELECT t.ws_bill_customer_sk
FROM 
	(SELECT ws_bill_customer_sk
	FROM web_sales_history, date_dim
	WHERE d_date_sk = ws_sold_date_sk
		AND d_year = 2000 AND d_moy = 1 AND ws_bill_customer_sk IS NOT NULL

	INTERSECT

	SELECT ws_bill_customer_sk
	FROM web_sales_history, date_dim
	WHERE d_date_sk = ws_sold_date_sk
	    AND d_year = 2001 AND d_moy = 1 AND ws_bill_customer_sk IS NOT NULL
	)
WHERE dbo.increaseInWebSpending(t.ws_bill_customer_sk) > 0;

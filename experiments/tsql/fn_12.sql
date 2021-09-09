-- SQL ProcBench Scalar UDF 12: "Increase in Web Spending"

CREATE OR ALTER FUNCTION increaseInWebSpending(@cust_sk INT) RETURNS DECIMAL(15, 2) AS
BEGIN
	DECLARE @spending1  DECIMAL(15, 2) = 0;
	DECLARE @spending2  DECIMAL(15, 2) = 0;
	DECLARE @increase  DECIMAL(15, 2) = 0;
	SET @spending1 = (SELECT sum(ws_net_paid_inc_ship_tax) 
						FROM web_sales_history, date_dim
						WHERE d_date_sk = ws_sold_date_sk
							AND d_year = 2001
							AND ws_bill_customer_sk = @cust_sk);
	SET @spending2 = (SELECT sum(ws_net_paid_inc_ship_tax) 
						FROM web_sales_history, date_dim
						WHERE d_date_sk = ws_sold_date_sk
							AND d_year = 2000
							AND ws_bill_customer_sk = @cust_sk);
	-- TODO: Can Froid handle this multiple-return?
    IF (@spending1 < @spending2)
		RETURN -1;
	ELSE
		SET @increase = @spending1-@spending2;
	RETURN @increase;
END

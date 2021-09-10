-- SQL ProcBench Scalar UDF 18: "Preferred Channel WRT Expenditure"

CREATE OR ALTER FUNCTION preferredChannel_wrtExpenditure(@cust_key INT) RETURNS VARCHAR(50) AS
BEGIN
	DECLARE @numWeb DECIMAL(15, 2) = 0;
	DECLARE @numStore DECIMAL(15, 2) = 0;
	DECLARE @numCat DECIMAL(15, 2) = 0;

	IF EXISTS (SELECT * FROM web_sales_history WHERE ws_bill_customer_sk = @cust_key)
		SET @numWeb = (SELECT SUM(ws_net_paid_inc_ship_tax) FROM web_sales_history WHERE ws_bill_customer_sk = @cust_key);
	
    IF EXISTS (SELECT * FROM store_sales_history WHERE ss_customer_sk = @cust_key)
		SET @numStore = (SELECT SUM(ss_net_paid_inc_tax) FROM store_sales_history WHERE ss_customer_sk = @cust_key);
	
    IF EXISTS (SELECT * FROM catalog_sales_history WHERE cs_bill_customer_sk = @cust_key)
		SET @numCat = (SELECT SUM(cs_net_paid_inc_ship_tax) FROM catalog_sales_history WHERE cs_bill_customer_sk = @cust_key);
	
    IF (@numWeb >= @numStore AND @numWeb >= @numCat)
		RETURN 'web';
	IF (@numStore >= @numWeb AND @numStore >= @numCat)
		RETURN 'store';
	IF (@numCat >= @numStore AND @numCat >= @numWeb)
		RETURN 'Catalog';
	RETURN 'Logical error';
END

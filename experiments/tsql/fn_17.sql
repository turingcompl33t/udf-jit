-- SQL ProcBench Scalar UDF 17: "Preferred Channel WRT Count"

CREATE OR ALTER FUNCTION preferredChannel_wrtCount(@cust_key INT) RETURNS VARCHAR(50) AS
BEGIN
	DECLARE @numWeb INT = 0;
	DECLARE @numStore INT = 0;
	DECLARE @numCat INT = 0;
	SET @numWeb = (SELECT COUNT(*) FROM web_sales_history WHERE ws_bill_customer_sk=@cust_key);
	SET @numStore = (SELECT COUNT(*) FROM store_sales_history WHERE ss_customer_sk=@cust_key);
	SET @numCat = (SELECT COUNT(*) FROM catalog_sales_history WHERE cs_bill_customer_sk=@cust_key);
	IF (@numWeb >= @numStore AND @numWeb >= @numCat)
		RETURN 'web';
	IF (@numStore >= @numWeb AND @numStore >= @numCat)
		RETURN 'store';
	IF (@numCat >= @numStore AND @numCat >= @numWeb)
		RETURN 'Catalog';
	RETURN 'Logical error';
END

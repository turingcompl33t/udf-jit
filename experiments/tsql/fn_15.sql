-- SQL ProcBench Scalar UDF 15: "Income Band of Max Buy Customer"

CREATE OR ALTER FUNCTION incomeBandOfMaxBuyCustomer(@storeNumber INT) RETURNS VARCHAR(50) AS 
BEGIN 
	DECLARE @incomeband INT;
	DECLARE @cust INT;
	DECLARE @hhdemo INT;
	DECLARE @cnt INT;
	DECLARE @cLevel VARCHAR(50);
	SELECT @cust = ss_customer_sk, @hhdemo = c_current_hdemo_sk, @cnt = COUNT(*)
	FROM store_sales_history, customer
	WHERE ss_store_sk = 1
		AND c_customer_sk = ss_customer_sk
	GROUP BY ss_customer_sk, c_current_hdemo_sk
	HAVING COUNT(*) =(SELECT MAX(cnt) FROM 
			(SELECT ss_customer_sk, c_current_hdemo_sk, COUNT(*) AS cnt
			FROM store_sales_history, customer
			WHERE ss_store_sk = 1
			AND c_customer_sk = ss_customer_sk GROUP BY ss_customer_sk, c_current_hdemo_sk HAVING ss_customer_sk IS NOT NULL) tbl)

	SET @incomeband = (SELECT hd_income_band_sk FROM household_demographics WHERE hd_demo_sk = @hhdemo);

	IF (@incomeband >= 0 AND @incomeband <= 3)
		SET @cLevel = 'low';
	IF (@incomeband >= 4 AND @incomeband <= 7)
		SET @cLevel = 'lowerMiddle';
	IF (@incomeband >= 8 AND @incomeband <= 11)
		SET @cLevel = 'upperMiddle';
	IF (@incomeband >= 12 AND @incomeband <= 16)
		SET @cLevel = 'high';
	IF (@incomeband >= 17 AND @incomeband <= 20)
		SET @cLevel = 'affluent';
	
	RETURN @cLevel;
END

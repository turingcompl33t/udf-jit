-- SQL ProcBench Scalar UDF 15: "Income Band of Max Buy Customer"
--
-- TODO: Can NoisePage handle this subquery?

CREATE OR REPLACE FUNCTION incomeBandOfMaxBuyCustomer(storeNumber INT) RETURNS VARCHAR(50) AS $$
DECLARE
    incomeband INT;
	cust INT;
	hhdemo INT;
	cntVar INT;
	cLevel varchar(50);
BEGIN 
	SELECT ss_customer_sk , c_current_hdemo_sk , COUNT(*) 
    INTO cust, hhdemo, cntVar
	FROM store_sales_history, customer
	WHERE ss_store_sk = 1 and c_customer_sk=ss_customer_sk
    GROUP BY ss_customer_sk, c_current_hdemo_sk
	HAVING COUNT(*) =(SELECT MAX(cnt) FROM 
			(SELECT ss_customer_sk, c_current_hdemo_sk, COUNT(*) AS cnt
			FROM store_sales_history, customer
			WHERE ss_store_sk = 1
			AND c_customer_sk=ss_customer_sk GROUP BY ss_customer_sk, c_current_hdemo_sk HAVING ss_customer_sk IS NOT NULL ) tbl);
    
    SELECT hd_income_band_sk INTO incomeband FROM household_demographics WHERE hd_demo_sk = hhdemo;

	IF (incomeband >= 0 AND incomeband <= 3) THEN
		 cLevel := 'low';
    END IF;
    IF (incomeband >= 4 AND incomeband <= 7) THEN
		 cLevel := 'lowerMiddle';
	END IF;
    IF (incomeband >= 8 AND incomeband <= 11) THEN
		 cLevel := 'upperMiddle';
	END IF;
    IF (incomeband >= 12 AND incomeband <= 16) THEN
		 cLevel := 'high';
	END IF;
    IF (incomeband >= 17 AND incomeband <= 20) THEN
		 cLevel := 'affluent';
	END IF;
	RETURN cLevel;
END;
$$ LANGUAGE PLPGSQL;

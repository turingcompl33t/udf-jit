-- SQL ProcBench Scalar UDF 17: "Preferred Channel WRT Count"

CREATE OR REPLACE FUNCTION preferredChannel_wrtCount(cust_key INT) RETURNS VARCHAR(50) AS $$
DECLARE
    numWeb INT;
    numStore INT;
    numCat INT;
BEGIN
	numWeb := 0;
	numStore := 0;
	numCat := 0;
	SELECT COUNT(*) INTO numWeb FROM web_sales_history WHERE ws_bill_customer_sk = cust_key;
	SELECT COUNT(*) INTO numStore FROM store_sales_history WHERE ss_customer_sk = cust_key;
	SELECT COUNT(*) INTO numCat FROM catalog_sales_history WHERE cs_bill_customer_sk = cust_key;
	IF (numWeb >= numStore and numWeb >= numCat) THEN
		RETURN 'web';
    END IF;
	IF (numStore >= numWeb and numStore >= numCat) THEN
		RETURN 'store';
    END IF;
	IF (numCat >= numStore and numCat >= numWeb) THEN
		RETURN 'Catalog';
    END IF;
	RETURN 'Logical error';
END;
$$ LANGUAGE PLPGSQL;

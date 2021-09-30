-- SQL ProcBench Scalar UDF 18: "Preferred Channel WRT Expenditure"

CREATE OR REPLACE FUNCTION preferredChannel_wrtExpenditure(cust_key INT) RETURNS VARCHAR(50) AS $$
DECLARE
	numWeb FLOAT8;
	numStore FLOAT8;
	numCat FLOAT8;
BEGIN 
	numWeb := 0;
    numStore := 0; 
    numCat := 0;
	IF EXISTS (SELECT * FROM web_sales_history WHERE ws_bill_customer_sk = cust_key) THEN
		numWeb := (SELECT SUM(ws_net_paid_inc_ship_tax) FROM web_sales_history WHERE ws_bill_customer_sk = cust_key);
	END IF;
	
    IF EXISTS (SELECT * FROM store_sales_history WHERE ss_customer_sk=cust_key) THEN
		numStore := (SELECT SUM(ss_net_paid_inc_tax) FROM store_sales_history WHERE  ss_customer_sk=cust_key);
	END IF;
	
    IF EXISTS (SELECT * FROM catalog_sales_history WHERE cs_bill_customer_sk=cust_key) THEN
		numCat := (SELECT SUM(cs_net_paid_inc_ship_tax) FROM catalog_sales_history WHERE  cs_bill_customer_sk=cust_key);
	END IF;
	
    IF (numWeb >= numStore AND numWeb >= numCat) THEN
		RETURN 'web';
	END IF;
	IF (numStore >= numWeb AND numStore >= numCat) THEN
		RETURN 'store';
	END IF;
	IF (numCat >= numStore AND numCat >= numWeb) THEN
		RETURN 'Catalog';
	END IF;
	RETURN 'Logical error';
END; 
$$ LANGUAGE PLPGSQL;

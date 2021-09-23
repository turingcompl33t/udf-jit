-- SQL ProcBench Scalar UDF 06: "Total Discount"

CREATE OR REPLACE FUNCTION totalDiscount(manufacture_id INT) RETURNS FLOAT8 AS $$
DECLARE
    average FLOAT8;
    addition FLOAT8;
BEGIN
	SELECT AVG(ws_ext_discount_amt) INTO average FROM web_sales_history, item 
				WHERE ws_item_sk = i_item_sk AND i_manufact_id = manufacture_id;

	SELECT SUM(ws_ext_discount_amt) INTO addition FROM web_sales_history, item 
				WHERE ws_item_sk = i_item_sk AND i_manufact_id = manufacture_id AND
				ws_ext_discount_amt>1.3*average;
	RETURN addition;	
END;
$$ LANGUAGE PLPGSQL;

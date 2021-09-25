-- SQL ProcBench Scalar UDF 06: "Total Discount"
--
-- Modifications: The original version of this function
-- used "> 1.3 * average" as the final JOIN condition of
-- the second query. In NoisePage, this condition causes
-- optimization of the second embedded query to fail.

CREATE OR REPLACE FUNCTION totalDiscount(manufacture_id INT) RETURNS DECIMAL AS $$
DECLARE
    average DECIMAL;
    addition DECIMAL;
BEGIN
	SELECT AVG(ws_ext_discount_amt) INTO average FROM web_sales_history, item 
				WHERE ws_item_sk = i_item_sk 
				AND i_manufact_id = manufacture_id;

	SELECT SUM(ws_ext_discount_amt) INTO addition FROM web_sales_history, item 
				WHERE ws_item_sk = i_item_sk 
				AND i_manufact_id = manufacture_id
				AND ws_ext_discount_amt > average;
	RETURN addition;
END;
$$ LANGUAGE PLPGSQL;

-- SQL ProcBench Scalar UDF 06: "Total Discount"

CREATE OR ALTER FUNCTION totalDiscount(@manufacture_id INT) RETURNS DECIMAL(15, 2) AS
BEGIN
	DECLARE @avg DECIMAL(15,2);
	DECLARE @s DECIMAL(15, 2);
	SET @avg = (SELECT avg(ws_ext_discount_amt) FROM web_sales_history, item 
				WHERE ws_item_sk = i_item_sk AND i_manufact_id = @manufacture_id);

	SET @s = (SELECT sum(ws_ext_discount_amt) FROM web_sales_history, item 
					WHERE ws_item_sk = i_item_sk AND i_manufact_id = @manufacture_id AND
					ws_ext_discount_amt>1.3*@avg);
	return @s;	
END

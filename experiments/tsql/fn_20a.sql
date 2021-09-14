-- SQL ProcBench Scalar UDF 20a: "Get Manufacturer Simple"

CREATE OR ALTER FUNCTION getManufact_simple(@item INT) RETURNS CHAR(50) AS
BEGIN
	RETURN (SELECT i_manufact FROM item WHERE i_item_sk = @item)
END

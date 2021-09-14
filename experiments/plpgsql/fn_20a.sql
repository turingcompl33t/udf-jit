-- SQL ProcBench Scalar UDF 20a: "Get Manufacturer Simple"

CREATE OR REPLACE FUNCTION getManufact_simple(itm INT) RETURNS CHAR(50) AS
$$
BEGIN
	RETURN (SELECT i_manufact FROM item WHERE i_item_sk = itm);
END; 
$$ LANGUAGE PLPGSQL;

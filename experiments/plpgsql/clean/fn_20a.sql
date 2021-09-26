-- SQL ProcBench Scalar UDF 20a: "Get Manufacturer Simple"
--
-- Modifications: Replaced use of CHAR with VARCHAR.

CREATE OR REPLACE FUNCTION getManufact_simple(itm INT) RETURNS VARCHAR AS $$
DECLARE
	r VARCHAR;
BEGIN
	r = (SELECT i_manufact FROM item WHERE i_item_sk = itm);
	RETURN r;
END; 
$$ LANGUAGE PLPGSQL;

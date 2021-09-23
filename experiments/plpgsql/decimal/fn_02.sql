-- SQL ProcBench Scalar UDF 02: "Max Promo Channel"

CREATE OR REPLACE FUNCTION maxPromoChannel(year INT) RETURNS VARCHAR AS $$
DECLARE
BEGIN	
  RETURN promoVsNoPromoItems(year);
END;
$$ LANGUAGE PLPGSQL;

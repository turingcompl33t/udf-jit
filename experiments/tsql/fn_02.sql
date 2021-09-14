-- SQL ProcBench Scalar UDF 02: "Max Promo Channel"

CREATE OR ALTER FUNCTION maxPromoChannel(@year INT) RETURNS VARCHAR(20) AS
BEGIN
	RETURN dbo.promoVsNoPromoItems(@year);
END

-- SQL ProcBench Scalar UDF 04: "Generate Random Integer"
-- 
-- Modifications: We can't do CAST(), so we have no
-- way to turn the REAL returned by FLOOR into an INT.

CREATE OR REPLACE FUNCTION genRandomInt(lower INT, upper INT, rand FLOAT) RETURNS INT AS $$
DECLARE
    result INT;
BEGIN
  result := (SELECT 1);
  RETURN result;
END; 
$$ LANGUAGE PLPGSQL;

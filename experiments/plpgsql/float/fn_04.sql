-- SQL ProcBench Scalar UDF 04: "Generate Random Integer"

CREATE OR REPLACE FUNCTION genRandomInt(lower INT, upper INT, rand FLOAT) RETURNS INT AS $$
declare
    result INT;
    range INT;
BEGIN
  range := upper - lower + 1;
  result := FLOOR(rand * range + lower);
  RETURN result;
END; 
$$ LANGUAGE PLPGSQL;

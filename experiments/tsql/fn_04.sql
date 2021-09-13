-- SQL ProcBench Scalar UDF 04: "Generate Random Integer"

CREATE FUNCTION genRandomInt(@lower INT, @upper INT, @rand FLOAT) RETURNS INT AS
BEGIN
  DECLARE @result INT;
  DECLARE @range int = @upper - @lower + 1;
  SET @result = FLOOR(@rand * @range + @lower);
  RETURN @result;
END

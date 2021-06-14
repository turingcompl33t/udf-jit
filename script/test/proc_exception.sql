-- EXCEPTION block
CREATE FUNCTION test() LANGUAGE plpgsql AS $$
DECLARE
  x INT := 0;
  y INT := 1;
  z INT := 0;
BEGIN
  z := y / x;
EXCEPTION
  WHEN division_by_zero THEN
    RAISE NOTICE 'caught division by zero';
END;
$$
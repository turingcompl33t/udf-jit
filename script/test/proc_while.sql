-- WHILE-loop control flow
CREATE FUNCTION test() LANGUAGE plpgsql AS $$
DECLARE
  x INT := 0;
BEGIN
  WHILE x < 10 LOOP
    x = x + 1;
  END LOOP;
END;
$$
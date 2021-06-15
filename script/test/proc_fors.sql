-- FOR-loop control flow (query)
CREATE FUNCTION test() RETURNS INT LANGUAGE plpgsql AS $$
DECLARE
  r RECORD;
  x INT := 0;
BEGIN
  FOR r IN SELECT * FROM TestTable
  LOOP
    x = x + 1;
  END LOOP;
  RETURN x;
END;
$$
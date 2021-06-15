-- FOR-loop control flow
CREATE FUNCTION test() LANGUAGE plpsql AS $$
DECLARE
  x INT := 0;
BEGIN
  FOR i IN 1..10 LOOP
    x = x + 1;
  END LOOP;
END;
$$
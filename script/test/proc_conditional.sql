-- conditional control flow
CREATE FUNCTION test(x INT) RETURNS INT LANGUAGE plpgsql AS $$
BEGIN
  IF x < 10 THEN
    RETURN 1;
  ELSE
    RETURN 2;
  END IF;
END;
$$
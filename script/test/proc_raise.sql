-- RAISE statement
CREATE FUNCTION test() LANGUAGE plpgsql AS $$
BEGIN
  RAISE NOTICE 'Hello, World!';
  RETURN 1;
END;
$$
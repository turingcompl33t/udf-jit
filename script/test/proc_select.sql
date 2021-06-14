-- SELECT query
CREATE FUNCTION test() LANGUAGE plpgsql AS $$
BEGIN
  SELECT * FROM TestTable;
END;
$$
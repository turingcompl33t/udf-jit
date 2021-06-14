-- DELETE query
CREATE FUNCTION test() LANGUAGE plpgsql AS $$
BEGIN
  DELETE FROM TestTable;
END;
$$
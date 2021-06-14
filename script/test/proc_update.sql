-- UPDATE query
CREATE FUNCTION test() LANGUAGE plpgsql AS $$
BEGIN
  UPDATE TestTable SET hello = "World" WHERE id = 0;
END;
$$
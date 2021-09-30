CREATE OR REPLACE FUNCTION genRandomInt(lower int4, 
                                        rand float8, 
                                        upper int4) RETURNS int4
AS
$$
    SELECT "return1".*
    FROM (LATERAL (SELECT 1 AS "result_1") AS "let0"("result_1")
          LEFT OUTER JOIN
          LATERAL (SELECT "result_1" AS "result") AS "return1"
          ON True)
$$ LANGUAGE SQL;
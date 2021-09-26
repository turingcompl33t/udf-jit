-- SQL ProcBench Scalar UDF 11: "Generate Random Character"
--
-- Modifications: The original version of this function
-- returns a CHAR. NoisePage does not support the CHAR type,
-- so I modified this definition to return a VARCHAR.

CREATE OR REPLACE FUNCTION genRandomChar(chars VARCHAR, rand FLOAT) RETURNS VARCHAR AS $$
DECLARE
    r VARCHAR;
    i INT;
    l INT;
BEGIN
    IF chars IS NULL THEN
        r := NULL;
    ELSE
        IF LENGTH(chars) = 0 THEN
            r := NULL;
        ELSE
            l = LENGTH(chars);
            i := genRandomInt(1, l, rand);
            r := SUBSTR(chars, i, 1);
        END IF;
    END IF;
    RETURN r;
END; 
$$ LANGUAGE PLPGSQL;

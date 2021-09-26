-- SQL ProcBench Scalar UDF 11: "Generate Random Character"
--
-- Modifications: The original version of this function
-- returns a CHAR. NoisePage does not support the CHAR type,
-- so I modified this definition to return a VARCHAR.

CREATE OR REPLACE FUNCTION genRandomChar(chars VARCHAR, rand FLOAT) RETURNS VARCHAR AS $$
DECLARE
    rslt CHAR(1) := NULL;
    resultIndex INT := NULL;
BEGIN
    IF chars IS NULL THEN
        rslt := NULL;
    ELSIF LENGTH(chars) = 0 THEN
        rslt := NULL;
    ELSE
        resultIndex := genRandomInt(1, LENGTH(chars), rand);
        rslt := SUBSTR(chars, resultIndex, 1);
    END IF;
    RETURN rslt;
END; 
$$ LANGUAGE PLPGSQL;

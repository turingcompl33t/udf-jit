-- Custom Benchmark: "Lighweight Loop"

CREATE OR REPLACE FUNCTION busyLoop(x INTEGER) RETURNS INTEGER AS $$
DECLARE
    c INTEGER := 0;
BEGIN
    WHILE c <= x LOOP
        c = c + 1;
    END LOOP;
    RETURN c;
END
$$ LANGUAGE PLPGSQL;

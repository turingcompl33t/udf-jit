-- Custom Benchmark: "Lighweight Loop"

CREATE OR REPLACE FUNCTION sumNaturals(x INTEGER) RETURNS INTEGER AS $$
DECLARE
    c INTEGER := 0;
    a INTEGER := 0;
BEGIN
    WHILE c <= x LOOP
        a = a + c;
        c = c + 1;
    END LOOP;
    RETURN a;
END
$$ LANGUAGE PLPGSQL;

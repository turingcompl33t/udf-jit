-- Custom Benchmark: "Overhead of Function Call"

CREATE OR REPLACE FUNCTION addOne(x INTEGER) RETURNS INTEGER AS $$
BEGIN
    RETURN x + 1;
END
$$ LANGUAGE PLPGSQL;

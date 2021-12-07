# Demonstration

A demonstration of various UDF JIT-compilation functionalities.

CREATE FUNCTION return_constant_str() RETURNS TEXT AS $$ \
BEGIN                                                \
  RETURN 'hello, functions';                         \
END                                                  \
$$ LANGUAGE PLPGSQL;

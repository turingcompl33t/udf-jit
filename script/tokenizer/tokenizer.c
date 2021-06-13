/**
 * @file tokenizer.c
 * @brief A UNIX-style PL/pgSQL function tokenizer.
 */

#include <stdio.h>
#include <stdlib.h>

#include <pg_query.h>

const char* PROC = " \
  CREATE OR REPLACE FUNCTION cs_fmt_browser_version(v_name varchar, \
                                                  v_version varchar) \
RETURNS varchar AS $$ \
BEGIN \
    IF v_version IS NULL THEN \
        RETURN v_name; \
    END IF; \
    RETURN v_name || '/' || v_version; \
END; \
$$ LANGUAGE plpgsql;";

int main() {
  PgQueryPlpgsqlParseResult result = pg_query_parse_plpgsql(PROC);
  if (result.error) {
    printf("error: %s at %d\n", result.error->message, result.error->cursorpos);
  } else {
    printf("%s\n", result.plpgsql_funcs);
  }

  pg_query_free_plpgsql_parse_result(result);
  pg_query_exit();

  return EXIT_SUCCESS;
}

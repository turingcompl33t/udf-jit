/**
 * @file query_parser.c
 * @brief A UNIX-style SQL query parser.
 * 
 * Reads a SQL query from standard input, parses the query
 * with the Postgres parser (libpg_query) and writes the 
 * JSON-formatted parse tree to standard output.
 */

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <stdbool.h>

#include <pg_query.h>

// The initial size for the query buffer
#define QUERY_BUFFER_SIZE 1024
// The number of bytes read in each iteration
#define QUERY_READ_SIZE   256

#define UNREACHABLE(msg) assert(false && msg)

// ----------------------------------------------------------------------------
// Memory Allocation
// ----------------------------------------------------------------------------

// Global counters for memory allocations
static size_t N_FREE = 0;
static size_t N_ALLOC = 0;

/**
 * @brief Allocate `size` bytes of memory.
 * @param size The number of bytes to allocate.
 * @return A pointer to the block
 * 
 * Identical to `malloc()`, crashes on allocation failure.
 */
void* check_malloc(size_t size) {
  void* ptr = malloc(size);
  assert(ptr != NULL && "malloc() failed");
  ++N_ALLOC;
  return ptr;
}

/**
 * @brief Re-allocate the previously-allocated block 
 * in `ptr`, making the new block `size` bytes long.
 * @param ptr The previously-allocated block
 * @param size The size of the allocation
 * @return A pointer to the block
 * 
 * Identical to `realloc()`, crashes on allocation failure
 */
void* check_realloc(void* ptr, size_t size) {
  void* new_ptr = realloc(ptr, size);
  assert(new_ptr != NULL && "realloc() failed");
  return new_ptr;
}

/**
 * @brief Deallocate a previously allocation.
 * @param ptr The pointer to the allocated block
 * 
 * Identical to `free()`, crashes on NULL block pointer
 */
void check_free(void* ptr) {
  if (NULL == ptr) {
    assert(false && "Call to free() will NULL pointer");
  }
  free(ptr);
  ++N_FREE;
}

/**
 * @brief Check the global allocation state.
 */
void check_allocations() {
  assert(N_FREE == N_ALLOC && "Memory leak detected");
}

// ----------------------------------------------------------------------------
// Query I/O
// ----------------------------------------------------------------------------

/**
 * @brief Read a line from the given file descriptor.
 * @param fd The file descriptor from which the line is read.
 * @return A buffer that contains the read line.
 * Buffer is allocated via a call to malloc(), caller
 * is responsible for subsequent deallocation with free().
 */
char* read_query(int fd) {
  char* query_buffer = check_malloc(QUERY_BUFFER_SIZE);
  memset(query_buffer, 0, QUERY_BUFFER_SIZE);

  // Track the current location in the buffer
  char* cursor = query_buffer;

  // Track for buffer resize operations
  size_t remaining = QUERY_BUFFER_SIZE;
  size_t buffer_size = QUERY_BUFFER_SIZE;

  for (;;) {
    ssize_t n_bytes = read(fd, cursor, QUERY_READ_SIZE);
    if (n_bytes < 0) {
      fprintf(stderr, "read() failed: %d\n", errno);
      check_free(query_buffer);
      return NULL;
    }

    cursor += n_bytes;

    if (0 == n_bytes) {
      *cursor = '\0';
      return query_buffer;
    }

    // If there is not sufficient space to read 
    // another QUERY_READ_SIZE bytes from the descriptor,
    // reallocate the buffer so it can handle it
    remaining -= n_bytes;
    if (remaining <= (QUERY_READ_SIZE + 1)) {
      const size_t new_size = buffer_size*2;
      query_buffer = check_realloc(query_buffer, new_size);
      remaining = remaining + buffer_size;
      buffer_size = new_size;
    }
  }

  UNREACHABLE("");
}

/**
 * @brief Write the parsed query to standard output.
 * @param result The parse result
 */
void write_query(PgQueryParseResult result) {
  fprintf(stdout, "%s\n", result.parse_tree);
}

// ----------------------------------------------------------------------------
// Entry Point
// ----------------------------------------------------------------------------

int main() {
  // Read the query from standard input
  char* query = read_query(STDIN_FILENO);
  if (NULL == query) {
    return EXIT_FAILURE;
  }

  // Parse the input query
  PgQueryParseResult result = pg_query_parse(query);
  if (result.error) {
    fprintf(stderr, "[ERROR]: %s at %d\n", result.error->message, result.error->cursorpos);
  }

  // Write the parsed query
  write_query(result);

  // Cleanup
  pg_query_free_parse_result(result);
  pg_query_exit();

  check_free(query);

  check_allocations();
  return EXIT_SUCCESS;
}

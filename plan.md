## user-Defined Functions

This PR adds support for user-defined functions.

### Background

For his master's thesis work, Tanuj implemented support for user-defined functions in NoisePage on a branch in his fork of the project, the most recent version of which is [here](TODO). However, because his research was primarily focused on an evaluation of different UDF performance enhancements (see the [Froid paper](https://www.vldb.org/pvldb/vol11/p432-ramachandra.pdf) for an introduction to UDF inlining) he also implemented some degree of support for other big name features, namely common table expressions and lateral joins. These two features are now largely being handled by [a separate PR](https://github.com/cmu-db/noisepage/pull/1111), so to avoid overlap, reduce the blast radius of the PRs, and (hopefully) integrate these features in a more timely manner, we are splitting the functionality implemented by Tanuj (and others) into distinct PRs. 

Therefore, _this_ PR is concerned with cherry-picking the UDf-relevant components from the existing fork, and preparing them to be integrated into `master` in a clean, controlled manner.

### Starting Point

The basic statistics for the original PR for user-defined functions and common table expressions are as follows:
- Commits: 482
- Files Changed: 304

Excluding non-source files (e.g. Java, Python, etc.) we have:
- 164 Source (`.cpp`) Files
- 114 Header (`.hpp`) Files
- 10 TPL (`.tpl`) Test Files

Clearly we need some way to more accurately assess both the scale of the PR as it relates to user-defined functions alone, as well as a way to track current progress, given the large number of components of the system that will be affected.

### Current Status

The enumeration below lists all of the files in the original PR that pertain to UDF support. While the primary goal is simply to integrate these into the current `master` branch, I reserve the right to perform any refactoring I see fit while doing so.

Binder 
- [ ] `src/binder/bind_node_visitor.cpp`
- [ ] `src/include/binder/bind_node_visitor.h`
- [ ] `src/binder/binder_context.cpp`
- [ ] `src/include/binder/binder_context.h`
- [ ] `src/include/binder/binder_sherpa.h`

Catalog
- [ ] `src/catalog/database_catalog.cpp`

Execution: AST
- [ ] `src/execution/ast/ast.cpp`
- [ ] `src/include/execution/ast/ast.h`
- [ ] `src/execution/ast/ast_clone.cpp`
- [ ] `src/include/execution/ast/ast_clone.h`
- [ ] `src/execution/ast/ast_dump.cpp`
- [ ] `src/execution/ast/ast_pretty_print.cpp`
- [ ] `src/execution/ast/context.cpp`
- [ ] `src/execution/ast/type.cpp `
- [ ] `src/include/execution/ast/type.h`
- [ ] `src/execution/ast/type_printer.cpp`
- [ ] `src/include/execution/ast/ast_node_factory.h`
- [ ] `src/include/execution/ast/builtins.h`
- [ ] `src/include/execution/compiler/ast_fwd.h`

Execution: Compiler
- [ ] `src/execution/compiler/codegen.cpp`
- [ ] `src/include/execution/compiler/codegen.h`
- [ ] `src/execution/compiler/compilation_context.cpp`
- [ ] `src/include/execution/compiler/compilation_context.h`
- [ ] `src/execution/compiler/executable_query.cpp`
- [ ] `src/include/execution/compiler/executable_query.h`
- [ ] `src/execution/compiler/executable_query_builder.cpp`
- [ ] `src/execution/compiler/expression/expression_translator.cpp`
- [ ] `src/include/execution/compiler/expression/expression_translator.h`
- [ ] `src/execution/compiler/expression/function_translator.cpp`
- [ ] `src/include/execution/compiler/expression/function_translator.h`
- [ ] `src/execution/compiler/function_builder.cpp`
- [ ] `src/include/execution/compiler/function_builder.h`
- [ ] `src/execution/compiler/operator/output_translator.cpp`
- [ ] `src/execution/compiler/operator/operator_translator.cpp`
- [ ] `src/include/execution/compiler/operator/operator_translator.h`
- [ ] `src/execution/compiler/pipeline.cpp`
- [ ] `src/include/execution/compiler/pipeline.h`

Execution: Exec
- [ ] `src/include/execution/exec/execution_context.h`
- [ ] `src/include/execution/exec/output.h`

Execution: Functions
- [ ] `src/include/execution/functions/function_context.h`

Execution: Parsing
- [ ] `src/execution/parsing/parser.cpp`
- [ ] `src/include/execution/parsing/parser.h`
- [ ] `src/execution/parsing/scanner.cpp`
- [ ] `src/include/execution/parsing/token.h`
- [ ] `src/include/execution/sema/error_message.h`

Execution: SEMA
- [ ] `src/execution/sema/scope.cpp`
- [ ] `src/include/execution/sema/scope.h`
- [ ] `src/execution/sema/sema_builtin.cpp`
- [ ] `src/execution/sema/sema_checking.cpp`
- [ ] `src/execution/sema/sema_decl.cpp`
- [ ] `src/execution/sema/sema_expr.cpp`
- [ ] `src/execution/sema/sema_stmt.cpp`
- [ ] `src/execution/sema/sema_type.cpp`

Execution: SQL
- [ ] `src/execution/sql/ddl_executors.cpp`
- [ ] `src/include/execution/sql/ddl_executors.h`

Execution: VM
- [ ] `src/execution/vm/bytecode_emitter.cpp`
- [ ] `src/include/execution/vm/bytecode_emitter.h`
- [ ] `src/execution/vm/bytecode_function_info.cpp`
- [ ] `src/include/execution/vm/bytecode_function_info.h`
- [ ] `src/execution/vm/bytecode_generator.cpp`
- [ ] `src/include/execution/vm/bytecode_generator.h`
- [ ] `src/execution/vm/bytecode_handlers.cpp`
- [ ] `src/include/execution/vm/bytecode_handlers.h`
- [ ] `src/execution/vm/bytecode_module.cpp`
- [ ] `src/execution/vm/llvm_engine.cpp`
- [ ] `src/execution/vm/module.cpp`
- [ ] `src/execution/vm/vm.cpp`
- [ ] `src/include/execution/vm/bytecodes.h`

Network
- [ ] `src/include/network/network_defs.h`

Parser
- [ ] `src/parser/postgresparser.cpp`
- [ ] `src/include/parser/postgresparser.h`

Parser: UDF (New Subdirectory)
- [ ] `src/include/parser/udf/ast_node_visitor.h`
- [ ] `src/parser/udf/ast_nodes.cpp`
- [ ] `src/include/parser/udf/ast_nodes.h`
- [ ] `src/include/parser/udf/udf_ast_context.h`
- [ ] `src/parser/udf/udf_codegen.cpp`
- [ ] `src/include/parser/udf/udf_codegen.h`
- [ ] `src/parser/udf/udf_handler.cpp`
- [ ] `src/include/parser/udf/udf_handler.h`
- [ ] `src/parser/udf/udf_parser.cpp`
- [ ] `src/include/parser/udf/udf_parser.h`

Traffic Cop
- [ ] `src/traffic_cop/traffic_cop.cpp`
- [ ] `src/traffic_cop/traffic_cop_util.cpp`

Tests
- [ ] `test/binder/binder_test.cpp`

TPL Test Files
- [ ] `sample_tpl/agg.tpl`
- [ ] `sample_tpl/call.tpl`
- [ ] `sample_tpl/param.tpl` 
- [ ] `sample_tpl/struct.tpl`
## NoisePage UDF Integration Plan

Tanuj has implemented limited support for UDF execution in NoisePage on a branch in his fork of the project. However, also included in this PR are several other features that either overlap with other outstanding PRs or are incomplete. Therefore, we only want to bring in UDF support, and do so in a clean, controlled manner. This is the plan we will follow to accomplish this.

PR Statistics:
- Commits: 482
- Files Changed: 304

Excluding Non-Source Files (e.g. Java, Python, etc.):
- 164 Source (`.cpp`) Files
- 114 Header (`.hpp`) Files
- 10 TPL (`.tpl`) Test Files

Binder 
- binder/bind_node_visitor.cpp
- include/binder/bind_node_visitor.h
- binder/binder_context.cpp
- include/binder/binder_context.h
- include/binder/binder_sherpa.h

Catalog
- catalog/database_catalog.cpp

Execution: AST
- execution/ast/ast.cpp
- include/execution/ast/ast.h
- execution/ast/ast_clone.cpp
- include/execution/ast/ast_clone.h
- execution/ast/ast_dump.cpp
- execution/ast/ast_pretty_print.cpp
- execution/ast/context.cpp
- execution/ast/type.cpp 
- include/execution/ast/type.h
- execution/ast/type_printer.cpp
- include/execution/ast/ast_node_factory.h
- include/execution/ast/builtins.h
- include/execution/compiler/ast_fwd.h

Execution: Compiler
- execution/compiler/codegen.cpp
- include/execution/compiler/codegen.h
- execution/compiler/compilation_context.cpp
- include/execution/compiler/compilation_context.h
- execution/compiler/executable_query.cpp
- include/execution/compiler/executable_query.h
- execution/compiler/executable_query_builder.cpp
- execution/compiler/expression/expression_translator.cpp
- include/execution/compiler/expression/expression_translator.h
- execution/compiler/expression/function_translator.cpp
- include/execution/compiler/expression/function_translator.h
- execution/compiler/function_builder.cpp
- include/execution/compiler/function_builder.h
- execution/compiler/operator/output_translator.cpp
- execution/compiler/operator/operator_translator.cpp
- include/execution/compiler/operator/operator_translator.h
- execution/compiler/pipeline.cpp
- include/execution/compiler/pipeline.h

Execution: Exec (Horrible Name)
- include/execution/exec/execution_context.h
- include/execution/exec/output.h

Execution: Functions
- include/execution/functions/function_context.h

Execution: Parsing
- execution/parsing/parser.cpp
- include/execution/parsing/parser.h
- execution/parsing/scanner.cpp
- include/execution/parsing/token.h
- include/execution/sema/error_message.h

Execution: SEMA
- execution/sema/scope.cpp
- include/execution/sema/scope.h
- execution/sema/sema_builtin.cpp
- execution/sema/sema_checking.cpp
- execution/sema/sema_decl.cpp
- execution/sema/sema_expr.cpp
- execution/sema/sema_stmt.cpp
- execution/sema/sema_type.cpp

Execution: SQL
- execution/sql/ddl_executors.cpp
- include/execution/sql/ddl_executors.h

Execution: VM
- execution/vm/bytecode_emitter.cpp
- include/execution/vm/bytecode_emitter.h
- execution/vm/bytecode_function_info.cpp
- include/execution/vm/bytecode_function_info.h
- execution/vm/bytecode_generator.cpp
- include/execution/vm/bytecode_generator.h
- execution/vm/bytecode_handlers.cpp
- include/execution/vm/bytecode_handlers.h
- execution/vm/bytecode_module.cpp
- execution/vm/llvm_engine.cpp
- execution/vm/module.cpp
- execution/vm/vm.cpp
- include/execution/vm/bytecodes.h

Network
- include/network/network_defs.h

Parser
- parser/postgresparser.cpp
- include/parser/postgresparser.h

Parser: UDF
- include/parser/udf/ast_node_visitor.h
- parser/udf/ast_nodes.cpp
- include/parser/udf/ast_nodes.h
- include/parser/udf/udf_ast_context.h
- parser/udf/udf_codegen.cpp
- include/parser/udf/udf_codegen.h
- parser/udf/udf_handler.cpp
- include/parser/udf/udf_handler.h
- parser/udf/udf_parser.cpp
- include/parser/udf/udf_parser.h

Traffic Cop
- traffic_cop/traffic_cop.cpp
- traffic_cop/traffic_cop_util.cpp

Tests
- test/binder/binder_test.cpp

TPL Test Files
- agg.tpl
- call.tpl
- param.tpl 
- struct.tpl
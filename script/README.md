gcc -Ilibpg_query -c tokenizer.c
gcc -llibpg_query/libpg_query.a tokenizer.o -o tokenizer
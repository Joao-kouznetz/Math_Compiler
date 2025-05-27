
#include <stdio.h>

/* words_callback defined in the object file -- you could put
   this declaration in a header file words.h */
int token_callback(char *, void (*)(const char * ,const char *));

void print_word(const char *tokname , const char *token)
{
	printf("%-12s → \"%s\"\n", tokname, token);
}

int main(void)
{
	token_callback(
        "while ( 9129821 ola ): {}\n", &print_word
	);
	return 0;
}

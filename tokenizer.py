class Token:
    """
    Representa um token com um tipo e um valor opcional.
    """

    def __init__(self, type, value=None):
        if not isinstance(type, str):
            raise ValueError("O atributo 'type' deve ser uma string")
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


class Tokenizer:
    """
    Tokenizer que separa a string de entrada em tokens.
    Atributo 'next' armazena o último token separado.
    método selectNext pega o novo token.
    """

    def __init__(self, source):
        """
        init do tokenizer
        """
        if not isinstance(source, str):
            raise ValueError("O código fonte 'source' deve ser uma string")
        self.source = source
        self.position = 0
        self.next = self.selectNext()  # Inicializa 'next' com o primeiro token

    def selectNext(self):
        """
        Retorna o próximo token na sequência e atualiza o atributo 'next'.
        """
        # ta retirando os espaços e quebrando os tokens sem pular quebra de linhas
        while self.position < len(self.source) and self.source[self.position] in " \t":
            self.position += 1

        if self.position >= len(self.source):
            token = Token("EOF", None)
            self.next = token  # Atualiza 'next' com EOF
            return token

        current_char = self.source[self.position]

        if current_char.isdigit():
            start = self.position
            while (
                self.position < len(self.source)
                and self.source[self.position].isdigit()
            ):
                self.position += 1
            value = int(self.source[start : self.position])
            token = Token("NUMBER", value)
            self.next = token  # Atualiza 'next' com o número encontrado
            return token
        elif current_char == "+":
            self.position += 1
            token = Token("PLUS", None)
            self.next = token  # Atualiza 'next' com o operador PLUS
            return token
        elif current_char == "-":
            self.position += 1
            token = Token("MINUS", None)
            self.next = token  # Atualiza 'next' com o operador MINUS
            return token
        elif current_char == "*":
            self.position += 1
            token = Token("MULT", None)
            self.next = token  # Atualiza 'next'com o operador MULT
            return token
        elif current_char == "/":
            self.position += 1
            token = Token("DIV", None)
            self.next = token  # Atualiza 'next'com o operador DIV
            return token
        elif current_char == "(":
            self.position += 1
            token = Token("OPEN_PAR", None)
            self.next = token  # atualiza o 'next'com o operador OPEN_PAR
            return token
        elif current_char == ")":
            self.position += 1
            token = Token("CLOSE_PAR", None)
            self.next = token  # atualiza o 'next'com o operador OPEN_PAR
            return token
        elif current_char == "{":
            self.position += 1
            token = Token("OPEN_BRA", None)
            self.next = token
            return token
        elif current_char == "}":
            self.position += 1
            token = Token("CLOSE_BRA", None)
            self.next = token
            return token
        elif current_char == "\n":
            self.position += 1
            token = Token("LINE_FEED", None)
            self.next = token
            return token
        elif current_char == "!":
            self.position += 1
            token = Token("NOT", None)
            self.next = token
            return token
        elif current_char == "<":
            self.position += 1
            token = Token("SMALLER", None)
            self.next = token
            return token
        elif current_char == ">":
            self.position += 1
            token = Token("GREATER", None)
            self.next = token
            return token
        elif current_char == ",":
            self.position += 1
            token = Token("COMMA", None)
            self.next = token
            return token
        elif current_char == "=":
            self.position += 1
            if (
                self.position < len(self.source) and self.source[self.position] == "="
            ):  # é o current char
                self.position += 1
                token = Token("EQUAL_EQUAL", None)
                self.next = token
                return token
            else:
                token = Token("EQUAL", None)
                self.next = token
                return token
        elif current_char == "|":
            self.position += 1
            if (
                self.position < len(self.source) and self.source[self.position] == "|"
            ):  # é o current char
                self.position += 1
                token = Token("OR", None)
                self.next = token
            else:
                # erro lexico
                raise ValueError(
                    f"Caracter invalido encontrado:' {current_char}'vindo depois de um '|' "
                )
        elif current_char == "&":
            self.position += 1
            if (
                self.position < len(self.source) and self.source[self.position] == "&"
            ):  # é o current char
                self.position += 1
                token = Token("AND", None)
                self.next = token
            else:
                # erro lexico
                raise ValueError(
                    f"Caracter invalido encontrado:' {current_char}' vindo depois de um &"
                )
        elif current_char == '"':
            self.position += 1
            start = self.position
            while (
                self.position < len(self.source) and self.source[self.position] != '"'
            ):
                self.position += 1
            if self.position >= len(self.source):
                raise ValueError("String literal não fechada")
            value = self.source[start : self.position]
            self.position += 1
            token = Token("STR", value)
            self.next = token
            return token
        elif current_char.isidentifier():
            start = self.position
            while (
                self.position < len(self.source)
                and (self.source[self.position].isidentifier())
                or self.source[self.position].isdigit()
            ):
                self.position += 1
            value = str(self.source[start : self.position])
            if value == "Println":
                token = Token("PRINT", None)
                self.next = token  # Atualiza 'next' com o número encontrado
                return token
            elif value == "for":
                token = Token("FOR", None)
                self.next = token
                return token
            elif value == "if":
                token = Token("IF", None)
                self.next = token
                return token
            elif value == "else":
                token = Token("ELSE", None)
                self.next = token
                return token
            elif value == "Scan":
                token = Token("READ", None)
                self.next = token
                return token
            elif value == "true":
                token = Token("BOOL", True)
                self.next = token
                return token
            elif value == "false":
                token = Token("BOOL", False)
                self.next = token
                return token
            elif value == "var":
                token = Token("VAR", None)
                self.next = token
                return token
            elif value == "bool":
                token = Token("TYPE", "bool")
                self.next = token
                return token
            elif value == "int":
                token = Token("TYPE", "int")
                self.next = token
                return token
            elif value == "string":
                token = Token("TYPE", "str")
                self.next = token
                return token
            elif value == "def":
                token = Token("FUNC", None)
                self.next = token
                return token
            elif value == "return":
                token = Token("RETURN", None)
                self.next = token
                return token
            else:
                token = Token("IDENTIFIER", value)
                self.next = token  # Atualiza 'next' com o número encontrado
                return token
        else:
            # Erro lexico
            raise ValueError(f"Caractere inválido encontrado: '{current_char}'")

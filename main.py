import sys
from parser_arvore_sintatica import Parser


class SymbolTable:
    def __init__(self, parent=None):
        self.table = {}
        self.parent = parent

    # get key
    def get_keyValue(self, key):
        if key in self.table:
            return self.table[key]
        elif self.parent:
            return self.parent.get_keyValue(key)
        else:
            # Erro semantico
            raise KeyError(f"Chave {key} não definida'")

    # setter
    def set_keyValue(self, key, value):
        if key in self.table:
            if self.table[key][0][0] == "func":
                tipo = "func"
                pass
            if self.table[key][0][0] == "func" or isinstance(value, int):
                self.table[key][1] = value
        elif self.parent:
            self.parent.set_keyValue(key, value)
        else:
            raise KeyError(f"chave {key} não definida")

    def set_defineKeyType(self, key, type):
        if key not in self.table:
            self.table[key] = [type, None]
        else:
            raise ValueError("Você ja declarou essa variável")

    # Método para anexar um novo escopo (SymbolTable) no topo da pilha
    def push_scope(self):
        return SymbolTable(parent=self)

    # Método para destruir/remover o escopo atual e voltar ao escopo anterior
    def pop_scope(self):
        return self.parent


def main():
    """
    Função principal para executar o tokenizer a partir da linha de comando ou input interativo.
    """
    source = "test_code.go"
    # Lendo a entrada: via linha de comando ou input interativo
    if len(sys.argv) > 1:
        source = sys.argv[1]

    with open(source, "r") as file:
        code = file.read()
    st = SymbolTable()
    Parser.run(code=code, st=st)


if __name__ == "__main__":
    main()

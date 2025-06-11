from tokenizer import Tokenizer
import re
from latex import render_latex


class PrePro:
    """
    Vai fazer o pre processamento da string. Basicamente vai retornar o código sem os comentários
    """

    @staticmethod
    def filter(source):
        # Remove comentários
        pattern = r"//.*?(?=\n|$)"
        return re.sub(pattern=pattern, repl="", string=source)


class Node:
    """
    Vai funcionar para retonrar os nós da arvore.
    """

    def __init__(self, value, children):
        self.value = value
        self.children = children

    def evaluate(self, st):
        pass

    def latlatexate(self, st):
        pass


class BinOp(Node):
    """herda a classe node, é uma extensão dela especificamente para operaçÕes binarias, (tem dois filhos)
    agora ele esta vendo os dois tipos da operação binaria, verificando se pode fazer a operação. Se permetir retorna um [tipo, valor] e se não permetir gera erro
    """

    def evaluate(self, st):
        tipo0 = self.children[0].evaluate(st=st)[0]
        tipo1 = self.children[1].evaluate(st=st)[0]
        if self.value == "+" and (
            (tipo0 == "str" and tipo1 == "str")
            or (tipo0 == "int" and tipo1 == "str")
            or (tipo0 == "str" and tipo1 == "int")
            or (tipo0 == "str" and tipo1 == "bool")
        ):
            if tipo1 == "bool":
                valor1 = str(self.children[1].evaluate(st=st)[1]).lower()
            else:
                valor1 = str(self.children[1].evaluate(st=st)[1])

            valor = str(self.children[0].evaluate(st=st)[1]) + valor1

            return ["str", valor]
        elif self.value == "+" and (tipo0 == "int" and tipo1 == "int"):
            valor = (
                self.children[0].evaluate(st=st)[1]
                + self.children[1].evaluate(st=st)[1]
            )
            return ["int", valor]
        elif self.value == "+":
            raise ValueError(
                f"Voce esta concatenando/ somando um { tipo0} com um {tipo1}"
            )
        elif self.value == "-" and (tipo0 == "int" and tipo1 == "int"):
            valor = (
                self.children[0].evaluate(st=st)[1]
                - self.children[1].evaluate(st=st)[1]
            )
            return ["int", valor]
        elif self.value == "-":
            raise ValueError(f"Voce esta subtraindo um { tipo0} com um {tipo1}")
        elif self.value == "*" and (tipo0 == "int" and tipo1 == "int"):
            resultado = (
                self.children[0].evaluate(st=st)[1]
                * self.children[1].evaluate(st=st)[1]
            )
            return ["int", resultado]
        elif self.value == "*":
            raise ValueError(f"Voce esta multiplicando um { tipo0} com um {tipo1}")
        elif self.value == "//" and (tipo0 == "int" and tipo1 == "int"):
            resultado = (
                self.children[0].evaluate(st=st)[1]
                // self.children[1].evaluate(st=st)[1]
            )
            return ["int", resultado]
        elif self.value == "//":
            raise ValueError(f"Voce esta dividindo um { tipo0} com um {tipo1}")
        elif self.value == "/" and (tipo0 == "int" and tipo1 == "int"):
            resultado = (
                self.children[0].evaluate(st=st)[1]
                // self.children[1].evaluate(st=st)[1]
            )
            return ["int", resultado]
        elif self.value == "/":
            raise ValueError(f"Voce esta dividindo um { tipo0} com um {tipo1}")
        elif self.value == "&&" and (tipo0 == "bool" and tipo1 == "bool"):
            resultado = (
                self.children[0].evaluate(st=st)[1]
                and self.children[1].evaluate(st=st)[1]
            )
            return ["bool", resultado]
        elif self.value == "&&":
            raise ValueError(
                f"Voce esta fazendo um and com um { tipo0} e com um {tipo1}"
            )
        elif self.value == "||" and (tipo0 == "bool" and tipo1 == "bool"):
            resultado = (
                self.children[0].evaluate(st=st)[1]
                or self.children[1].evaluate(st=st)[1]
            )
            return ["bool", resultado]
        elif self.value == "||":
            raise ValueError(
                f"Voce esta fazendo um or com um { tipo0} e com um {tipo1}"
            )
        elif self.value == "==" and (
            (tipo0 == "bool" and tipo1 == "bool")
            or (tipo0 == "int" and tipo1 == "int")
            or (tipo0 == "str" and tipo1 == "str")
        ):
            resultado = (
                self.children[0].evaluate(st=st)[1]
                == self.children[1].evaluate(st=st)[1]
            )
            return ["bool", resultado]
        elif self.value == "==":
            raise ValueError(
                f"Voce esta vendo uma igualdade com um { tipo0} e com um {tipo1}"
            )
        elif self.value == ">" and (
            (tipo0 == "int" and tipo1 == "int") or (tipo0 == "str" and tipo1 == "str")
        ):
            resultado = (
                self.children[0].evaluate(st=st)[1]
                > self.children[1].evaluate(st=st)[1]
            )
            return ["bool", resultado]
        elif self.value == ">":
            raise ValueError(
                f"Voce esta fazendo um maior que o outro com { tipo0} e com um {tipo1}"
            )
        elif self.value == "<" and (
            (tipo0 == "int" and tipo1 == "int") or (tipo0 == "str" and tipo1 == "str")
        ):
            resultado = (
                self.children[0].evaluate(st=st)[1]
                < self.children[1].evaluate(st=st)[1]
            )
            return ["bool", resultado]
        elif self.value == "<":
            raise ValueError(
                f"Voce esta fazendo um menor que o outro com { tipo0} e com um {tipo1}"
            )
        else:
            # Erro Semântico operação invalida ?
            raise ValueError(f"Operador '{self.value}' inválido")

    def latexate(self, st):
        left = self.children[0].latexate(st)
        right = self.children[1].latexate(st)
        op = {
            "+": " + ",
            "-": " - ",
            "*": " \\times ",
            "/": " \\div ",
            "^": "^",
            "==": "=",
            "<": "<",
            ">": ">",
        }[self.value]
        if self.value == "^":
            return f"{left}^{{{right}}}"
        return f"( {left}{op}{right} )"


class UnOp(Node):
    """Herda a classe node, so para operações unarias so tem 1 filho agora esta fazendo verificação de tipo e retorna um [tipo, valor]"""

    def evaluate(self, st):
        tipo = self.children[0].evaluate(st=st)[0]
        if self.value == "+" and tipo == "int":
            resultado = self.children[0].evaluate(st=st)[1] * 1
            return ["int", resultado]
        elif self.value == "-" and tipo == "int":
            resultado = self.children[0].evaluate(st=st)[1] * (-1)
            return ["int", resultado]
        elif self.value == "!" and tipo == "bool":
            resultado = not self.children[0].evaluate(st=st)[1]
            return ["bool", resultado]
        elif self.value in ["!", "+", "-"]:
            raise TypeError(
                f"Voce esta com o seguinte operador unario: {self.value} e esta fazendo a conta com esse tipo: {tipo}"
            )
        else:
            # Erro Semântico realizando operação invalida?
            raise ValueError(f"Operador '{self.value}' inválido")

    def latexate(self, st):
        operand = (
            self.children[0].latexate(st)
            if hasattr(self.children[0], "latexate")
            else self.children[0].latexate(st)
        )
        if self.value == "!":
            return r"\lnot " + operand
        return self.value + operand


class IntVal(Node):
    """Herda a classe node, não contem filhos"""

    def evaluate(self, st):
        return ["int", self.value]

    def latexate(self, st):
        return str(self.value)


class StrVal(Node):
    """Herda a classe node, não contem filhos"""

    def evaluate(self, st):
        return ["str", self.value]


class BoolVal(Node):
    """Herda a classe node, não contem filhos"""

    def evaluate(self, st):
        return ["bool", self.value]


class NoOp(Node):
    """é um dummy por em quanto"""

    def evaluate(self, st):
        return 0

    def latexate(self, st):
        return ""


class Ident(Node):
    """Herda a classe node, não contem filhos"""

    def evaluate(self, st):
        return st.get_keyValue(self.value)

    def latexate(self, st):
        return st.get_keyValue(self.value)[1]


class Print(Node):
    """Heda a classe node, contem 1 filho"""

    def evaluate(self, st):
        if isinstance(self.children[0].evaluate(st=st)[1], bool):
            print(str(self.children[0].evaluate(st=st)[1]).lower())
        else:
            print(self.children[0].evaluate(st=st)[1])


class Block(Node):
    """Herda a classe node, contem x filhos"""

    def evaluate(self, st):
        for children in self.children:
            if isinstance(children, Return):
                return children.evaluate(st=st)
            elif isinstance(children, Block):
                new_st = st.push_scope()
                result = children.evaluate(st=new_st)
                # precisaria propagar retorno?
                if result is not None:
                    return result
            else:
                result = children.evaluate(st=st)
                if result is not None and (
                    isinstance(result, list) or isinstance(result, tuple)
                ):
                    # Propaga retornos de return aninhados (ex: vindo de if/while)
                    return result

    def latexate(self, st):
        parts = [child.latexate(st) for child in self.children]
        return "\n".join(p for p in parts if p)


class Dec(Node):
    """Herda a classe node e tem 1 filho e opcionalmente outro. Ela é para definir a variavel"""

    def evaluate(self, st):
        """ta definindo e colocando na arvore sintatica qual é o tipo da variavel. Pode colocar ou não qual é o valor"""
        identifier = self.children[0].value
        type = self.value
        st.set_defineKeyType(key=identifier, type=type)
        if len(self.children) > 1:
            """Tem o filho opcional definido a variavel"""
            valor = self.children[1].evaluate(st=st)[1]
            st.set_keyValue(key=identifier, value=valor)

    def latexate(self, st):
        ident = self.children[0].value
        if len(self.children) > 1:
            expr = self.children[1].latexate(st)
            return f"{ident} : {self.value} = {expr}"
        return f"{ident} : {self.value}"


class Assigment(Node):
    """Herda a classe node, contem 2 filhos"""

    def evaluate(self, st):
        """só coloca o valor da variavel oq é"""
        valor = self.children[1].evaluate(st=st)[1]
        identifier = self.children[0].value
        st.set_keyValue(key=identifier, value=valor)

    def latexate(self, st):
        ident = self.children[0].value
        expr = self.children[1].latexate(st)
        return f"{ident} = {expr}"


class While(Node):
    """Herda a classe node tem 2 filhos"""

    def evaluate(self, st):
        tipo = self.children[0].evaluate(st=st)[0]
        if tipo != "bool":
            raise ValueError(
                "Voce não esta usando um bool na sua clausula de continuidade no for"
            )
        while self.children[0].evaluate(st=st)[1] == True:
            resultado = self.children[1].evaluate(st=st)
            if resultado is not None:
                return resultado

    def latexate(self, st):
        cond = self.children[0].latexate(st)
        body = self.children[1].latexate(st)
        return r"\mathbf{while}\ " + cond + r"\ do\ " + body


class If(Node):
    """Herda a classe node pode ter 2 ou 3 filhos depende se tem else ou não"""

    def evaluate(self, st):
        tipo = self.children[0].evaluate(st=st)[0]
        if tipo != "bool":
            raise ValueError("Voce não esta usando um bool na sua clausula if")
        if self.children[0].evaluate(st=st)[1] == True:
            resultado = self.children[1].evaluate(st=st)
            if resultado is not None:
                return resultado
        elif len(self.children) > 2:
            resultado = self.children[2].evaluate(st=st)
            if resultado is not None:
                return resultado

    def latexate(self, st):
        cond = self.children[0].latexate()
        then = self.children[1].children[0].latexate()
        parts = [rf"{then}, & {cond},\\"]
        if len(self.children) > 2:
            els = self.children[2].children[0].latexate()
            parts.append(rf"{els}, & \text{{caso contrário.}}\\")
        cases = "\n".join(parts)
        return rf"""\begin{{cases}}{cases}\end{{cases}}"""


class Read(Node):
    """Herda a classe node e não tem filhos"""

    def evaluate(self, st):
        # inteiro porque até agora so trabalhamos com inteiro
        return ["int", int(input())]


class FuncDec(Node):
    """Herda a classe node e tem n+2 filhos do tipo identificador ou expressão sendo o primeiro um identfier, o identfier dos parametros e o ultimo o block. lembrando que o tipo que esta antes do block vai estar como value do no do funcdec"""

    def evaluate(self, st):
        func_name = self.children[0].value
        return_tipo = self.value
        st.set_defineKeyType(func_name, ["func", return_tipo])
        st.set_keyValue(
            func_name,
            self,
        )

    def latexate(self, st):
        func_name = self.children[0].value
        return_tipo = self.value
        st.set_defineKeyType(func_name, ["func", return_tipo])
        st.set_keyValue(
            func_name,
            self,
        )
        lista_function = st.get_keyValue(func_name)
        retorno = lista_function[0][1]
        no_function = lista_function[1]
        # os filhos de no_function: [nome, params..., bloco] (ajuste se diferente!)
        if len(no_function.children) > 2:
            params = no_function.children[1:-1]
        else:
            params = []
        bloco = no_function.children[-1]
        if len(self.children) != len(params):
            new_st = st.push_scope()
            lista_ident_entrada = []
            for index in range(len(params)):
                # param é o que esta recebendo
                param_node = params[index]
                tipo = "int"
                ident = param_node.children[0].value
                lista_ident_entrada.append(ident)
                new_st.set_defineKeyType(ident, tipo)
                new_st.set_keyValue(ident, str(ident))
            resultado = bloco.latexate(new_st)
        else:
            new_st = st.push_scope()
            for index in range(len(params)):
                # param é o que esta recebendo
                param_node = params[index]
                tipo = param_node.value
                ident = param_node.children[0].value
                arg_node = self.children[index]
                valor = arg_node.evaluate(st=st)[1]
                # param_node.children.append(arg_node)
                # param_node.evaluate(st=st)
                new_st.set_defineKeyType(ident, tipo)
                new_st.set_keyValue(ident, valor)
            resultado = bloco.latexate(new_st)

        parametros = ", ".join(lista_ident_entrada)
        return "$$ " + func_name + "(" + parametros + ")" + " = " + resultado + " $$"


class FuncCall(Node):
    """herda a classe node e possui n filhos do tipo identificador ou expressão"""

    def evaluate(self, st):
        nome_fun = self.value
        lista_function = st.get_keyValue(nome_fun)
        retorno = lista_function[0][1]
        no_function = lista_function[1]
        # os filhos de no_function: [nome, params..., bloco] (ajuste se diferente!)
        if len(no_function.children) > 2:
            params = no_function.children[1:-1]
        else:
            params = []
        bloco = no_function.children[-1]
        if len(self.children) != len(params):
            raise TypeError("voce passou a quantidade errada de argumentos")

        new_st = st.push_scope()
        for index in range(len(params)):
            # param é o que esta recebendo
            param_node = params[index]
            tipo = param_node.value
            ident = param_node.children[0].value
            arg_node = self.children[index]
            valor = arg_node.evaluate(st=st)[1]
            # param_node.children.append(arg_node)
            # param_node.evaluate(st=st)
            new_st.set_defineKeyType(ident, tipo)
            new_st.set_keyValue(ident, valor)
        resultado = bloco.evaluate(new_st)
        if resultado is not None:
            if retorno == "void":
                raise TypeError("não era para voce retornar na sua func")
            elif retorno == "int":
                tipo = int
            elif retorno == "string":
                tipo = str
            elif retorno == "bool":
                tipo = bool
            if tipo is int and type(resultado[1]) is bool:
                # bloqueando bools sendo usados como int (porque em python true é subconjunto de int)
                raise TypeError("bool não pode ser atribuído a  ints")
            elif isinstance(resultado[1], tipo):
                return resultado
            else:
                raise TypeError(
                    f"o retorno da sua funcao é {retorno} e voce esta retornando {resultado}"
                )
        if retorno != "void":
            raise TypeError("era para a sua funcao estar retornando e não esta.")

    def latexate(self, st):
        nome_fun = self.value
        lista_function = st.get_keyValue(nome_fun)
        retorno = lista_function[0][1]
        no_function = lista_function[1]
        # os filhos de no_function: [nome, params..., bloco] (ajuste se diferente!)
        if len(no_function.children) > 2:
            params = no_function.children[1:-1]
        else:
            params = []
        bloco = no_function.children[-1]
        if len(self.children) != len(params):
            raise TypeError("voce passou a quantidade errada de argumentos")

        new_st = st.push_scope()
        for index in range(len(params)):
            # param é o que esta recebendo
            param_node = params[index]
            tipo = param_node.value
            ident = param_node.children[0].value
            arg_node = self.children[index]
            valor = arg_node.latexate(st=st)
            # param_node.children.append(arg_node)
            # param_node.evaluate(st=st)
            new_st.set_defineKeyType(ident, tipo)
            new_st.set_keyValue(ident, valor)
        resultado = bloco.latexate(new_st)
        return resultado


class Return(Node):
    """herda a classe node e possui 1 filho a depender da expressão recebida ele é um filho do block"""

    def evaluate(self, st):
        return self.children[0].evaluate(st=st)

    def latexate(self, st):
        expr = self.children[0].latexate(st)
        return expr


class Parser:
    @staticmethod
    def parseFactor(st):
        """
        Aqui é para o parenteses, e operadores unários
        """

        if Parser.T.next.type == "NUMBER":
            no = IntVal(value=int(Parser.T.next.value), children=[])
            Parser.T.selectNext()
            return no
        elif Parser.T.next.type == "IDENTIFIER":
            nome_variavel = Parser.T.next.value
            no = Ident(value=str(nome_variavel), children=[])
            Parser.T.selectNext()
            if Parser.T.next.type != "OPEN_PAR":
                return no

            if Parser.T.next.type == "OPEN_PAR":
                filhos_funcall = []
                Parser.T.selectNext()
                if Parser.T.next.type == "CLOSE_PAR":
                    Parser.T.selectNext()  # Nenhum parâmetro
                else:
                    while True:
                        no_biexpression = Parser.parseBiexpression(st=st)
                        filhos_funcall.append(no_biexpression)
                        if Parser.T.next.type == "COMMA":
                            Parser.T.selectNext()
                        elif Parser.T.next.type == "CLOSE_PAR":
                            Parser.T.selectNext()
                            break
                        else:
                            raise SyntaxError("Esperado ',' ou ')' após function call")
                    no = FuncCall(value=nome_variavel, children=filhos_funcall)
            else:
                raise SyntaxError(
                    f"Você esta ou chamando uma func ou declarando uma variavel para o identifier : {nome_variavel} então precisa ter um  '=' ou um '(' "
                )
            return no

        elif Parser.T.next.type == "STR":
            no_str = StrVal(value=Parser.T.next.value, children=[])
            Parser.T.selectNext()
            return no_str
        elif Parser.T.next.type == "BOOL":
            no_bool = BoolVal(value=Parser.T.next.value, children=[])
            Parser.T.selectNext()
            return no_bool
        elif Parser.T.next.type == "PLUS":
            Parser.T.selectNext()
            no = UnOp(value="+", children=[Parser.parseFactor(st=st)])
            return no
        elif Parser.T.next.type == "MINUS":
            Parser.T.selectNext()
            no = UnOp(value="-", children=[Parser.parseFactor(st=st)])
            return no
        elif Parser.T.next.type == "NOT":
            Parser.T.selectNext()
            no = UnOp(value="!", children=[Parser.parseFactor(st=st)])
            return no
        elif Parser.T.next.type == "OPEN_PAR":
            Parser.T.selectNext()
            resultado = Parser.parseBiexpression(st=st)
            if Parser.T.next.type == "CLOSE_PAR":
                Parser.T.selectNext()
                return resultado
            else:
                raise ValueError(f"O fechamento de parenteses não ocorre")
        elif Parser.T.next.type == "READ":
            Parser.T.selectNext()
            no_input = Read(value="Scan", children=[])
            if Parser.T.next.type == "OPEN_PAR":
                Parser.T.selectNext()
                if Parser.T.next.type == "CLOSE_PAR":
                    Parser.T.selectNext()
                else:
                    raise ValueError(f" Faltou fechar o parenteses do Scan")
            else:
                raise ValueError(
                    f"Caracter invalido, precisa abrir parenteses depois de Scan"
                )
            return no_input

        else:
            raise ValueError(f"Caracter invalido")

    @staticmethod
    def parseTerm(st):
        """
        consome os tokens do Tokenizer e analise se a sintaxe está aderente à gramática proposta. retorna o resultado da expressão analisada.
        ele so é para o * e o /.
        """

        no = Parser.parseFactor(st)
        while Parser.T.next.type in ["DIV", "MULT"]:

            if Parser.T.next.type == "MULT":
                Parser.T.selectNext()
                no = BinOp(value="*", children=[no, Parser.parseFactor(st=st)])

            elif Parser.T.next.type == "DIV":
                Parser.T.selectNext()
                no = BinOp(value="/", children=[no, Parser.parseFactor(st=st)])

        return no

    @staticmethod
    def parseExpression(st):
        """
        consome os tokens do Tokenizer e analise se a sintaxe está aderente à gramática proposta. retorna o resultado da expressão analisada.
        """

        no = Parser.parseTerm(st=st)
        while Parser.T.next.type in ["PLUS", "MINUS"]:

            if Parser.T.next.type == "MINUS":
                Parser.T.selectNext()
                no = BinOp(value="-", children=[no, Parser.parseTerm(st=st)])

            elif Parser.T.next.type == "PLUS":
                Parser.T.selectNext()
                no = BinOp(value="+", children=[no, Parser.parseTerm(st=st)])

        return no

    @staticmethod
    def parseRelExpression(st):
        no = Parser.parseExpression(st=st)
        while Parser.T.next.type in ["EQUAL_EQUAL", "GREATER", "SMALLER"]:
            if Parser.T.next.type == "EQUAL_EQUAL":
                Parser.T.selectNext()
                no = BinOp(value="==", children=[no, Parser.parseRelExpression(st=st)])
            elif Parser.T.next.type == "GREATER":
                Parser.T.selectNext()
                no = BinOp(value=">", children=[no, Parser.parseRelExpression(st=st)])

            elif Parser.T.next.type == "SMALLER":
                Parser.T.selectNext()
                no = BinOp(value="<", children=[no, Parser.parseRelExpression(st=st)])

        return no

    @staticmethod
    def parseBiTerm(st):
        no = Parser.parseRelExpression(st=st)
        while Parser.T.next.type == "AND":
            if Parser.T.next.type == "AND":
                Parser.T.selectNext()
                no = BinOp(value="&&", children=[no, Parser.parseRelExpression(st=st)])
        return no

    @staticmethod
    def parseBiexpression(st):
        """consome os tokens do Tokenizer e analisa se a sintaxe esta aderente a grammática. essa é a parte de maior prioridade das operações binarias"""
        no = Parser.parseBiTerm(st=st)
        while Parser.T.next.type == "OR":
            if Parser.T.next.type == "OR":
                Parser.T.selectNext()
                no = BinOp(value="||", children=[no, Parser.parseBiTerm(st=st)])
        return no

    @staticmethod
    def parseStatement(st):
        """
        consome os tokens do Tokenizer e analise se a sintaxe está aderente à gramática proposta. retorna o resultado da expressão analisada.
        ele so é para o identifier e para o println, while e if.
        """
        if Parser.T.next.type == "IDENTIFIER":
            nome_variavel = Parser.T.next.value
            Parser.T.selectNext()
            no_esquerda = Ident(value=str(nome_variavel), children=[])
            if Parser.T.next.type == "EQUAL":
                Parser.T.selectNext()
                no = Assigment(
                    value="=", children=[no_esquerda, Parser.parseBiexpression(st=st)]
                )
            elif Parser.T.next.type == "OPEN_PAR":
                filhos_funcall = []
                Parser.T.selectNext()
                if Parser.T.next.type == "CLOSE_PAR":
                    Parser.T.selectNext()  # Nenhum parâmetro
                else:
                    while True:
                        no_biexpression = Parser.parseBiexpression(st=st)
                        filhos_funcall.append(no_biexpression)
                        if Parser.T.next.type == "COMMA":
                            Parser.T.selectNext()
                        elif Parser.T.next.type == "CLOSE_PAR":
                            Parser.T.selectNext()
                            break
                        else:
                            raise SyntaxError("Esperado ',' ou ')' após function call")
                    no = FuncCall(value=nome_variavel, children=filhos_funcall)
            else:
                raise SyntaxError(
                    f"Você esta ou chamando uma func ou declarando uma variavel para o identifier : {identifier} então precisa ter um  '=' ou um '(' "
                )
            if Parser.T.next.type == "LINE_FEED":
                Parser.T.selectNext()
                # no_noop = NoOp(value="barra_n", children=[])
            else:
                raise SyntaxError(f"Precisa ter um /n depois de definir uma variavel")
            return no

        elif Parser.T.next.type == "PRINT":
            Parser.T.selectNext()
            if Parser.T.next.type == "OPEN_PAR":
                Parser.T.selectNext()
                no_print = Print(
                    value="print", children=[Parser.parseBiexpression(st=st)]
                )
                if Parser.T.next.type == "CLOSE_PAR":
                    Parser.T.selectNext()
                    if Parser.T.next.type == "LINE_FEED":
                        Parser.T.selectNext()
                        # no_noop = NoOp(value="barra_n", children=[])
                    else:
                        raise SyntaxError(f"Precisa ter um /n depois de dar um print")
                    return no_print
                else:
                    raise SyntaxError(f"Voce esqueceu de fechar o parenteses do print")
            else:
                raise SyntaxError(f"precisa ter um parenteses depois de um print")

        elif Parser.T.next.type == "VAR":
            Parser.T.selectNext()
            if Parser.T.next.type == "IDENTIFIER":
                identifier = Parser.T.next.value
                Parser.T.selectNext()
                type = "int"
                if Parser.T.next.type == "TYPE":
                    type = Parser.T.next.value
                    Parser.T.selectNext()

            else:
                raise SyntaxError(
                    f"Na hora de declarar uma variavel depois de um var precisa de um indentifier"
                )
            if Parser.T.next.type == "EQUAL":
                Parser.T.selectNext()
                no_ident = Ident(value=str(identifier), children=[])
                no_dec = Dec(
                    value=type, children=[no_ident, Parser.parseBiexpression(st=st)]
                )
            else:
                no_ident = Ident(value=str(identifier), children=[])
                no_dec = Dec(value=type, children=[no_ident])
            if Parser.T.next.type == "LINE_FEED":
                # precisa ter o /n
                Parser.T.selectNext()
            return no_dec

        elif Parser.T.next.type == "FOR":
            Parser.T.selectNext()
            no_whilee = While(
                value="for_while",
                children=[
                    Parser.parseBiexpression(st=st),
                    Parser.parseBlock(st=st),
                ],
            )
            if Parser.T.next.type == "LINE_FEED":
                # precisa ter o /n
                Parser.T.selectNext()
            return no_whilee

        elif Parser.T.next.type == "IF":
            Parser.T.selectNext()
            cond = Parser.parseBiexpression(st=st)
            no_if = If(
                value="if",
                children=[cond, Parser.parseBlock(st=st)],
            )
            if Parser.T.next.type == "ELSE":
                Parser.T.selectNext()
                no_if.children.append(Parser.parseBlock(st=st))
            if Parser.T.next.type == "LINE_FEED":
                Parser.T.selectNext()
            else:
                raise SyntaxError("Esperado quebra de linha após condicional do if")

            return no_if

        elif Parser.T.next.type == "LINE_FEED":
            no_noop = NoOp(value="barra_n", children=[])
            Parser.T.selectNext()
            return no_noop

        elif Parser.T.next.type == "RETURN":
            Parser.T.selectNext()
            no_biexpression = Parser.parseBiexpression(st=st)
            no_return = Return(value=None, children=[no_biexpression])
            if Parser.T.next.type == "LINE_FEED":
                Parser.T.selectNext()
            else:
                raise SyntaxError("Esperado quebra de linha após condicional do if")
            return no_return
        elif Parser.T.next.type == "OPEN_BRA":
            no_block = Parser.parseBlock(st=st)
            return no_block
        else:
            raise SyntaxError(f"Caracter invalido : {Parser.T.next.value} ")

    @staticmethod
    def parseBlock(st):
        if Parser.T.next.type == "OPEN_BRA":
            Parser.T.selectNext()
            if Parser.T.next.type == "LINE_FEED":
                Parser.T.selectNext()
                no_noop = NoOp(value="barra_n", children=[])
                filhos_block = []
                filhos_block.append(no_noop)
                while Parser.T.next.type not in ["CLOSE_BRA"]:
                    resultado = Parser.parseStatement(st=st)
                    filhos_block.append(resultado)
                Parser.T.next.type == "CLOSE_BRA"
                Parser.T.selectNext()
            else:
                raise SyntaxError(
                    "Depois de iniciar um programa precisa ter um barra n depois do  '{'"
                )
        else:
            raise SyntaxError("Precisa iniciar o seu programa com um '{'")
        no = Block(value="block", children=filhos_block)
        return no

    def parseVarDec(st):
        if Parser.T.next.type == "VAR":
            Parser.T.selectNext()
        else:
            raise SyntaxError("sintaxe errada")

        if Parser.T.next.type == "IDENTIFIER":
            identifier = Parser.T.next.value
            Parser.T.selectNext()
        else:
            raise SyntaxError("sintaxe errada")
        tipo = "int"
        if Parser.T.next.type == "TYPE":
            tipo = Parser.T.next.value
            Parser.T.selectNext()

        if Parser.T.next.type != "EQUAL":
            no_ident = Ident(value=str(identifier), children=[])
            no_dec = Dec(value=tipo, children=[no_ident])
            # Parser.T.selectNext()
        else:
            # é igual a equal
            Parser.T.selectNext()
            no_ident = Ident(value=str(identifier), children=[])
            no_dec = Dec(
                value=tipo, children=[no_ident, Parser.parseBiexpression(st=st)]
            )
        return no_dec

    def parseFuncDec(st):
        filhos_funcdec = []
        if Parser.T.next.type == "FUNC":
            Parser.T.selectNext()
        else:
            raise SyntaxError("sintaxe errada")

        if Parser.T.next.type == "IDENTIFIER":
            identifier = Parser.T.next.value
            no_ident = Ident(value=str(identifier), children=[])
            filhos_funcdec.append(no_ident)
            Parser.T.selectNext()
        else:
            raise SyntaxError("sintaxe errada")

        if Parser.T.next.type != "OPEN_PAR":
            raise SyntaxError("Esperado '('")

        # ele é o open par
        Parser.T.selectNext()

        if Parser.T.next.type == "CLOSE_PAR":
            Parser.T.selectNext()  # Nenhum parâmetro
        else:
            while True:

                if Parser.T.next.type == "IDENTIFIER":
                    identifier = Parser.T.next.value
                    Parser.T.selectNext()
                else:
                    raise SyntaxError("Esperado IDENTIFIER")

                tipo = "int"
                if Parser.T.next.type == "TYPE":
                    tipo = Parser.T.next.value
                    Parser.T.selectNext()

                no_ident = Ident(value=str(identifier), children=[])
                no_dec = Dec(value=tipo, children=[no_ident])
                filhos_funcdec.append(no_dec)

                if Parser.T.next.type == "COMMA":
                    Parser.T.selectNext()
                elif Parser.T.next.type == "CLOSE_PAR":
                    Parser.T.selectNext()
                    break
                else:
                    raise SyntaxError("Esperado ',' ou ')' após parâmetros")
        tipo = "int"
        if Parser.T.next.type == "TYPE":
            tipo = Parser.T.next.value
            Parser.T.selectNext()

        no_block = Parser.parseBlock(st=st)
        filhos_funcdec.append(no_block)
        no_funcdec = FuncDec(value=str(tipo), children=filhos_funcdec)
        return no_funcdec

    def parseProgram(st):
        """"""
        filhos_block = []
        while Parser.T.next.type != "EOF":
            if Parser.T.next.type == "LINE_FEED":
                Parser.T.selectNext()
                no = NoOp(value="barra_n", children=[])
                filhos_block.append(no)
            elif Parser.T.next.type == "FUNC":
                no = Parser.parseFuncDec(st=st)
                filhos_block.append(no)
            elif Parser.T.next.type == "VAR":
                no = Parser.parseVarDec(st=st)
                filhos_block.append(no)
            else:
                raise SyntaxError(
                    "voce precisa iniciar o seu programa com uma função ou variavel"
                )
        no = Block(value="block", children=filhos_block)
        return no

    @staticmethod
    def run(code, st):
        """
        recebe o código fonte como argumento, inicializa um objeto Tokenizador, posiciona no primeiro token e retorna o resultado do prseExpression(). Ao final verificar se terminou de consumir toda a cadeia (o token deve ser EOF)
        """
        Parser.T = Tokenizer(source=PrePro.filter(code))
        ast = Parser.parseProgram(st=st)
        if Parser.T.next.type != "EOF":
            raise ValueError("não terminou de rodar a sintaxe")

        # --- Adiciona e executa o nó FuncCall para main ---
        child_texts = []
        for node in ast.children:
            if isinstance(node, FuncDec):
                child_texts.append(node.latexate(st=st))

        resultado = child_texts
        for idx, formula in enumerate(resultado, start=1):
            render_latex(formula, output_pdf=f"formula_{idx}.pdf")
        print(resultado)
        return resultado

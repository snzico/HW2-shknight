INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF'
)
BOOLEAN = 'BOOLEAN'
VAR = 'VAR'

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.
        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()
        
class AST(object):
    pass

# integer ****
class Num(AST): 
    def __init__(self, token):
        self.token = token
        self.value = token.value
        # print("num", self.token, self.value)

# booleans. true or false ****
class Bool(AST): 
    def __init__(self, token):
        self.token = token
        self.value = token.value
        
# locations(assignable variables) *****
class Var(AST): 
    def __init__(self, name):
        self.name = name
        self.value = 0

# all binary operations. {+, -, *, /, =, >, <, ∧, ∨} ***
class BinOp(AST): 
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

# **
class Neg(AST):
    def __init__(self, b):
        self.b = b

# x := e ****          
class Assign(AST): 
    def __init__(self, x, e):
        self.x = x
        self.e = e

# skip        
class Skip(AST):
    pass

# c1 ; c2 *         
class Comma(AST): 
    def __init__(self, left, right):
        self.left = left
        self.right = right
            
# if b then c1 else c2 ******
class If(AST): 
    def __init__(self, b, c1, c2):
        self.b = b
        self.c1 = c1
        self.c2 = c2
        
# while b do c *******
class While(AST): 
    def __init__(self, b, c):
        self.b = b
        self.c = c

class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        self.words = text.split()
        self.word_ind = 0
        self.current_word = self.words[self.word_ind]

    def error(self):
        print("invalid word", self.current_word)
        raise Exception('Invalid word')

    def advance(self):
        """Advance the `word_ind` pointer and set the `current_word` variable."""
        self.word_ind += 1
        if self.word_ind > len(self.words) - 1:
            self.current_word = None
        else:
            self.current_word = self.words[self.word_ind]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_word is not None:
            if (self.current_word.isnumeric() or self.current_word.strip('-').isnumeric()):
                n = int(self.current_word)
                self.advance()
                return Token(INTEGER, n)

            if self.current_word == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_word == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_word == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_word == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_word == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_word == ')':
                self.advance()
                return Token(RPAREN, ')')
                
            if self.current_word == ':=':
                self.advance()
                return Token(':=', ':=')
            
            if self.current_word == ';':
                self.advance()
                return Token(';', ';')
            
            if self.current_word == 'while':
                self.advance()
                return Token('while', 'while')
            
            if self.current_word == '¬':
                self.advance()
                return Token('¬', '¬')
            
            if self.current_word == '=':
                self.advance()
                return Token('=', '=')
            
            if self.current_word == 'do':
                self.advance()
                return Token('do', 'do')
            
            if self.current_word == '{':
                self.advance()
                return Token('{', '{')
                
            if self.current_word == 'if':
                self.advance()
                return Token('if', 'if')
            
            if self.current_word == '<':
                self.advance()
                return Token('<', '<')
                
            if self.current_word == 'then':
                self.advance()
                return Token('then', 'then')
                
            if self.current_word == 'else':
                self.advance()
                return Token('else', 'else')
                
            if self.current_word == '>':
                self.advance()
                return Token('>', '>')
                
            if self.current_word == '>=':
                self.advance()
                return Token('>=', '>=')
                
            if self.current_word == '<=':
                self.advance()
                return Token('<=', '<=')
                
            if self.current_word == 'false':
                self.advance()
                return Token(BOOLEAN, False)
            
            if self.current_word == 'true':
                self.advance()
                return Token(BOOLEAN, True)
            
            if self.current_word == 'skip':
                self.advance()
                return Token('skip', 'skip')
                
            if self.current_word == '∧':
                self.advance()
                return Token('∧', '∧')
                
            if self.current_word == '∨':
                self.advance()
                return Token('∨', '∨')
                
            if self.current_word == '}':
                self.advance()
                return Token('}', '}')
            
            if self.current_word.isidentifier():
                var = self.current_word
                self.advance()
                return Token(VAR, var)

            self.error()

        return Token(EOF, None)

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
    
    def factor(self):
        """factor : INTEGER 
        | LPAREN expr RPAREN
        | { expr }
        """
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        if token.type == LPAREN:
            self.eat(LPAREN)
            node = self.aexp()
            self.eat(RPAREN)
            return node
        if token.type == VAR:
            self.eat(VAR)
            return Var(token.value)
        
    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node
    
    def aexp(self):
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            node = BinOp(left=node, op=token, right=self.term())

        return node
    
    def bcmpr(self):
        if self.current_token.type == '¬':
            self.eat('¬')
            b = self.b_or()
            return Neg(b)
        if self.current_token.type == LPAREN:
            self.eat(LPAREN)
            node = self.b_or()
            self.eat(RPAREN)
            return node
        if self.current_token.type == BOOLEAN:
            b = Bool(self.current_token)
            self.eat(BOOLEAN)
            return b
        node = self.aexp()
        if self.current_token.type == '=':
            self.eat('=')
            return BinOp(left=node, op=Token('=', '='), right=self.aexp())
        if self.current_token.type == '<':
            self.eat('<')
            return BinOp(left=node, op=Token('<','<'), right=self.aexp())
        if self.current_token.type == '>':
            self.eat('>')
            return BinOp(left=node, op=Token('>','>'), right=self.aexp())
        if self.current_token.type == '<=':
            self.eat('<=')
            return BinOp(left=node, op=Token('<=','<='), right=self.aexp())
        if self.current_token.type == '>=':
            self.eat('>=')
            return BinOp(left=node, op=Token('>=','>='), right=self.aexp())

    def b_and(self):
        node = self.bcmpr()
        while self.current_token.type == '∧':
            self.eat('∧')
            node = BinOp(left=node, op=Token('∧','∧'), right=self.bcmpr())
        return node
        
    def b_or(self):
        """
        b_or   : b_and (∨ b_and)*
        b_and   : bterm (∧ bterm)*
        bterm   : bfactor ((< | =) bfactor)*
        bfactor : BOOLEAN | LPAREN expr RPAREN
        """
        node = self.b_and()
        if self.current_token.type == '∨':
            self.eat('∨')
            node = BinOp(left=node, op=Token('∨','∨'), right=self.b_and())
        return node

    def command(self):
        """ c ::=
        skip
        | x := e
        | if b then c1 else c2
        | while b do c
        """
        if self.current_token.type == '{':
            self.eat('{')
            c = self.comma_command()
            self.eat('}')
            return c
        if self.current_token.type == 'skip':
            self.eat('skip')
            return Skip()
        if self.current_token.type == 'if':
            self.eat('if')
            b = self.b_or()
            self.eat('then')
            c1 = self.comma_command()
            self.eat('else')
            c2 = self.comma_command()
            return If(b, c1, c2)
        if self.current_token.type == 'while':
            # print("current token:", self.current_token.type, self.current_token.value)
            self.eat('while')
            # print("current token:", self.current_token.type, self.current_token.value)
            b = self.b_or()
            # print(b, b.token, b.value)
            # print("current token:", self.current_token.type, self.current_token.value)
            self.eat('do')
            # print("current token:", self.current_token.type, self.current_token.value)
            c = self.command()
            # print(c)
            # print("current token:", self.current_token.type, self.current_token.value)
            return While(b, c)
        if self.current_token.type == VAR:
            x = Var(self.current_token.value)
            self.eat(VAR)
            self.eat(':=')
            e = self.aexp()
            return Assign(x, e)

    def comma_command(self):
        """ c ::= c1 ;c2 
        | { comm }"""
        node = self.command()
        while self.current_token.type == ';':
            self.eat(';')
            c2 = self.command()
            node =  Comma(node, c2)
        return node
    def parse(self):
        return self.comma_command()
        
class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.vars = {}
        self.report_vars = []

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.type == '=':
            return self.visit(node.left) == self.visit(node.right)
        elif node.op.type == '>':
            return self.visit(node.left) > self.visit(node.right)
        elif node.op.type == '<':
            return self.visit(node.left) < self.visit(node.right)
        elif node.op.type == '<=':
            return self.visit(node.left) <= self.visit(node.right)
        elif node.op.type == '>=':
            return self.visit(node.left) >= self.visit(node.right)
        elif node.op.type == '∧':
            return self.visit(node.left) and self.visit(node.right)
        elif node.op.type == '∨':
            return self.visit(node.left) or self.visit(node.right)

    def visit_Num(self, node):
        return node.value
    
    def visit_Bool(self, node):
        return node.value
    
    def visit_Var(self, node):
        if node.name not in self.vars:
            self.vars[node.name] = 0
        return self.vars[node.name]
    
    def visit_Neg(self, node):
        return not self.visit(node.b)
    
    def visit_Assign(self, node):
        name = node.x.name
        if name not in self.report_vars:
            self.report_vars.append(name)
        val = self.visit(node.e)
        self.vars[name] = val
        
    def visit_Skip(self, node):
        pass
        
    def visit_Comma(self, node):
        self.visit(node.left)
        self.visit(node.right)
        
    def visit_If(self, node):
        if self.visit(node.b):
            self.visit(node.c1)
        else:
            self.visit(node.c2)
        
    def visit_While(self, node):
        # print('b: ', self.visit(node.b))
        while self.visit(node.b):
            self.visit(node.c)

    def interpret(self):
        tree = self.parser.parse()
        self.visit(tree)
        s = '{'
        first = True
        self.report_vars.sort()
        for i in self.report_vars:
            if first == False:
                s += ', '
            first = False
            s += i
            s += ' → '
            s += str(self.vars[i])
        s += '}'
        return s
        
def eval(ast):
    interpreter = Interpreter(ast)
    return interpreter.interpret()

def main():
    text = input()
    lexer = Lexer(text)
    ast = Parser(lexer)
    print(eval(ast))


if __name__ == '__main__':
    main()

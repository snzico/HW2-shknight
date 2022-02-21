import locale

locale.getdefaultlocale()

LEFTPARENTHESIS, RIGHTPARENTHESIS, LEFTBRACKET, RIGHTBRACKET, LEFTBRACE, RIGHTBRACE, ADD, SUB, MUL, DIV, MOD, LESSTHAN, LESSTHANEQUALS, GREATERTHAN, GREATERTHANEQUALS, NOT, EQUAL, AND, OR, COLON, SEMICOLON, ASSIGN, WHILE, DO, SKIP, IF, THEN, ELSE, BOOL, TRUE, FALSE, VARIABLE, INTEGER, STRING, EOF = '(', ')', '[', ']', '{', '}', '+', '-', '*', '/', '%', '<', '<=', '>', '>=', '¬', '=', '∧', '∨', ':', ';', ":=", "while", "do", "skip", "if", "then", "else", "bool", "true", "false", "identifier", "integer", "string", "EOF"

def get_constants_dictionary():
    keys = "LEFTPARENTHESIS, RIGHTPARENTHESIS, LEFTBRACKET, RIGHTBRACKET, LEFTBRACE, RIGHTBRACE, ADD, SUB, MUL, DIV, MOD, LESSTHAN, LESSTHANEQUALS, GREATERTHAN, GREATERTHANEQUALS, NOT, EQUAL, AND, OR, COLON, SEMICOLON, ASSIGN, WHILE, DO, SKIP, IF, THEN, ELSE, BOOL, TRUE, FALSE, VARIABLE, INTEGER, STRING, EOF".split(', ')
    values = "(, ), [, ], {, }, +, -, *, /, %, <, <=, >, >=, ¬, =, ∧, ∨, :, ;, :=, while, do, skip, if, then, else, bool, true, false, identifier, integer, string, EOF".split(', ')
    constants ={}

    for i in range(len(keys)):
        constants[keys[i]] = values[i]

    if len(constants) > 0:
        print("Constants: " + constants + "\n\n")
        return constants
    else:
        print("Constants empty.\n\n")
        return {}

class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        token_string = "\n--TOKEN  Token({type}, {value})  TOKEN--".format(type = self.type, value = self.value)
        return token_string

    def __repr__(self):
        return self.__str__()

class AST:
    pass

class Root_Node(AST):
    def __init__(self, left_child, right_child):
        self.left_child = left_child
        self.right_child = right_child

    def __str__(self):
        return "\n--ROOTNODE  Root_Node(Left Child: <  {}  >,\nRight Child: <  {}  >\n)  ROOTNODE--\n".format(repr(self.left_child), repr(self.right_child))

    def __repr__(self):
        return self.__str__()

# Unary_Node includes:
#   - Negated Values (i.e. Values prepended by 'Not' / ¬)
#       - operator = logical operator [¬], child = value
class Unary_Node(AST):
    def __init__(self, operator, child):
        self.operator = operator
        self.child = child

    def __str__(self):
        return "\n--UNARYNODE  Unary_Node(Operator: <  {operator}  >,\nChild: <  {child}  >\n)  UNARYNODE--\n".format(operator = self.operator, child = repr(self.child))

    def __repr__(self):
        return self.__str__()

# Binary_Node includes:
#   - Arithmetic Expressions
#       - operator = arithmetic operator [+, -, *, /, %], left_child = left operand, right_child = right operand
#   - Boolean Comparisons
#       - operator = boolean comparison operator [<, <=, >, >=], left_child = left operand, right_child = right operand
#   - Boolean Expressions
#       - operator = logical operator [∧, ∨], left_child = left operand, right_child = right operand
#   - Assignments
#       - operator = assignment operand [:=], left_child = variable identifier, right_child = assigned value [numeric or identifier value]
class Binary_Node(AST):
    def __init__(self, operator, left_child, right_child):
        self.operator = operator
        self.left_child = left_child
        self.right_child = right_child

    def __str__(self):
        return "\n--BINARYNODE\n\tBinary_Node(Operator: <  {operator}  >,\n\tLeft Child: <  {left_child}  >,\n\tRight Child: <  {right_child}  >\n)  BINARYNODE--\n".format(operator = repr(self.operator), left_child = repr(self.left_child), right_child = repr(self.right_child))

    def __repr__(self):
        return self.__str__()



# Operand_Node includes:
#   - Number (Integer and Float) values
#   - Boolean literals
#   - Arithmetic
# Equivalent: Assign ****
#             Num    ****
#             Bool   ****
class Operand_Node(AST):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "\n--OPERANDNODE  Operand_Node(Type: <  {type}  >,\nValue: <  {value}  >\n)  OPERANDNODE--\n".format(type = self.type, value = self.value)

    def __repr__(self):
        return self.__str__()

# Variable_Node includes all variables
#   - When an alphanumeric identifier is found, a new instance is created
#   - Receives an identifier from lexer.get_next_token() case
#       - Initializes self.identifier to received identifier
#   - Initializes value to 0
#   - Updates self.value to variable value
class Variable_Node(AST):
    def __init__(self, identifier):
        self.identifier = identifier
        self.value = 0

    def __str__(self):
        return "\n--VARIABLENODE  Variable_Node(Identifier: <  {identifier}  >,\nValue: <  {value}  >\n)  VARIABLENODE--\n".format(identifier = self.identifier, value = self.value)

    def __repr__(self):
        return self.__str__()

class Skip_Node(AST):
    pass

    def __str__(self):
        return "\n--SKIPNODE Skip_Node{{pass}}  SKIPNODE--\n"

class If_Node(AST):
    def __init__(self, condition, true_branch, false_branch):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

    def __str__(self):
        return "\n--IFNODE  If_Node(Condition: <  {condition}  >,\nTrue Branch: <  {true_branch}  >,\nFalse Branch: <  {false_branch}  >\n)  IFNODE--\n".format(condition = str(self.condition), true_branch = str(self.true_branch), false_branch = str(self.false_branch))

    def __repr__(self):
        return self.__str__()

class While_Node(AST):
    def __init__(self, condition, block_statement):
        self.condition = condition
        self.block_statement = block_statement

    def __str__(self):
        return "\n--WHILENODE  While_Node(Condition: <  {condition}  >,\nBlock Statement: <  {block_statement}  >\n)  WHILENODE--\n".format(condition = str(self.condition), block_statement = str(self.block_statement))

    def __repr__(self):
        return self.__str__()

class Lexer(object):
    def __init__(self, input):
        self.input = input
        self.index = 0
        self.current = self.input[self.index]

    def advance(self):
        self.index = self.index + 1

        if (self.index > (len(self.input) - 1)):
            self.current = None
        else:
            self.current = self.input[self.index]

    def get_next_token(self):
        while self.current is not None:
            if (self.current.isnumeric() or self.current.strip('-').isnumeric()):
                value = int(self.current)
                self.advance()
                return Token(INTEGER, value)

            if (self.current == '('):
                self.advance()
                return Token(LEFTPARENTHESIS, '(')

            if (self.current == ')'):
                self.advance()
                return Token(RIGHTPARENTHESIS, ')')

            if (self.current == '{'):
                self.advance()
                return Token(LEFTBRACE, '{')

            if (self.current == '}'):
                self.advance()
                return Token(RIGHTBRACE, '}')

            if (self.current == '+'):
                self.advance()
                return Token(ADD, '+')

            if (self.current == '-'):
                self.advance()
                return Token(SUB, '-')

            if (self.current == '*'):
                self.advance()
                return Token(MUL, '*')

            if (self.current == '/'):
                self.advance()
                return Token(DIV, '/')

            if (self.current == '%'):
                self.advance()
                return Token(MOD, '%')

            if (self.current == '<'):
                self.advance()
                return Token(LESSTHAN, '<')

            if (self.current == '<='):
                self.advance()
                return Token(LESSTHANEQUALS, '<=')

            if (self.current == '>'):
                self.advance()
                return Token(GREATERTHAN, '>')

            if (self.current == '>='):
                self.advance()
                return Token(GREATERTHANEQUALS, '>=')

            if (self.current == '¬'):
                self.advance()
                return Token(NOT, '¬')

            if (self.current == '='):
                self.advance()
                return Token(EQUAL, '=')

            if (self.current == '∧'):
                self.advance()
                return Token(AND, '∧')

            if (self.current == '∨'):
                self.advance()
                return Token(OR, '∨')

            if (self.current == ':='):
                self.advance()
                return Token(ASSIGN, ':=')

            if (self.current == ';'):
                self.advance()
                return Token(SEMICOLON, ';')

            if (self.current == 'while'):
                self.advance()
                return Token(WHILE, 'while')

            if (self.current == 'do'):
                self.advance()
                return Token(DO, 'do')

            if (self.current == 'if'):
                self.advance()
                return Token(IF, 'if')

            if (self.current == 'then'):
                self.advance()
                return Token(THEN, 'then')

            if (self.current == 'else'):
                self.advance()
                return Token(ELSE, 'else')

            if (self.current == 'true'):
                self.advance()
                return Token(BOOL, True)

            if (self.current == 'false'):
                self.advance()
                return Token(BOOL, False)

            if (self.current == 'skip'):
                self.advance()
                return Token(SKIP, 'skip')

            if (self.current.isidentifier()):
                identifier = self.current
                self.advance()
                return Token(VARIABLE, identifier)

        return Token(EOF, None)

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current = self.lexer.get_next_token()


    def parse(self):
        return self.build_scope()

    def advance(self):
        self.current = self.lexer.get_next_token()

    def advance_after_verification(self, token_type):
        if (self.current.type) == token_type:
            self.advance()

    def build_variable(self, identifier):
        current_node = Variable_Node(identifier = identifier)


        self.advance_after_verification(VARIABLE)

        return current_node

    def build_factor(self):
        current_token_type = self.current.type
        current_value = self.current.value

        if current_token_type in [INTEGER, BOOL]:
            if current_token_type == INTEGER:
                self.advance_after_verification(INTEGER)
            else:
                self.advance_after_verification(BOOL)


            return Operand_Node(current_token_type, current_value)

        elif current_token_type == LEFTPARENTHESIS:


            return current_node

        elif current_token_type == VARIABLE:
            return self.build_variable(current_value)

    def build_term(self):
        current_node = self.build_factor()
        # current_token_type = self.current.type
        # current_token_value = self.current.value

        while self.current.type in [MUL, DIV]:
            current_token = self.current

            if self.current.type is MUL:
                self.advance_after_verification(MUL)
            else:
                self.advance_after_verification(DIV)

            current_node = Binary_Node(operator = current_token, left_child = current_node, right_child = self.build_factor())

        return current_node

    def build_arithmetic_expression(self):
        current_node = self.build_term()

        while self.current.type in [ADD, SUB]:
            current_token_type = self.current.type
            current_token_value = self.current.value

            if current_token_type == ADD:
                self.advance_after_verification(ADD)
            else:
                self.advance_after_verification(SUB)

            current_node = Binary_Node(operator = Token(current_token_type, current_token_value), left_child = current_node, right_child = self.build_term())

        return current_node

    def build_boolean_comparison(self):
        if self.current.type == NOT:
            self.advance_after_verification(NOT)
            value = self.build_boolean_expression()


            return Unary_Node(operator = NOT, child = value)

        elif (self.current.type) is LEFTPARENTHESIS:
            self.advance_after_verification(LEFTPARENTHESIS)

            current_node = self.build_boolean_expression()

            self.advance_after_verification(RIGHTPARENTHESIS)

            return current_node

        current_node = self.build_arithmetic_expression()

        while self.current.type in [EQUAL, LESSTHAN, LESSTHANEQUALS, GREATERTHAN, GREATERTHANEQUALS]:
            current_token = self.current

            self.advance_after_verification(current_token.type)

            current_node = Binary_Node(operator = current_token, left_child = current_node, right_child = self.build_arithmetic_expression())

        return current_node

    def build_boolean_expression(self):
        current_node = self.build_boolean_comparison()

        while self.current.type in [AND, OR]:
            current_token = self.current
            self.advance_after_verification(current_token.type)

            current_node = Binary_Node(operator = current_token, left_child = current_node, right_child = self.build_boolean_expression())

        return current_node

    def build_statement(self):
        if self.current.type == SKIP:
            self.advance_after_verification(SKIP)
            return Skip_Node()
        if self.current.type == LEFTBRACE:
            self.advance_after_verification(LEFTBRACE)
            scope = self.build_scope()
            self.advance_after_verification(RIGHTBRACE)
            return scope
        if self.current.type == IF:
            self.advance_after_verification(IF)
            return self.build_if_statement()
        if self.current.type == WHILE:
            self.advance_after_verification(WHILE)
            return self.build_while_statement()
        if self.current.type == VARIABLE:
            return self.build_assignment_statement()

    def build_assignment_statement(self):
        left_child = self.build_variable(self.current.value)

        operator = Operand_Node(ASSIGN, ':=')
        self.advance_after_verification(ASSIGN)

        right_child = self.build_boolean_expression()
        left_child.value = right_child


        return Binary_Node(operator, left_child, right_child)

    def build_if_statement(self):
        false_branch = None

        condition = self.build_boolean_expression()

        self.advance_after_verification(THEN)
        true_branch = self.build_scope()

        if (self.current.type == ELSE):
            self.advance_after_verification(ELSE)
            false_branch = self.build_scope()


        return If_Node(condition, true_branch, false_branch)

    def build_while_statement(self):
        condition = self.build_boolean_expression()

        self.advance_after_verification(DO)
        block_statement = self.build_statement()



        return While_Node(condition, block_statement)

    # Function build_scope(self):
    # Receives variable it is called by
    #   - Should be interpreter (variable of type Interpreter) in main()
    # Returns root_node of AST
    #
    # Works by determing the scope
    #   - Calling function .build_scope_list() on interpreter
    #   - During the first step of .build_scope_list(), interpreter is passed to .build_statement()
    #   - This continues (call of next function during 1st step of current function) until .build_factor() is reached
    #   - After the list of nodes in the interpreter are worked through, the root_node is returned, having had its
    def build_scope(self):
        current_node = self.build_statement()

        while self.current.type == SEMICOLON:
            self.advance_after_verification(SEMICOLON)
            next_statement = self.build_scope()
            current_node = Root_Node(current_node, next_statement)

        return current_node

class Interpreter(object):
    def __init__(self, parser):
        self.parser = parser
        self.root_node = parser.parse()
        self.scope = {}
        self.variables = []

    def evaluate(self):
        second_section = False
        return_value = self.visit_node(self.root_node)

        self.variables.sort()

        return_value = "{"

        for section in self.variables:

            if (second_section):
                return_value = ", "

            return_value += str(section) + ' → ' + str(self.scope[section])
            second_section = True

        return_value += "}\n\n"

        print(return_value)
        return return_value

    def visit_node(self, node):
        node_type = type(node)

        match_type = {
            Root_Node: self.visit_root_node,
            Unary_Node: self.visit_unary_node,
            Binary_Node: self.visit_binary_node,
            Operand_Node: self.visit_operand_node,
            Variable_Node: self.visit_variable_node,
            Skip_Node: self.visit_skip_node,
            If_Node: self.visit_if_node,
            While_Node: self.visit_while_node
        }

        returnValue = match_type[node_type](node)
        print("Node: " + repr(node) + "\nSent to function " + str(match_type[node_type]) + "\nNode type: " + str(node_type) + "\nReturn Value: " + str(returnValue) + "\n\n")
        return returnValue

    def visit_root_node(self, node):
        self.visit_node(node.left_child)
        self.visit_node(node.right_child)

    def visit_unary_node(self, node):
        if (node.operator == NOT):
            return not self.visit_node(node.child)

    def visit_binary_node(self, node):
        node_operation = node.operator.value

        if (str(node_operation) == ASSIGN):
            identifier = node.left_child.identifier

            if (identifier not in self.scope):
                self.variables.append(identifier)

            value = self.visit_node(node.right_child)
            self.scope[identifier] = value
            return

        left_operand = self.visit_node(node.left_child)
        right_operand = self.visit_node(node.right_child)

        match_operation = {
            ADD: (lambda: int(left_operand) + int(right_operand)),
            SUB: (lambda: int(left_operand) - int(right_operand)),
            MUL: (lambda: int(left_operand) * int(right_operand)),
            DIV: (lambda: int(left_operand) / int(right_operand)),
            MOD: (lambda: int(left_operand) % int(right_operand)),
            AND: (lambda: bool(left_operand) and bool(right_operand)),
            OR: (lambda: bool(left_operand) or bool(right_operand)),
            EQUAL: (lambda: int(left_operand) == int(right_operand)),
            LESSTHAN: (lambda: int(left_operand) < int(right_operand)),
            LESSTHANEQUALS: (lambda: int(left_operand) <= int(right_operand)),
            GREATERTHAN: (lambda: int(left_operand) > int(right_operand)),
            GREATERTHANEQUALS: (lambda: int(left_operand) >= int(right_operand)),
        }

        boop

        return match_operation[node_operation]()

    def visit_operand_node(self, node):
        return node.value

    def visit_variable_node(self, node):
        if node.identifier not in self.scope:
            self.scope[node.identifier] = 0
        return self.scope[node.identifier]

    def visit_skip_node(self, node):
        pass

    def visit_if_node(self, node):
        if (self.visit_node(node.condition)):
            return self.visit_node(node.true_branch)
        else:
            return self.visit_node(node.false_branch)

    def visit_while_node(self, node):
        while (self.visit_node(node.condition)):
            self.visit_node(node.block_statement)

def main():
    user_input = 'while ( ¬ ( 0 - -1 < 2 + z ) ) do skip ; while -1 * IY = 2 - L ∧ 0 + x < 2 + 2 do while ( ¬ ( z + S = z - -1 ) ) do if ( false ∨ NT + -3 = 3 ) then y := k * 0 else y := 0 - y'.split()
    lexer = Lexer(user_input)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    interpreter.evaluate()

if __name__ == "__main__":
    main()

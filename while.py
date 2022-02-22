import locale

locale.getdefaultlocale()

# Declaration and Initialization of Global Variables
# Each variable represents a TokenType
LEFTPARENTHESIS, RIGHTPARENTHESIS, LEFTBRACKET, RIGHTBRACKET, LEFTBRACE, RIGHTBRACE, ADD, SUB, MUL, DIV, MOD, LESSTHAN, LESSTHANEQUALS, GREATERTHAN, GREATERTHANEQUALS, NOT, EQUAL, AND, OR, COLON, SEMICOLON, ASSIGN, WHILE, DO, SKIP, IF, THEN, ELSE, BOOL, TRUE, FALSE, VARIABLE, INTEGER, STRING, EOF = '(', ')', '[', ']', '{', '}', '+', '-', '*', '/', '%', '<', '<=', '>', '>=', '¬', '=', '∧', '∨', ':', ';', ":=", "while", "do", "skip", "if", "then", "else", "bool", "true", "false", "identifier", "integer", "string", "EOF"

# Token includes each alphanumeric value, delimited by spaces, inputted via stdin by user
# Token(type, value)
# Receives:
#   - Token.type is the relevant label (see global variables) for inputted token
#   - Token.value is the inputted value
class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        token_string = "\n--TOKEN  Token({type}, {value})  TOKEN--".format(type = self.type, value = self.value)
        return token_string

    def __repr__(self):
        return self.__str__()

# AST is no-op (pass) parent of each *_Node type
class AST:
    pass

# Root_Node is the root node of the AST
# Root_Node(left_child, right_child)
# Receives:
#   - left_child is a *_Node or Token object that represents the immediate child node along the left edge of Root_Node
#   - right_child is a *_Node or Token object that represents the immediate child node along the right edge of Root_Node
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
# Unary_Node(operator, child)
# Receives:
#   - operator is a string that represents the operator used in the evaluation of the expression represented by the parameters of the Unary_Node
#   - child is a *_Node or Token which represents the Unary_Node's value
class Unary_Node(AST):
    def __init__(self, operator, child):
        self.operator = operator
        self.child = child

    def __str__(self):
        return "\n--UNARYNODE  Unary_Node(Operator: <  {operator}  >,\nChild: <  {child}  >\n)  UNARYNODE--\n".format(operator = self.operator, child = repr(self.child))

    def __repr__(self):
        return self.__str__()

# Binary_Node includes:
#   - Arithmetic Expressions (operator = arithmetic operator [+, -, *, /, %], left_child = left operand, right_child = right operand)
#   - Boolean Comparisons (operator = boolean comparison operator [<, <=, >, >=], left_child = left operand, right_child = right operand)
#   - Boolean Expressions (operator = logical operator [∧, ∨], left_child = left operand, right_child = right operand)
#   - Assignments (operator = assignment operator [:=], left_child = variable identifier, right_child = assigned value [numeric or identifier value])
# Binary_Node(operator, left_child, right_child)
# Receives:
#   - operator is an Operand_Node (for Assignment [:=]) or Token that represents the operator used in the evaluation of the expression represented by the parameters of the Binary_Node
#   - left_child is a *_Node or Token object that represents the immediate child node along the left edge of Binary_Node
#   - right_child is a *_Node or Token object that represents the immediate child node along the right edge of Binary_Node
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
#   - Assignment Operator
# Operand_Node(type, value)
# Receives:
#   - type represents the relevant TokenType of the Token used to initialize new instance of Operand_Node
#   - value represents the value of the Token (provided by user via stdin) used to initialize new instance of Operand_Node
class Operand_Node(AST):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "\n--OPERANDNODE  Operand_Node(Type: <  {type}  >,\nValue: <  {value}  >\n)  OPERANDNODE--\n".format(type = self.type, value = self.value)

    def __repr__(self):
        return self.__str__()

# Variable_Node includes all variables
#   - Lexer.get_next_token() employs builtin isidentifier() function to determine when an alphanumeric identifier is found
# Variable_Node(identifier, value)
# Receives an identifier from lexer.get_next_token() case
#   - identifier represents the alphanumeric identifier (name / placeholder) of the variable
# Value is initialized to 0
# Value is updated to variable value when Assignment Statement (variable := [value]) in Parser.build_assignment_statement (from Parser.build_statement() < Parser.build_scope() < Parser.parse())
class Variable_Node(AST):
    def __init__(self, identifier):
        self.identifier = identifier
        self.value = 0

    def __str__(self):
        return "\n--VARIABLENODE  Variable_Node(Identifier: <  {identifier}  >,\nValue: <  {value}  >\n)  VARIABLENODE--\n".format(identifier = self.identifier, value = self.value)

    def __repr__(self):
        return self.__str__()

# Skip_Node includes Skip statements found in conditional statements
# Skip_Node()
# Receives:
#   - No values received at or after initialization
class Skip_Node(AST):
    pass

    def __str__(self):
        return "\n--SKIPNODE Skip_Node{{pass}}  SKIPNODE--\n"

# If_Node represents If (Conditional Command) Statements
# If_Node(condition, true_branch, false_branch)
# Receives:
#   - condition represents the conditional statement that is evaluated following an If token encounter
#   - true_branch is a *_Node that represents the statement(s) executed when condition evaluates to True
#   - false_branch is a *_Node that represents the statement(s) executed when condition evaluates to False
class If_Node(AST):
    def __init__(self, condition, true_branch, false_branch):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch

    def __str__(self):
        return "\n--IFNODE  If_Node(Condition: <  {condition}  >,\nTrue Branch: <  {true_branch}  >,\nFalse Branch: <  {false_branch}  >\n)  IFNODE--\n".format(condition = str(self.condition), true_branch = str(self.true_branch), false_branch = str(self.false_branch))

    def __repr__(self):
        return self.__str__()

# While_Node represents While (Loop) Statements
# While_Node(condition, block_statement)
# Receives:
#   - condition represents the conditional statement that is evaluated following a While token encounter until the condition evaluates to False
#   - block_statement represents the statement(s) evaluated while the condition evaluates to True
class While_Node(AST):
    def __init__(self, condition, block_statement):
        self.condition = condition
        self.block_statement = block_statement

    def __str__(self):
        return "\n--WHILENODE  While_Node(Condition: <  {condition}  >,\nBlock Statement: <  {block_statement}  >\n)  WHILENODE--\n".format(condition = str(self.condition), block_statement = str(self.block_statement))

    def __repr__(self):
        return self.__str__()

# Lexer receives user input as a list of values that can include any value represented by a Global Variables listed above
# Lexer(input)
# Receives:
#   - input represents user input via stdin that is split at every space value before passing to Lexer initialization
class Lexer(object):
    def __init__(self, input):
        self.input = input
        self.index = 0
        self.current = self.input[self.index]

    # Lexer.index is incremented by 1
    # If Lexer.index is in the bounds of Lexer.input, the current element to be tokenized is set to the next value in Lexer.input
    # If Lexer.index is out of bounds of Lexer.input, the current element is set to None, to break the while loop in Lexer.get_next_token()
    def advance(self):
        self.index = self.index + 1

        if (self.index > (len(self.input) - 1)):
            self.current = None
        else:
            self.current = self.input[self.index]

    # Lexer.current is compared to each Global Variable by value
    # Should a match be found, a relevant Token() is created
    # A while loop is used to ensure each value passed to Lexer.input is evaluated and tokenized
    # When Lexer.advance returns None, the while loop is broken, and Token(EOF, None) [signifying End Of File] is returned
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
# Parser iterates through the tokens in Lexer and parses an AST relative to the precedence of each token and its fields
# Parser(lexer)
# Receives:
#   - lexer represents an instance of the Lexer class that has been initialized with user_input via stdin that has been split at each space
class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current = self.lexer.get_next_token()

    # Begin parsing of first (and possibly only) Scope
    def parse(self):
        return self.build_scope()

    # Set current Token to the value returned by lexer.get_next_token() and received by Parser.lexer field
    def advance(self):
        self.current = self.lexer.get_next_token()

    # Verify that the source TokenType is equivalent to the destination TokenType before assign next token from Parser.lexer to Parser.current
    def advance_after_verification(self, token_type):
        if (self.current.type) == token_type:
            self.advance()

    # An Assignment Operator or Variable Identifier has been encountered
    # Builds a Variable_Node with received identifier
    def build_variable(self, identifier):
        current_node = Variable_Node(identifier = identifier)
        self.advance_after_verification(VARIABLE)

        return current_node

    # Called from Parser.build_term(), at first line of .build_term(), or during creation of Binary_Node() for MUL or DIV
    # First build_* function executed completely
    # An Integer Literal [0 - 9] or Boolean Literal [true, false] token has been encountered
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

    # Called from Parser.build_arithmetic_expression(), at first line of .build_arithmetic_expression(), or during creation of Binary_Node() for ADD or SUB
    # Second build_* function executed completely
    # An Arithmetic Operator [MUL, DIV] has been encountered
    def build_term(self):
        current_node = self.build_factor()

        while self.current.type in [MUL, DIV]:
            current_token = self.current

            if self.current.type is MUL:
                self.advance_after_verification(MUL)
            else:
                self.advance_after_verification(DIV)

            current_node = Binary_Node(operator = current_token, left_child = current_node, right_child = self.build_factor())

        return current_node

    # Called from Parser.build_boolean_comparison() function, after self.current is tested against NOT and LEFTPARENTHESIS, or during creation of Binary_Node() for a Boolean Comparison Operator
    # Third build_* function executed completely
    # An Arithmetic Operator [ADD, SUB] has been encountered
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

    # Called from Parser.build_boolean_expression() function, at first like of .build_boolean_expression()
    # Fourth build_* function executed completely
    # A Boolean Comparison Operator [<, <=, >, >=] has been encountered
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

    # Called from Parser.build_boolean_comparison() when self.current is [NOT, LEFTPARENTHESIS],
    #   Parser.build_boolean_expression() during creation of Binary_Node() for [AND, OR],
    #   Parser.build_assignment_statement() during creation of Binary_Node for ASSIGN,
    #   or Parser.build_if_statement() / Parser.build_while_statement() as condition during creation of [If_Node, While_Node]
    # Fifth build_* function executed completely
    # A Boolean Expression Operator [AND, OR] has been encountered
    def build_boolean_expression(self):
        current_node = self.build_boolean_comparison()

        while self.current.type in [AND, OR]:
            current_token = self.current
            self.advance_after_verification(current_token.type)
            current_node = Binary_Node(operator = current_token, left_child = current_node, right_child = self.build_boolean_expression())

        return current_node

    # Called from Parser.build_while_statement() as block_statement during creation of While_Node,
    #   and from Parser.build_scope() to begin comparison of tokens
    # Seventh build_* function executed completely
    # A [SKIP, LEFTBRACE, IF, WHILE, VARIABLE] has been encountered
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

    # Called from Parser.build_statement() when VARIABLE token encountered
    # Sixth build_* function executed completely
    # A VARIABLE and ASSIGN (:=) have been encountered
    def build_assignment_statement(self):
        left_child = self.build_variable(self.current.value)
        operator = Operand_Node(ASSIGN, ':=')
        self.advance_after_verification(ASSIGN)
        right_child = self.build_boolean_expression()
        left_child.value = right_child

        return Binary_Node(operator, left_child, right_child)

    # Called from Parser.build_statement() when IF token encountered
    # Sixth build_* function executed completely
    # An IF, THEN and possibly ELSE have been encountered
    def build_if_statement(self):
        false_branch = None
        condition = self.build_boolean_expression()
        self.advance_after_verification(THEN)
        true_branch = self.build_scope()

        if (self.current.type == ELSE):
            self.advance_after_verification(ELSE)
            false_branch = self.build_scope()

        return If_Node(condition, true_branch, false_branch)

    # Called from Parser.build_statement() when WHILE token encountered
    # Sixth build_* function executed completely
    # A WHILE and DO token have been encountered
    def build_while_statement(self):
        condition = self.build_boolean_expression()
        self.advance_after_verification(DO)
        block_statement = self.build_statement()

        return While_Node(condition, block_statement)

    # Called from Parser.parse() to begin parsing a complete statement with a definite scope
    #   from Parser.build_statement() when LEFTBRACE encountered, signifying a solution statement (for comparison) has been encountered,
    #   from Parser.build_if_statement() when THEN encountered to create true_branch,
    #   from Parser.build_if_statement() if ELSE encountered to create false_branch,
    #   from Parser.build_scope() when SEMICOLON encountered, signifying end of nested statement and need for new sub-scope
    # Eighth and final build_* function executed completely
    # A SEMICOLON may have been encountered, or Parser.parse() was called immediately before function call
    def build_scope(self):
        current_node = self.build_statement()

        while self.current.type == SEMICOLON:
            self.advance_after_verification(SEMICOLON)
            next_statement = self.build_scope()
            current_node = Root_Node(current_node, next_statement)

        return current_node

# Interpreter parses the parser, and assigns the resultant AST Root_Node to root_node
# Interpreter then visits the Root_Node and each child, commencing a Depth-First Search of the entire AST
# Interpreter(parser)
# Receives:
#   - Instance of Parser Class, parser, used to assign children to each not from high precedence to
#     lowest, ensuring order of operations is followed during DFS in Interpreter.evaluate()
class Interpreter(object):
    def __init__(self, parser):
        self.parser = parser
        self.root_node = parser.parse()
        self.scope = {}
        self.variables = []

    # Called from main() following initialization of Interpreter
    # Function begins by visiting the Interpreter.root_node
    # After every node is visited, the values stored in Interpreter.variables
    # Receives:
    #   - No argument
    # Returns:
    #   - Solution set as return_value as string value
    def evaluate(self):
        second_section = False

        self.visit_node(self.root_node)
        self.variables.sort()

        return_value = "{"
        # Loop through each varriable stored in Interpreter.variables list
        # For input with multiple statements (scopes), a comma (', ') is inserted between solutions
        for variables in self.variables:

            if (second_section):
                return_value += ", "

            return_value += str(variable) + ' → ' + str(self.scope[variable])
            second_section = True

        return_value += "}"

        return return_value

    # Called from Interpreter.evaluate(), and each NodeType-specific visit_*_node statement
    # Function uses dictionary to match NodeType to relevant visit_*_node function call
    #   - Dictionary functions as an improvised switch statement
    # Sets the return_value to value returned by visit_*_node call
    # Receives:
    #   - node represents the node passed by Interpreter.evaluate() and / or node passed by Interpreter.visit_*_node()
    # Returns:
    #   - value derived from statement evaluation as return_value
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

        return_value = match_type[node_type](node)
        return return_value

    # Called from Interpreter.visit_node() match_type dictionary (improvised switch statement)
    # Calls Interpreter.visit_node() for each child of Root_Node
    # Receives:
    #   - Root_Node as node
    # Returns:
    #   - No value returned
    def visit_root_node(self, node):
        self.visit_node(node.left_child)
        self.visit_node(node.right_child)

    # Called from Interpreter.visit_node() match_type dictionary (improvised switch statement)
    # Calls Interpreter.visit_node() on node field child
    #   - If node field operator is NOT the value return by Interpreter.visit_node(node.child) is negated
    # Receives:
    #   - Unary_Node instance as node
    # Returns:
    #   - Negated value of expression evaluation of node
    def visit_unary_node(self, node):
        if (node.operator == NOT):
            return not self.visit_node(node.child)

    # Called from Interpreter.visit_node() match_type dictionary (improvised switch statement)
    # Checks if node operator is ASSIGN
    #   - If so, the expression represented by the node and it's children is evaluated accordingly
    #   - The identifier of the node is added to Interpreter.variables and the identifier/value pair are added to Interpreter.scope
    #   - Returns no value
    # Otherwise, Interpreter.visit_node() is called on both of node's children
    # Interpreter.visit_binary_node() match_type dictionary (improvised switch statement) is used to determine Binary Operation (Arithmetic or Boolean) used to evaluate expression represented by node and it's child(ren) (if any)
    # Receives:
    #   - Binary_Node instance as node
    # Returns:
    #   - The value calculated by the relevant Arithmetic or Boolean operation called using match_operation dictionary
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

        return match_operation[node_operation]()

    # Called from Interpreter.visit_node() match_type dictionary (improvised switch statement)
    # Simply returns value held in Operand_Node node's field value
    # Receives:
    #   - Operand_Node instance as node
    # Returns:
    #   - ASSIGN symbol - or - Integer or Boolean Literal value is Operand_Node node's field value
    def visit_operand_node(self, node):
        return node.value

    # Called from Interpreter.visit_node() match_type dictionary (improvised switch statement)
    # Sets identifier/value pair in Interpreter.scope if identifier is not found in Interpreter.scope
    # Gets value for node.identifier from Interpreter.scope
    # Receives:
    #   - Variable_Node instance as node
    # Returns:
    #   - Variable_Node node's field value
    def visit_variable_node(self, node):
        if node.identifier not in self.scope:
            self.scope[node.identifier] = 0
        return self.scope[node.identifier]

    # Called from Interpreter.visit_node() match_type dictionary (improvised switch statement)
    # Simply skips any instruction using 'pass' keyword
    # Receives:
    #   - Skip_Node instance as node
    # Returns:
    #   - No value returned
    def visit_skip_node(self, node):
        pass

    # Called from Interpreter.visit_node() match_type dictionary (improvised switch statement)
    # Runs Interpreter.visit_node(node.true_branch) if Interpreter.visit_node(node.condition) evaluates to true
    # Otherwise, runs Interpreter.visit_node(node.false_branch)
    # Receives:
    #   - If_Node instance as node
    # Returns:
    #   - Returned value of Interpreter.visit_node(*_branch) relevant to evaluation of Interpreter.visit_node(node.condition)
    def visit_if_node(self, node):
        if (self.visit_node(node.condition)):
            return self.visit_node(node.true_branch)
        else:
            return self.visit_node(node.false_branch)

    # Called from Interpreter.visit_node() match_type dictionary (improvised switch statement)
    # Uses while loop to continuously evaluate Interpreter.visit_node(node.block_statement) as long as Interpreter.visit_node(node.condition) evaluates to True
    # Receives:
    #   - While_Node instance as node
    # Returns:
    #   - Returned value of Interpreter.visit_node(node.block_statement)
    def visit_while_node(self, node):
        return_value = 0
        while (self.visit_node(node.condition)):
            return_value = self.visit_node(node.block_statement)
        return return_value

def main():
    user_input = 'while ( ¬ ( 0 - -1 < 2 + z ) ) do skip ; while -1 * IY = 2 - L ∧ 0 + x < 2 + 2 do while ( ¬ ( z + S = z - -1 ) ) do if ( false ∨ NT + -3 = 3 ) then y := k * 0 else y := 0 - y'.split()
    lexer = Lexer(user_input)
    parser = Parser(lexer)
    interpreter = Interpreter(parser)
    print(interpreter.evaluate())

if __name__ == "__main__":
    main()

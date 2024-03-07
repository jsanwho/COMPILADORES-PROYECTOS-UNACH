import ply.yacc as yacc
from analizadorlexico import tokens
from analizadorlexico import analizador

# resultado del analisis
resultado_gramatica = []

precedence = (
    ('right','ASIGNAR'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULT', 'DIV'),
    ('right', 'UMINUS'),
)
nombres = {}

def p_inicio(t):
    '''
    inicio : declaraciones
    '''
    t[0] = t[1]

def p_declaraciones(t):
    '''
    declaraciones : declaracion
                  | declaracion declaraciones
    '''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = [t[1]] + t[2]

def p_declaracion_asignar(t):
    'declaracion : IDENTIFICADOR ASIGNAR expresion PUNTOCOMA'
    nombres[t[1]] = t[3]
    t[0] = t[1]

def p_expresion_operaciones(t):
    '''
    expresion  :   expresion SUMA expresion
                |   expresion RESTA expresion
                |   expresion MULT expresion
                |   expresion DIV expresion
                |   expresion POTENCIA expresion
                |   expresion MODULO expresion
    '''
    if t[2] == '+':
        t[0] = t[1] + t[3]
    elif t[2] == '-':
        t[0] = t[1] - t[3]
    elif t[2] == '*':
        t[0] = t[1] * t[3]
    elif t[2] == '/':
        t[0] = t[1] / t[3]
    elif t[2] == '%':
        t[0] = t[1] % t[3]
    elif t[2] == '**':
        t[0] = t[1] ** t[3]

def p_expresion_uminus(t):
    'expresion : RESTA expresion %prec UMINUS'
    t[0] = -t[2]

def p_expresion_grupo(t):
    '''
    expresion  : PARIZQ expresion PARDER
                | LLAIZQ expresion LLADER
                | CORIZQ expresion CORDER
    '''
    t[0] = t[2]

def p_expresion_numero(t):
    'expresion : ENTERO'
    t[0] = t[1]

def p_expresion_nombre(t):
    'expresion : IDENTIFICADOR'
    try:
        t[0] = nombres[t[1]]
    except LookupError:
        print("Nombre desconocido ", t[1])
        t[0] = 0

def p_error(t):
    global resultado_gramatica
    if t:
        resultado = "Error sintáctico: Se esperaba un símbolo de cierre para '{}' en la línea {}".format(t.value, t.lineno)
        print(resultado)
        resultado_gramatica.append(resultado)
    else:
        resultado = "Error sintáctico: Error de sintaxis en la entrada"
        print(resultado)
        resultado_gramatica.append(resultado)

# Instanciamos el analizador sintáctico
parser = yacc.yacc()

def prueba_sintactica(data):
    global resultado_gramatica
    resultado_gramatica.clear()

    resultado = parser.parse(data)
    if resultado:
        resultado_gramatica.append(resultado)

    print("result: ", resultado_gramatica)
    return resultado_gramatica

if __name__ == '__main__':
    while True:
        try:
            s = input(' ingresa dato >>> ')
        except EOFError:
            continue
        if not s: continue

        prueba_sintactica(s)

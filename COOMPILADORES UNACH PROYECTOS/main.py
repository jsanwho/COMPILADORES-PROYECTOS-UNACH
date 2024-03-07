from flask import Flask, render_template, request
from analizadorlexico import prueba as lexico_prueba
from analizadorsintactico import prueba_sintactica

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analizar', methods=['POST'])
def analizar():
    codigo_fuente = request.form['codigo']
    
    # Ejecutar el análisis léxico y sintáctico
    resultados_lexico = lexico_prueba(codigo_fuente)
    resultados_sintactico = prueba_sintactica(codigo_fuente)
    
    return render_template('result.html', 
                           resultados_lexico=resultados_lexico, 
                           resultados_sintactico=resultados_sintactico)

if __name__ == '__main__':
    app.run(debug=True)


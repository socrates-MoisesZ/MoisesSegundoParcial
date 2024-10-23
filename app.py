from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
def index():
    productos = session.get('productos', [])
    return render_template('index.html', productos=productos)

@app.route('/productos', methods=['GET'])
def listar_productos():
    productos = session.get('productos', [])
    return render_template('index.html', productos=productos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nuevo_producto = {
            'id': request.form['id'],
            'nombre': request.form['nombre'],
            'cantidad': int(request.form['cantidad']),
            'precio': float(request.form['precio']),
            'fecha_vencimiento': request.form['fecha_vencimiento'],
            'categoria': request.form['categoria']
        }

        if 'productos' not in session:
            session['productos'] = []

        for producto in session['productos']:
            if producto['id'] == nuevo_producto['id']:
                return "El ID ya existe. Por favor, elige otro.", 400
        
        session['productos'].append(nuevo_producto)
        session.modified = True

        return redirect(url_for('index'))

    return render_template('agregar_producto.html')

@app.route('/editar/<string:id>', methods=['GET', 'POST'])
def editar_producto(id):
    productos = session.get('productos', [])
    producto = next((p for p in productos if p['id'] == id), None)

    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']
        session.modified = True
        return redirect(url_for('listar_productos'))

    return render_template('editar_producto.html', producto=producto)

@app.route('/eliminar/<string:id>', methods=['POST'])
def eliminar_producto(id):
    productos = session.get('productos', [])
    session['productos'] = [p for p in productos if p['id'] != id]
    session.modified = True
    return redirect(url_for('listar_productos'))

if __name__ == '__main__':
    app.run(debug=True)
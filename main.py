import psycopg2
from flask import Flask, jsonify, request

app = Flask(__name__)


def ejecutar_sql(sql_text, params=None):
    host = "localhost"
    port = "5432"
    dbname = "alexsoft"
    user = "postgres"
    password = "postgres"

    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            options="-c search_path=public"
        )

        cursor = connection.cursor()

        if params:
            cursor.execute(sql_text, params)
        else:
            cursor.execute(sql_text)

        # Si la consulta no devuelve resultados (como un INSERT)
        if cursor.description is None:
            connection.commit()
            cursor.close()
            connection.close()
            return None

        # Para consultas SELECT
        columnas = [desc[0] for desc in cursor.description]
        resultados = cursor.fetchall()
        datos = [dict(zip(columnas, fila)) for fila in resultados]

        cursor.close()
        connection.close()

        return datos

    except psycopg2.Error as e:
        print("Error:", e)
        return {"error": str(e)}, 500


@app.route('empleado/empleados', methods=['GET'])
def obtener_lista_empleados():
    query = 'SELECT * FROM public."Empleado" ORDER BY id ASC LIMIT 100'
    resultado = ejecutar_sql(query)
    if isinstance(resultado, tuple):
        return jsonify(resultado[0]), resultado[1]
    return jsonify(resultado)



@app.route('/proyecto/crear')
def crear_proyecto():









@app.route('gestor/login', methods=['POST'])
def login(user, passwd):
    body_request = request.json
    user = body_request["user"]
    passwd = body_request["passwd"]





@app.route('/proyecto/proyectos', methods=['GET'])
def obtener_proyectos():






@app.route('/proyecto/proyectos_activos', methods=['GET'])
def proyectos_activos():




@app.route('/proyecto/proyectos_gestor', methods=['GET'])
def obtener_proyectos_gestor_id():





if __name__ == '__main__':
    app.run(debug=True)

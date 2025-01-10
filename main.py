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


@app.route('/empleado/empleados', methods=['GET'])
def obtener_lista_empleados():
    query = 'SELECT * FROM public."Empleado" ORDER BY id ASC LIMIT 100'
    resultado = ejecutar_sql(query)
    if isinstance(resultado, tuple):
        return jsonify(resultado[0]), resultado[1]
    return jsonify(resultado)


@app.route('/gestor/login', methods=['POST'])
def login():
    body_request = request.json
    user = body_request["user"]
    passwd = body_request["passwd"]

    is_logged = ejecutar_sql(f" Select * from public.\"Gestor\" WHERE usuario = '{user}' and passwd = '{passwd}';")

    if len(is_logged) == 0:
        return jsonify({"msg": "login error"})
    empleado = ejecutar_sql(f" Select * from public.\"Empleado\" WHERE id = '{is_logged[0]["empleado"]}';")

    resultado = {
        "id_empleado": empleado[0]["id"],
        "id_gestor": is_logged[0]["id"],
        "nombre": empleado[0]["nombre"],
        "email": empleado[0]["email"],
    }

    return jsonify(resultado)


@app.route('/proyecto/crear', methods=['POST'])
def crear_proyecto():
    body_request = request.json
    id =body_request["id"]
    nombre = body_request["nombre"]
    descripcion = body_request["descripcion"]
    fecha_creacion = body_request["fecha_creacion"]
    fecha_inicio = body_request["fecha_inicio"]
    fecha_finalizacion = body_request["fecha_finalizacion"]
    cliente = body_request["cliente"]

    ejecutar_sql(
        f"INSERT INTO public.\"Proyecto\" VALUES ('{id}','{nombre}', '{descripcion}', '{fecha_creacion}', "
        f"'{fecha_inicio}', '{fecha_finalizacion}', {cliente});"
    )

    # if len(nombre | descripcion | fecha_creacion | fecha_inicio | cliente) == 0:
    #     return jsonify({"msg": "error al insertar proyecto"})

    return jsonify({"msg": "se insertó correctamente"})



@app.route("/gestor/proyecto", methods=["POST"])
def asignar_gestor_proyecto():
    body_request = request.json
    gestor = body_request["gestor"]
    proyecto = body_request["proyecto"]
    fecha_asignacion = body_request["fecha_asignacion"]

    ejecutar_sql(
        f"INSERT INTO public.\"GestoresProyecto\" VALUES ('{gestor}','{proyecto}','{fecha_asignacion}');"
    )
    if gestor ==0:
        return jsonify({"msg": "error al insertar"})

    return jsonify({"msg": "se insertó correctamente"})


# @app.route("/")
# def asignar_proyecto_existente():


@app.route("/proyecto/cliente", methods=['POST'])
def asignar_cliente_a_proyecto():
    body_request = request.json
    id_proyecto = body_request["id"]
    updatedcliente = body_request["updatedcliente"]

    ejecutar_sql(
        f"UPDATE public.\"Proyecto\" SET cliente = '{updatedcliente}' WHERE id = '{id_proyecto}';"
    )

    return jsonify({"msg": "se cambio correctamente el cliente"})


@app.route("/tarea/crear", methods=['POST'])
def crear_tareas_proyecto():
    body_request = request.json
    id = body_request["id"]
    nombre = body_request["nombre"]
    descripcion = body_request["descripcion"]
    estimacion = body_request["estimacion"]
    fecha_creacion = body_request["fecha_creacion"]
    fecha_finalizacion = body_request["fecha_finalizacion"]
    programador = body_request["programador"]
    proyecto = body_request["proyecto"]

    ejecutar_sql(
        f"INSERT INTO public.\"Tarea\" VALUES ('{id}','{nombre}', '{descripcion}','{estimacion}', '{fecha_creacion}', "
        f" '{fecha_finalizacion}', {programador},'{proyecto}');"
    )

    return jsonify({"msg": "Se asigno correctamente la tarea"})

# @app.route("/")
# def asignar_programador_a_proyecto(): #Tener en cuenta que el programador puede tener distinto precio a la hora
#
#
@app.route("/tarea/programador")
def asignar_programador_a_tarea():
    body_request = request.json
    id_tarea = body_request["id"]
    id_programador = body_request["id_programador"]

    ejecutar_sql(
        f"UPDATE public.\"Tarea\" SET programador = '{id_programador}' WHERE id = '{id_tarea}';"
    )

    return jsonify({"msg": "Se asigno correctamente el programador a la tarea"})

# @app.route("/")
# def calcular_horas_proyecto(): #definida en tareas
#
# @app.route("/")
# def añadir_extras_proyecto(): #artículos como: dominio, servidor, licencias, etc. (Tener en cuenta que cada artículo está asignado a un proveedor)
#
# @app.route("/")
# def calcular_presupuesto(): #contando las horas y con los datos de la empresa y del cliente.
#
#
# @app.route('/proyecto/proyectos', methods=['GET'])
# def obtener_proyectos():
#
#
#
#     return jsonify(
#         {
#             "id": proyecto.json[0]["id"],
#             "nombre": proyecto.json[0]["nombre"],
#             "descripcion": proyecto.json[0]["descripcion"],
#             "fecha_creacion": proyecto.json[0]["fecha_creacion"],
#             "fecha_inicio": proyecto.json[0]["fecha_inicio"],
#             "fecha_finalizacion": proyecto.json[0]["fecha_finalizacion"],
#             "cliente": proyecto.json[0]["cliente"],
#         }
#     )
#
#
# @app.route('/proyecto/proyectos_activos', methods=['GET'])
# def proyectos_activos():
#
#
#
#
# @app.route('/proyecto/proyectos_gestor', methods=['GET'])
# def obtener_proyectos_gestor_id():
#
#


if __name__ == '__main__':
    app.run(debug=True)

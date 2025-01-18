from flask import Flask, render_template, request, make_response, redirect, Blueprint
import requests
from .LibraryController import LibraryController

# Crear la aplicación Flask
app = Flask(__name__, static_url_path='', static_folder='../view/static', template_folder='../view/')
app.secret_key = "library"

library = LibraryController()

# === Configuración de OMDb API ===
OMDB_API_KEY = "773f7b1a"  # Sustituye esto con tu clave de API de OMDb
OMDB_API_URL = "http://www.omdbapi.com/"

@app.before_request
def get_logged_user():
    if '/css' not in request.path and '/js' not in request.path:
        token = request.cookies.get('token')
        time = request.cookies.get('time')
        if token and time:
            request.user = library.get_user_cookies(token, float(time))
            if request.user:
                request.user.token = token

@app.after_request
def add_cookies(response):
    if 'user' in dir(request) and request.user and request.user.token:
        session = request.user.validate_session(request.user.token)
        response.set_cookie('token', session.hash)
        response.set_cookie('time', str(session.time))
    return response

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/catalogue', methods=['GET', 'POST'])
def catalogue():
    if 'user' in dir(request) and request.user and request.user.token:
        title = request.values.get("title", "")
        page = int(request.values.get("page", 1))

        # Llamar a la API de OMDb para buscar películas
        params = {
            "s": title,
            "page": page,
            "apikey": OMDB_API_KEY
        }

        try:
            response = requests.get(OMDB_API_URL, params=params)
            if response.status_code == 200:
                data = response.json()
                movies = data.get("Search", [])
                total_results = int(data.get("totalResults", 0))
                total_pages = (total_results // 10) + (1 if total_results % 10 > 0 else 0)
            else:
                movies = []
                total_pages = 1
        except Exception as e:
            print(f"Error al realizar la solicitud a la API: {e}")
            movies = []
            total_pages = 1

    # Recomendaciones del sistema
        if 'user' in dir(request) and request.user and request.user.token:
            user = request.user
            recommended_movies = library.get_recommended_books(user)  # Reutilizamos la lógica de recomendaciones
        else:
            recommended_movies = []

        return render_template(
            'catalogue.html',
            movies=movies,
            title=title,
            current_page=page,
            total_pages=total_pages,
            recommended_movies=recommended_movies,
            max=max,
            min=min
        )
    else:
        return redirect('/login')  # Redirigir a catálogo si no es admin o no está logueado
        

@app.route('/profile')
def profile():
    if 'user' in dir(request) and request.user and request.user.token:
        user = request.user
        return render_template('profile.html')
    else:
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'user' in dir(request) and request.user and request.user.token:
		return redirect('/')
	email = request.values.get("email", "")
	password = request.values.get("password", "")
	user = library.get_user(email, password)
	if user:
		session = user.new_session()
		resp = redirect("/")
		resp.set_cookie('token', session.hash)
		resp.set_cookie('time', str(session.time))
	else:
		if request.method == 'POST':
			return redirect('/login')
		else:
			resp = render_template('login.html')
	return resp


@app.route('/logout')
def logout():
	path = request.values.get("path", "/")
	resp = redirect(path)
	resp.delete_cookie('token')
	resp.delete_cookie('time')
	if 'user' in dir(request) and request.user and request.user.token:
		request.user.delete_session(request.user.token)
		request.user = None
	return resp

# === Administracion ===

@app.route('/administrador')
def administrador():
	return render_template('administrador.html')

@app.route('/gestorUsuarios')
def gestorUsuarios():
	return render_template('gestorUsuarios.html')

@app.route('/crearUsuario', methods=['GET', 'POST'])
def crearUsuario():
	if request.method == 'POST':
		nombre = request.values.get("nombre")
		apellidos = request.values.get("apellidos")
		fecha_nac= request.values.get("fecha_nac")
		email = request.values.get("email")
		password = request.values.get("password")
		mensaje = library.add_user(nombre, apellidos, fecha_nac, email, password)
		return redirect('/msg?mensaje=' + mensaje) 
	else:
		return render_template('crearUsuario.html')
		
@app.route('/revisarUsuario', methods=['GET', 'POST'])
def revisarUsuario():
	usuariosP = library.get_userPlist()
	return render_template('revisarUsuario.html', pending_users=usuariosP)
	
@app.route('/aceptarUsuario', methods=['GET', 'POST'])
def aceptarUsuario():
	if request.method == 'POST':
		email = request.form.get("email")
		usuario = library.get_userP(email)
		usuario = usuario[0]
		mensaje = library.add_user(usuario[0], usuario[1], usuario[2], usuario[3], usuario[4])
		return redirect('/msg?mensaje=' + mensaje) 
	else:
		return render_template('revisarUsuario.html')
	
@app.route('/denegarUsuario', methods=['GET', 'POST'])
def denegarUsuario():
	if request.method == 'POST':
		email = request.form.get("email")
		mensaje = library.delete_userP(email)
		return redirect('/msg?mensaje=' + mensaje) 
	else:
		return render_template('revisarUsuario.html')
		
@app.route('/register', methods=['GET', 'POST'])
def regUsuario():
	if request.method == 'POST':
		nombre = request.values.get("nombre")
		apellidos = request.values.get("apellidos")
		fecha_nac= request.values.get("fecha_nac")
		email = request.values.get("email")
		password = request.values.get("password")
		mensaje = library.reg_user(nombre, apellidos, fecha_nac, email, password)
		return redirect('/msg?mensaje=' + mensaje) 
	else:
		return render_template('register.html')

@app.route('/editarPerfil', methods=['GET', 'POST'])
def editarUsuario():
	if request.method == 'POST':
		if 'user' in dir(request) and request.user and request.user.token:
			user = request.user
		nombre = request.values.get("nombre")
		apellidos = request.values.get("apellidos")
		fecha_nac= request.values.get("fecha_nac")
		email = request.values.get("email")
		password = request.values.get("password")
		print(request.user.email)
		userID = library.get_user2(request.user.email)
		print(userID.id)
		mensaje = library.edit_user(userID.id, nombre, apellidos, fecha_nac, email, password)
		return redirect('/msg?mensaje=' + mensaje) 
	else:
		return render_template('editarPerfil.html')
	
@app.route('/borrarUsuario', methods=['GET', 'POST'])
def borrarUsuario():
	if request.method == 'POST':
		email = request.form.get("email")
		mensaje = library.delete_user(email)
		return redirect('/msg?mensaje=' + mensaje)
	else:
		return render_template('borrarUsuario.html')
		
@app.route('/modificarUsuario', methods=['GET', 'POST'])
def editarADMINusuario():
	if request.method == 'POST':
		emailTarget = request.values.get("emailTarget")
		nombre = request.values.get("nombre")
		apellidos = request.values.get("apellidos")
		fecha_nac= request.values.get("fecha_nac")
		email = request.values.get("email")
		password = request.values.get("password")
		userID = library.get_user2(emailTarget)
		print(userID.id)
		mensaje = library.edit_user(userID.id, nombre, apellidos, fecha_nac, email, password)
		#mensaje = library.add_user(nombre, apellidos, fecha_nac, email, password)
		return redirect('/msg?mensaje=' + mensaje) 
	else:
		return render_template('modificarUsuario.html')

@app.route('/gestorLibros')
def gestorLibros():
	return render_template('gestorLibros.html')

@app.route('/añadirLibro', methods=['GET', 'POST'])
def añadirLibro():
	if request.method == 'POST':
		titulo = request.form.get("titulo")
		autor = request.form.get("autor")
		cover = request.form.get("cover")
		descripccion = request.form.get("descripcion")
		mensaje = library.add_book(titulo, autor, cover, descripccion)
		return redirect('/msg?mensaje=' + mensaje)
	else:
		return render_template('añadirLibro.html')

@app.route('/borrarLibro', methods=['GET', 'POST'])
def borrarLibro():
	if request.method == 'POST':
		titulo = request.form.get("titulo")
		autor = request.form.get("autor")
		mensaje = library.delete_book(titulo, autor)
		return redirect('/msg?mensaje=' + mensaje)
	else:
		return render_template('borrarLibro.html')
	
@app.route('/rental_catalogue')
def rental_catalogue():
	title = request.values.get("title", "")
	page = int(request.values.get("page", 1))
	# Llamar a la función de búsqueda de películas
	movies, nb_movies = library.search_movies(title=title, page=page - 1)
    
	# Calcular el total de páginas
	total_pages = (nb_movies // 6) + (1 if nb_movies % 6 > 0 else 0)
    
	return render_template('rental_catalogue.html', 
			movies=movies, 
			title=title, 
			current_page=page, 
			total_pages=total_pages)

@app.route('/rent_movie', methods=['POST'])
def rent_movie():
	if 'user' in dir(request) and request.user and request.user.token:
		movie_id = request.form.get("movie_id")
		user = request.user
		# Llamar a la función de alquiler de película
		message = library.rent_movie(user.id, movie_id)
		return redirect('/msg?mensaje=' + message)
	else:
		return redirect('/login')

@app.route('/rental_history')
def rental_history():
	if 'user' in dir(request) and request.user and request.user.token:
		user = request.user
		# Llamar a la función para obtener el historial de alquileres
		rentals = library.get_rental_history(user.id)
		return render_template('rental_history.html', rentals=rentals)
	else:
		return redirect('/login')


@app.route('/msg', methods=['GET'])
def mensaje():
	mensaje = request.values.get("mensaje","")
	return render_template('msg.html', mensaje=mensaje)

@app.route('/admin')
def admin():
    if 'user' in dir(request) and request.user and request.user.token:
        return render_template('admin.html')
    else:    
        return redirect('/login')  # Redirigir a catálogo si no es admin o no está logueado

@app.route('/accept_requested_movie', methods=['POST'])
def accept_requested_movie():
    if 'user' in dir(request) and request.user and request.user.token:
        try:
            # Obtener los datos de la película desde la solicitud JSON
            movie_data = request.get_json()
            movie = movie_data.get('movie')

            if movie:
                # Extraer solo el título y el año de la película
                title = movie.get('Title')
                year = movie.get('Year')

                if title and year:
                    # Llamar a la función que guarda el título y el año en la base de datos
                    message = library.add_movie(title, year)
                    return jsonify({"message": message}), 200
                else:
                    return jsonify({"message": "La película no contiene título o año válido"}), 400
            else:
                return jsonify({"message": "No se proporcionó película válida"}), 400
        except Exception as e:
            return jsonify({"message": f"Error: {str(e)}"}), 500
    else:
        return redirect('/login')
 
@app.route('/report_bug', methods=['POST'])
def report_bug():
	if 'user' in dir(request) and request.user and request.user.token:
		user = request.user
		movie_title = request.form.get("movie_title")
		bug_description = request.form.get("bug_description")
		message = library.report_bug(user.id, movie_title, bug_description)
		return redirect(f"/msg?mensaje={message}")
	else:
		return redirect('/login')
 
 
 
       
@app.route('/puntuaciones')
def puntuaciones():
	return render_template('puntuaciones.html')

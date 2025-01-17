import random
import hashlib
from model import Connection, Book, User
from model.tools import hash_password


db = Connection()
salt = "library"

class LibraryController:
	__instance = None

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = super(LibraryController, cls).__new__(cls)
			cls.__instance.__initialized = False
		return cls.__instance


	def search_books(self, title="", author="", limit=6, page=0):
		count = db.select("""
				SELECT count() 
				FROM Book b, Author a 
				WHERE b.author=a.id 
					AND b.title LIKE ? 
					AND a.name LIKE ? 
		""", (f"%{title}%", f"%{author}%"))[0][0]
		res = db.select("""
				SELECT b.* 
				FROM Book b, Author a 
				WHERE b.author=a.id 
					AND b.title LIKE ? 
					AND a.name LIKE ? 
				LIMIT ? OFFSET ?
		""", (f"%{title}%", f"%{author}%", limit, limit*page))
		books = [
			Book(b[0],b[1],b[2],b[3],b[4])
			for b in res
		]
		return books, count

	def get_user(self, email, password):
		user = db.select("SELECT * from User WHERE email = ? AND password = ?", (email, hash_password(password)))
		if len(user) > 0:
			return User(user[0][0], user[0][1], user[0][2], user[0][3], user[0][4], user[0][6])
		else:
			return None
			
	def get_user2(self, email):
		user = db.select("SELECT * from User WHERE email = ?", (email,))
		if len(user) > 0:
			return User(user[0][0], user[0][1], user[0][2], user[0][3], user[0][4], user[0][6])
		else:
			return None
			
	def get_userPlist(self):
		usuarios = db.select("SELECT name, last_name, birth_date, email FROM UserPendientes")
		return usuarios
		
		
	def get_userP(self, email):
		usuarios = db.select("SELECT name, last_name, birth_date, email, password FROM UserPendientes WHERE email = ?", (email,))
		return usuarios
	
			
	def reg_user(self, name, last_name, birth_date, email, password):
		if None == get_user2(email):
			try:
				dataBase_password = str(password) + salt
				hashed = hashlib.md5(dataBase_password.encode())
				dataBase_password = hashed.hexdigest()
				db.insert("INSERT INTO UserPendientes VALUES (NULL, ?, ?, ?, ?, ?, ?)", (name, last_name, birth_date, email, dataBase_password, 0))
				return("Usuario registrado correctamente")
			except:
				return("Usuario ya existe")

	def get_user_cookies(self, token, time):
		user = db.select("SELECT u.* from User u, Session s WHERE u.id = s.user_id AND s.last_login = ? AND s.session_hash = ?", (time, token))
		if len(user) > 0:
			return User(user[0][0], user[0][1], user[0][2], user[0][3], user[0][4], user[0][6])
		else:
			return None
	
	# === Administracion ===
	def add_user(self, name, last_name, birth_date, email, password):
		try:
			db.insert("INSERT INTO User VALUES (NULL, ?, ?, ?, ?, ?, ?)", (name, last_name, birth_date, email, password, 0))
			db.delete("DELETE FROM UserPendientes WHERE email = ?", (email,))
			return("Usuario aceptado correctamente")
		except:
			return("Usuario ya existe")
			
	def edit_user(self, userID, name, last_name, birth_date, email, password):
		try:
			dataBase_password = str(password) + salt
			hashed = hashlib.md5(dataBase_password.encode())
			dataBase_password = hashed.hexdigest()
			
			db.update("""
		        UPDATE User 
		        SET name = ?, last_name = ?, birth_date = ?, email = ?, password = ?
		        WHERE id = ?""", (name, last_name, birth_date, email, dataBase_password, userID))
			return "Usuario actualizado correctamente"
		except Exception as e:
        		return f"Error al actualizar el usuario: {str(e)}"

	def delete_user(self, email):
		id_user = db.select("SELECT id FROM User WHERE email = ?", (email,))
		if len(id_user) != 0 and id_user[0][0] != 1:			
			db.delete("DELETE FROM User WHERE email = ?", (email,))
			return("Usuario borrado correctamente")
		else:
			return("El email no existe o es admin")
	
	def delete_userP(self, email):
		try:
			db.delete("DELETE FROM UserPendientes WHERE email = ?", (email,))
			return("Usuario borrado correctamente")
		except:
			return("Usuario no existe")
		
	def add_book(self, title, author, cover, description):
		try:
			db.insert("INSERT INTO Author VALUES (NULL, ?)", (author,))
			author_id = db.select("SELECT id FROM Author WHERE name = ?", (author,))[0][0]
			db.insert("INSERT INTO Book VALUES (NULL, ?, ?, ?, ?)", (title, author_id, cover, description))
			return("El libro se ha añadido correctamente")
		except:
			return("El libro ya existe")

	def delete_book(self, title, author):
		try:
			author_id = db.select("SELECT id FROM Author WHERE name = ?", (author,))[0][0]
			book_id = db.select("SELECT id FROM Book WHERE title = ? AND author = ?", (title, author_id))[0][0]
			db.delete("DELETE FROM Book WHERE id = ?", (book_id,))
			return("El libro se ha borrado correctamente")
		except:
			return("El libro no existe")
		

		# === Recomendaciones de amigos===

	def recomendar_amigos(self, user=None, limite=3):
		# Lista de tus amigos
		lista_amigos = db.select("""SELECT * FROM Friend WHERE user_id = ? or friend_id=?""", [user.id,user.id])
		
		# Lista auxiliar para mantener el orden original
		lista_amigos_sin_duplicados = set()

		# Eliminar duplicados y mantener el orden original
		for amigo in lista_amigos:
			for aid in amigo:
				if aid != user.id:
					lista_amigos_sin_duplicados.add(aid)

		# Lista de amigos de amigos
		lista_amigos_de_amigos = set()

		lista_amigos_amigos_provisional = []
		for amigo_id in lista_amigos_sin_duplicados:
			amigos_de_amigo = db.select("""SELECT * FROM Friend WHERE user_id = ? OR friend_id = ?""", [amigo_id, amigo_id])
			lista_amigos_amigos_provisional = lista_amigos_amigos_provisional + amigos_de_amigo

		valores = [valor for tupla in lista_amigos_amigos_provisional for valor in tupla]

		for valor in valores:
			if( valor not in lista_amigos_sin_duplicados and valor!= user.id):
				lista_amigos_de_amigos.add(valor)

		# Elimina duplicados y amigos directos
		lista_recomendados = list(lista_amigos_de_amigos - lista_amigos_sin_duplicados)

		# Limita la lista según el parámetro "limite"
		lista_recomendados = lista_recomendados[:limite]

		#Cambiamos las id por el nombre usuario
		lista_nombres_recomendados = []
		for id in lista_recomendados:
			nombre = db.select("""SELECT user.name FROM User WHERE id = ?""", [id])
			lista_nombres_recomendados.append(nombre[0][0])			
		return lista_nombres_recomendados

	# === Recomendaciones del sistema ===
	def get_recommended_books(self, user=None):
		if user is None:
			"""Si no hay usuario del que obtener recomendaciones, se obtienen libros aleatorios"""
			res = db.select("""
				SELECT b.* 
				FROM Book b, Author a 
				WHERE b.author=a.id 
				ORDER BY RANDOM() LIMIT 3
			""")
			books = [
				Book(b[0],b[1],b[2],b[3],b[4])
				for b in res
			]
			return books
		else:
			"""En caso de que haya un usuario, se obtienen libros recomendados
			Para ello:
			  1. Se obtienen los temas de los libros que ha leido el usuario
			  2. Se obtienen los temas de los libros que ha leido los amigos del usuario
			  3. Se sacan todos los libros de los temas anteriores
			  4. Se eliminan los libros que ya ha leido el usuario
			"""
			# 1. Obtener los temas de los libros que ha leído el usuario
			user_themes = db.select("""
				SELECT DISTINCT theme_id
				FROM Borrow b, Copy c, BookTheme bt
				WHERE b.user_id = ? AND b.copy_id = c.id AND c.book_id = bt.book_id
			""", [user.id])

			# 2. Obtener los temas de los libros que han leído los amigos del usuario
			friend_themes = db.select("""
				SELECT DISTINCT theme_id
				FROM Friend f, Borrow b, Copy c, BookTheme bt
				WHERE f.user_id = ? AND f.friend_id = b.user_id AND b.copy_id = c.id AND c.book_id = bt.book_id
			""", [user.id])

			# Combinar las listas de temas
			themes = list(set().union(*user_themes, *friend_themes))

			# 3. Obtener los libros de los temas anteriores
			placeholders = ', '.join('?' for theme in themes)
			query = f"""
				SELECT b.*
				FROM Book b, BookTheme bt
				WHERE bt.book_id = b.id AND bt.theme_id IN ({placeholders})
			"""
			books = db.select(query, themes)

			# 4. Eliminar los libros que ya ha leído el usuario
			read_books = db.select("""
				SELECT c.book_id
				FROM Borrow b, Copy c
				WHERE b.user_id = ? AND b.copy_id = c.id
			""", [user.id])

			filtered_books = [book for book in books if book[0] not in {b[0] for b in read_books}]	# Tremenda linea de código

			# Devuelve 0-3 libros aleatorios
			random_books = random.sample(filtered_books, min(3, len(filtered_books)))
			sorted_books = sorted(random_books, key=lambda b: b[0])
			return [ Book(b[0],b[1],b[2],b[3],b[4]) for b in sorted_books ]
	# ===================================

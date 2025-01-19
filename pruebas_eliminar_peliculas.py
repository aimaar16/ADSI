import sqlite3

# Ruta de la base de datos
DB_PATH = "src/datos.db"

def verificarInterfazEliminar():
    # Esta función simula la existencia de una interfaz que incluye la opción "Eliminar Película"
    print("Interfaz de eliminación encontrada (simulado).")

def eliminarPeliculaExistente():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    # Insertar una película de prueba
    cursor.execute("INSERT INTO Book (title, author, cover, description) VALUES (?, ?, ?, ?)",
                   ("Matrix", 1, "matrix_cover.jpg", "A science fiction classic."))
    connection.commit()
    
    # Intentar eliminar la película
    cursor.execute("DELETE FROM Book WHERE title = ? AND author = ?", ("Matrix", 1))
    connection.commit()
    
    # Verificar que fue eliminada
    cursor.execute("SELECT * FROM Book WHERE title = ? AND author = ?", ("Matrix", 1))
    resultado = cursor.fetchone()
    
    if resultado is None:
        print("Película eliminada exitosamente.")
    else:
        print("Error: La película no se eliminó correctamente.")
    
    connection.close()

def eliminarPeliculaInexistente():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    # Intentar eliminar una película que no existe
    cursor.execute("DELETE FROM Book WHERE title = ? AND author = ?", ("Fantasma", 999))
    connection.commit()
    
    # Verificar si hubo algún error
    cursor.execute("SELECT * FROM Book WHERE title = ? AND author = ?", ("Fantasma", 999))
    resultado = cursor.fetchone()
    
    if resultado is None:
        print("Eliminación denegada: Película inexistente.")
    else:
        print("Error: Eliminación permitida de película inexistente.")
    
    connection.close()

def eliminarPeliculaSinTitulo():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    # Intentar eliminar una película sin título
    try:
        cursor.execute("DELETE FROM Book WHERE title = ?", ("",))
        connection.commit()
        print("Error: Eliminación permitida sin título.")
    except sqlite3.Error as e:
        print("Eliminación denegada: Falta título.")
    
    connection.close()

if __name__ == "__main__":
    verificarInterfazEliminar()
    eliminarPeliculaExistente()
    eliminarPeliculaInexistente()
    eliminarPeliculaSinTitulo()

import requests
from bs4 import BeautifulSoup


def test_register_user():
	url = "http://localhost:5000/register"
	data = {
		"nombre": "Test",
		"apellidos": "Usuario",
		"fecha_nac" : "0001-01-01",
		"email": "test@gmail.com",
		"password": "123456",
		"repetirContrasena" : "123456"
	}
	response = requests.post(url, data=data)
	print(response.url)
	
	
if __name__ == "__main__":
    test_register_user()

	

    


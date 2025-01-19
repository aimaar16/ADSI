import requests
from bs4 import BeautifulSoup
import re


def donacionVisible(url):
	response = requests.get(url)
	if re.search(r"\bDonar\b", response.text):  # \b asegura que sea una palabra completa
		print("Interfaz Encontrada")
	else:
		print ("Interfaz no visible")
		

def realizarDonacionBien(url):
	url = url + "/donacion"
	donation_data = {"donationAmount": "20"} 
	response = requests.post(url, data = donation_data)
	if response.url.find("Donacion%20compleatada%20con%20exito,%20GRACIAS!") != -1:
		print("Donacion Completada")
	else:
		print("Donacion Denegada")
		
def realizarDonacionMal(url):
	url = url + "/donacion"
	donation_data = {"donationAmount": "a"} 
	response = requests.post(url, data = donation_data)
	if response.url.find("Donación%20compleatada%20con%20exito,%20GRACIAS!") != -1:
		print("Donacion Completada")
	else:
		print("Donacion Denegada")
		
		
def realizarDonacionVacia(url):
	url = url + "/donacion"
	donation_data = {"donationAmount": ""} 
	response = requests.post(url, data = donation_data)
	if response.url.find("Donación%20compleatada%20con%20exito,%20GRACIAS!") != -1:
		print("Donacion Vacia Completada")
	else:
		print("Donacion Vacia Denegada")

url = "http://localhost:5000"
	
if __name__ == "__main__":
	donacionVisible(url)
	realizarDonacionBien(url)
	realizarDonacionMal(url)
	realizarDonacionVacia(url)
    

	

    


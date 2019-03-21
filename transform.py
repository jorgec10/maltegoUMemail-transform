from MaltegoTransform import *
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages/requests-2.21.0.dist-info')
sys.path.append('/usr/local/lib/python2.7/site-packages/beautifulsoup4-4.7.1.dist-info')
import requests
from bs4 import BeautifulSoup

# Get the email
email = sys.argv[1]
#print "Email: " + email

# Extract the username and the domain
s = email.split("@")
username = s[0]
domain = s[1]

#print("Username: " + username)
#print("Domain: " + domain)


# Create Maltego Transform object
malt = MaltegoTransform()

# Check if the domain is "um.es"
if domain != "um.es":
	# Launch maltego exception if not
	# TODO
	malt.addException("This transform only works with @um.es emails!")
	sys.exit("This transform only works with @um.es emails!")

# Make the search in the UM directory and store the webpage obtained as a result
r = requests.get('https://www.um.es/atica/directorio/?nivel=&lang=0&vista=unidades&search=' + username)

# print "URL: " + r.url

# Parse the html using beautiful soup
soup = BeautifulSoup(r.content, 'html.parser')

# Check if there are multiple entries

numEntries = soup.find('th', attrs={'class': 'numResult'})

if numEntries is not None:
	entries = numEntries.text.strip()
	entradasIndex = entries.find(' entradas ', 0, len(entries))
	number = entries[12:entradasIndex]
	print "numEntries: " + number

	# Find the URLs
	peoplebox = soup.findAll('td', attrs={'class': 'elemInfo2'})[1]

	s = BeautifulSoup(str(peoplebox), 'html.parser')
	for link in s.findAll('a'):
		print "https://www.um.es/atica/directorio/index.php" + link.get('href')
		
else:
	# Get the table of the data
	tablebox = soup.find('table', attrs={'class': 'infoElem'})
	table = tablebox.text.strip()


	# Find the index of the different data
	nombreIndex = table.find('Nombre:', 0 ,len(table))
	areaIndex = table.find('Area de Conocimiento:', 0, len(table))
	unidadIndex = table.find('Unidad Organizativa:', 0 ,len(table))
	telefonoIndex = table.find('fono:', 0, len(table))
	correoIndex = table.find('Correo', 0 ,len(table))
	direccionIndex = table.find('postal:', 0 ,len(table))
	centroIndex = table.find('Centro:', 0 ,len(table))
	puestoIndex = table.find('Puesto:', 0 ,len(table))
	despachoIndex = table.find('Despacho:', 0 ,len(table))
	filiacionIndex = table.find('Filiaci', 0 ,len(table))
	webIndex = table.find('institucional:', 0, len(table))

	# Exctract the data
	lastIndex = len(table)
	if webIndex != -1:
		web = table[webIndex+19:len(table)-26]
		web = "https" + web
		#print "Web personal: " + web
		lastIndex = webIndex-13
		malt.addEntity("maltego.Website", web.encode('utf-8').strip())
	if filiacionIndex != -1:
		correction = 3
		if webIndex == -1:
			correction = 25
		filiacion = table[filiacionIndex+11:lastIndex-correction]
		#print "Filiacion: " + filiacion
		lastIndex = filiacionIndex-1
		#malt.addEntity("maltego.Url", web)
	if despachoIndex != -1:
		despacho = table[despachoIndex+9:lastIndex-1]
		#print "Despacho: " + despacho
		lastIndex = despachoIndex
		malt.addEntity("maltego.Location", despacho.encode('utf-8').strip())
	if puestoIndex != -1:
		puesto = table[puestoIndex+7:lastIndex]
		#print "Puesto: " + puesto
		lastIndex = puestoIndex
		#malt.addEntity("maltego.Url", web)
	if centroIndex != -1:
		centro = table[centroIndex+7:lastIndex]
		#print "Centro: " + centro
		lastIndex = centroIndex
		malt.addEntity("maltego.Location", centro.encode('utf-8').strip())
	if direccionIndex != -1:
		direccion = table[direccionIndex+7:lastIndex]
		#print "Direccion: " + direccion
		lastIndex = direccionIndex
		malt.addEntity("maltego.Location", direccion.encode('utf-8').strip())
	if correoIndex != -1:
		#correo = table[correoIndex+19:lastIndex]
		#print "Correo: " + correo
		lastIndex = correoIndex
	if telefonoIndex != -1:
		telefono = table[telefonoIndex+5:lastIndex]
		#print "Telefono: " + telefono
		lastIndex = telefonoIndex-4
		malt.addEntity("maltego.PhoneNumber", telefono.encode('utf-8').strip())
	if unidadIndex != -1:
		unidad = table[unidadIndex+20:lastIndex]
		#print "Unidad: " + unidad
		lastIndex = unidadIndex
		malt.addEntity("maltego.Location", unidad.encode('utf-8').strip())
	if areaIndex != -1:
		area = table[areaIndex+21:lastIndex]
		#print "Area: " + area
		lastIndex = areaIndex
		#malt.addEntity("maltego.Location", centro)
	if nombreIndex != -1:
		nombre = table[nombreIndex+7:lastIndex]
		#print "Nombre: " + nombre
		lastIndex = nombreIndex
		malt.addEntity("maltego.Person", nombre.encode('utf-8').strip())


	# Return Maltego transform as an xml
	malt.returnOutput()



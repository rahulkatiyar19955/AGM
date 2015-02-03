import copy, sys, time
sys.path.append('/usr/local/share/agm/')
from AGGL import *
from agglplanner import *


#-----------------------------------------------------------------------#
#  CODIGO CUANDO EL OBJETIVO ES SERVIR AGUA DE UNA JARRA EN UNA MESA    #
#  A UN VASO EN LA MISMA MESA. TODOS SON SIMBOLOS CONSTANTES.           #
#-----------------------------------------------------------------------#

def computeMaxScore(a, b, maxScore):
	s = 0
	for i in a: s+=i
	for i in b: s+=i
	if s > maxScore: return s
	return maxScore

def CheckTarget(graph):
	starting_point = time.time()
	n2id = dict()
	available = copy.deepcopy(graph.nodes) # Guarda nombres y tipos de los nodos del grafo

	totalScore = 900
	maxScore = 0

	# Hard score
	scoreNodes = []
	scoreLinks = []
	# Sacamos los nodos que son constantes.
	del available['11']
	del available['13']
	del available['12']
	del available['14']
	
	# Sacamos TODOS los nodos constantes y los guardamos en variables. Estos
	# nodos NO necesitan hacer uso del diccionario.
	symbol_11 = graph.nodes['11']
	symbol_12 = graph.nodes['12']
	symbol_13 = graph.nodes['13']
	symbol_14 = graph.nodes['14']
	
	# Calculamos la puntuacion de los NODOS:
	if symbol_11.sType == 'Agua': scoreNodes.append(100)
	if symbol_12.sType == 'Jarra' and symbol_12.name != symbol_11.name: scoreNodes.append(100)
	if symbol_13.sType == 'Mesa'  and symbol_13.name != symbol_11.name and symbol_13.name != symbol_12.name: scoreNodes.append(100)
	if symbol_14.sType == 'Vaso'  and symbol_14.name != symbol_11.name and symbol_14.name != symbol_12.name and symbol_14.name != symbol_13.name: scoreNodes.append(100)
	
	# Ahora calculamos la puntuacion de los enlaces: [origen, destino, "nombre"] Un nodo cuyos enlaces terminan en el
	# (es decir, es un nodo destino) no computa enlaces. Siempre se calcula de origen a destino.
	# Comenzamos con el nodo 11. Debe estar conectado al nodo 14 mediante "en"
	if [symbol_11.name, symbol_14.name,"en"] in graph.links: scoreLinks.append(100)
	# Nodo 12, debe estar conectado a la mesa por dos links: "en" y "vacio"
	if [symbol_12.name, symbol_13.name,"en"] in graph.links: scoreLinks.append(100)
	if [symbol_12.name, symbol_13.name,"vacio"] in graph.links: scoreLinks.append(100)
	# El nodo 13 es la mesa y es un nodo puramente de destino. De el no sale ningun enlace.
	# Nodo 14, debe conectarse a la mesa mediante los enlaces "en" y "lleno"
	if [symbol_14.name, symbol_13.name,"en"] in graph.links: scoreLinks.append(100)
	if [symbol_14.name, symbol_13.name,"lleno"] in graph.links: scoreLinks.append(100)
	
	# Calculamos la heuristica
	maxScore = computeMaxScore(scoreNodes, scoreLinks, maxScore)
	
	if maxScore == totalScore:
		finalTime = time.time()-starting_point
		print 'Hemos llegado con: '+maxScore.__str__()+' con tiempo '+finalTime.__str__()
		return maxScore, True
	else:
		finalTime = time.time()-starting_point
		print 'No hemos llegado, '+maxScore.__str__()+' con tiempo '+finalTime.__str__()
		return maxScore, False

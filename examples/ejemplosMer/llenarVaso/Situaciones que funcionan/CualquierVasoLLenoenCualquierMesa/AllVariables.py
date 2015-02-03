import copy, sys, time
sys.path.append('/usr/local/share/agm/')
from AGGL import *
from agglplanner import *


#-------------------------------------------------------------------------#
# Quiero que haya cualquier vaso con cualquier agua en cualquier mesa. El #
# escenario inicial consta de una mesa 13 con una jarra 12 llena con agua #
# de inetificador 11 y un vaso 14 vacio. Ademas hay una mesa 15 con un    #
# vaso 16 vacio.							  #
# El objetivo es que el planner llene cualquier vaso en cualquier mesa    #
# Se busca solucion optima						  #
#-------------------------------------------------------------------------#

def computeMaxScore(a, b, maxScore):
	s = 0
	for i in a: s+=i
	for i in b: s+=i
	if s > maxScore: return s
	return maxScore

##@brief este metodo comprueba que el nombre de un simbolo, currentSymbol, no aparezca o
# este repetido dentro de una lista de simbolos visitados.
# @retval nameRepe es TRUE cuando el nombre se repite y FALSE cuando el nombre no se repite.
def checkList(currentSymbol, symbolsList):
	nameRepe = False
	if symbolsList.__len__() > 0:
		for symbol in symbolsList:
			if symbol.name == currentSymbol.name:
				nameRepe = True
				break
	return nameRepe

##@brief Metodo checkTarget. Comprueba si hemos alcanzado el estado objetivo o no. 
# @param graph es el grafo con el que esta trabajando el planificador. La primera vez que se
# llame al checkTarget coincidira con el estado del mundo inicial.
# @retval maxScore es la puntuación que se ha alcanzado al comprobar si s eha llegado al objetivo o no.
# @retval Bool indica si se ha llegado (TRUE) o no (FALSE) al objetivo.
def CheckTarget(graph):
	starting_point = time.time()
	n2id = dict()
	available = copy.deepcopy(graph.nodes) # Guarda nombres y tipos de los nodos del grafo
	
	totalScore = 600
	maxScore = 0

	# Hard score
	scoreNodes = []
	scoreLinks = []
	
	vectorAguas = []
	vectorVasos = []
	vectorMesas = []
	
	# No tenemos ningun simbolo constante. Nos ponemos a recorrer todo el grafo de
	# simbolos buscando los tres que nos importan: AGUA, VASO y MESA. Los guardamos
	# en vectores de tipos.
	for symbol_name in available:
		symbol = graph.nodes[symbol_name]
		# Comprobamos que no estamos metiendo dos veces el mismo simbolo en un determinado
		# vector mediante la funcion checkList. Aunque no deberia repetir nunca...
		if checkList(symbol, vectorAguas)==False and symbol.sType=='Agua': vectorAguas.append(symbol)
		else:
			if checkList(symbol, vectorVasos)==False and symbol.sType=='Vaso': vectorVasos.append(symbol)
			else:
				if checkList(symbol, vectorMesas)==False and symbol.sType=='Mesa': vectorMesas.append(symbol)
				
	# Tenemos que comporbar los enlaces: Necesitamos una mesa, con un vaso lleno de agua.
	for agua in vectorAguas:
		for vaso in vectorVasos:
			for mesa in vectorMesas:
				if [agua.name, vaso.name, "en"] in graph.links:
					if [vaso.name, mesa.name, "en"] in graph.links and [vaso.name, mesa.name, "lleno"] in graph.links:
						scoreNodes.append(300)
						scoreLinks.append(300)
				
		
	
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

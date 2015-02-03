import copy, sys, time
sys.path.append('/usr/local/share/agm/')
from AGGL import *
from agglplanner import *


#-----------------------------------------------------------------------#
# Quiero que haya cualquier vaso con cualquier agua en la mesa 15. El   #
# escenario inicial consta de una mesa 13 con una jarra 12 vacia y un   #
# vaso 14 lleno con agua 11. Ademas hay una mesa 15 con un vaso 16 vacio#
# El objetivo es que el planner mueva el vaso 14 a la mesa 15           #
#-----------------------------------------------------------------------#

def computeMaxScore(a, b, maxScore):
	s = 0
	for i in a: s+=i
	for i in b: s+=i
	if s > maxScore: return s
	return maxScore

##@brief este metodo comprueba que el nombre de un simbolo, currentSymbol, no aparezca o
# este repetido dentro de una lista de simbolos visitados.
# @retval nameRepe es TRUE cuando el nombre se repite y FALSE cuando el nombre no se repite.
#def checkList(currentSymbol, symbolsList):
	#nameRepe = False
	#if symbolsList.__len__() > 0:
		#for symbol in symbolsList:
			#if symbol.name == currentSymbol.name:
				#nameRepe = True
				#break
	#return nameRepe

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
	
		
	# Sacamos los nodos que son constantes y los guardamos en variables. Estos
	# nodos NO necesitan hacer uso del diccionario. En este caso es la mesa 15.
	del available['15']
	symbol_15 = graph.nodes['15']
	# Comprobamos su tipo y calculamos la heuristica del nodo.
	if symbol_15.sType == 'Mesa': scoreNodes.append(100)
	
	# Ahora debemos buscar un vaso con agua que este en la mesa 15. Hay que recorrer
	# el grafo de entrada buscando las coincidencias en los tipos y en los enlaces.
	# Problema: el objetivo es evitar for anidados.
	
	# Primer for: RECORRIDO GENERAL de los nodos NO costantes. Solo nos interesa encontrar
	# dos simbolos mas, el VASO y el AGUA.
	# CUIDADO: EL ORDEN DE COMPORBACION DE LOS LINKS AFECTA AL RESULTADO!!!!
	for symbol_name in available:
		symbol = graph.nodes[symbol_name]
		
		# --- VASO ---
		if symbol.name!=symbol_15.name and symbol.sType=='Vaso' and [symbol.name, symbol_15.name, "en"] in graph.links and [symbol.name, symbol_15.name, "lleno"] in graph.links: 
			scoreNodes.append(100)
			scoreLinks.append(200)
		
		# --- AGUA ---
		else:
			if symbol.name!=symbol_15.name and symbol.sType=='Agua':
				for symbol_name2 in available:
					symbol2 = graph.nodes[symbol_name2]
					
					# --- VASO ADECUADO Y AGUA ADECUADA ---
					if symbol2.name!=symbol.name and symbol2.name!=symbol_15.name and symbol2.sType=='Vaso' and [symbol2.name, symbol_15.name, "en"] in graph.links: 
							if [symbol.name, symbol2.name, "en"] in graph.links:
								scoreNodes.append(100)
								scoreLinks.append(100)
	
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

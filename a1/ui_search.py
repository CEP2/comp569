# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

Comp 569 - Artificial Intelligence
Assignment 1
Claveau 

Clifton Porter II
Fall 2016

Notes
-------------
Program currently does not run completely. 
Issue centers around 'get_other_label' in which the function
does not recognize 'other_vertex' as a vertex. On the contrary, in 
'get_edge_weight' trying to use 'other_vertex' as a 
"""

from collections import deque
import queue as Q
import sys

#-----------------------------------------------------------
class Vertex(object):
	def __init__(self,label, weight):
		self.label = label
		self.weight = weight
		self.edge_list = list()
		self.visited = False
		print('Created Vertex ' + self.label)

	def get_label(self):
		return self.label
	
	def get_other_label(self, other_vertex):
		other_vertex.get_label()

	def connect(self, other_vertex):
		self.edge_list.append(other_vertex)
		print('Added edge between Vertex ' + self.get_label() + ' and Vertex '+ other_vertex.get_label())
		
	def weighted_connect(self, other_vertex,weight):
		self.edge_list.append( (other_vertex, weight) )
		print('Added edge between Vertex ' + self.get_label() + ' and Vertex '+ other_vertex.get_label() + ' with weight of ' + str(weight) )
	
	def get_edge_weight(self, other_vertex):
		for edge in self.edge_list:
			print(other_vertex.get_label() + ' compared to ' + edge[0] )
			if other_vertex.get_label() == edge[0]:
				return edge[1]
		return None
		
	def get_edge_iterator(self):
		return iter(self.edge_list)

	def is_visited(self):
		return self.visited

	def set_visited(self):
		self.visited = True
		print ('Vertex ' + self.get_label() + ' is now visted.' )

	def get_weight(self):
		return self.weight

	def get_unvisited_neighbor(self):
		neighbors = self.get_edge_iterator()
		for neighbor in neighbors:
			if neighbor.is_visited():
				return neighbor
		return None

	def to_string(self):
		return self.label

#-----------------------------------------------------------
class Graph(object):
	def __init__(self, directed):
		self.adj_list = {}
		self.directed = directed
		self.dfs_solved = False

	def add_vertex(self, vertex_label,weight=1):
		self.adj_list[vertex_label] = Vertex(vertex_label,weight)

	def add_edge(self,v_one,v_two):
		if v_one in self.adj_list and v_two in self.adj_list:
			self.adj_list[v_one].connect(self.adj_list[v_two])
			if not self.directed:
				self.adj_list[v_two].connect(self.adj_list[v_one])
				
	def add_weighted_edge(self,v_one,v_two,weight):
		if v_one in self.adj_list and v_two in self.adj_list:
			self.adj_list[v_one].weighted_connect(self.adj_list[v_two], weight)
			if not self.directed:
				self.adj_list[v_two].weighted_connect(self.adj_list[v_one], weight)
				
	def reset_vertices(self):
		for vertex_label in self.adj_list:
			self.adj_list[vertex_label].visited = False
	#-----------------------------------------------------------
	def uniform_cost_search(self,start,goal):
		print('Running Uniform Cost Search between vertex ' + start + ' and Vertex ' + goal )
		level = dict()
		parent = dict()
		total_weight = dict()
		edge_weight = 0
		frontier = Q.PriorityQueue() 
		frontier.put( (0, start) )			#Use priority queue put. 
		parent[start] = None
		level[start] = 0
		total_weight[start] = 0
		
		solved = False
		while not frontier.empty() and not solved:
			vertex = frontier.get()[1]														#Get frontier
			self.adj_list[vertex].set_visited()										#Set Visited
			neighbors = self.adj_list[vertex].get_edge_iterator()				#Grab neighbors list.
			for neighbor in neighbors:
				if not solved:
					if not neighbor[0].is_visited():
						parent[neighbor[0].get_label()] = vertex 						#Set parent in dictionary.
						level[neighbor[0].get_label()] = level[vertex] + 1			#Set the level in dictionary.
						edge_weight = self.adj_list[vertex].get_edge_weight(neighbor[0].get_label())	#get the weight of the edge vertex->neighbor
						total_weight[neighbor.get_label()] = total_weight[vertex] + edge_weight
						if neighbor.get_label() == goal:								#Check if solved
							solved = True
						frontier.put( (total_weight[neighbor.get_label()], neighbor.get_label()  ) )				#Add to frontier queue if not solved.
						
		if solved:
			print('Solution Found:')
			while(neighbor):
				print(neighbor.to_string())
				if parent[neighbor.get_label()]:
					neighbor = self.adj_list[parent[neighbor.get_label()]];
				else:
					break
		else:
				print('No Solution Found!')
		self.reset_vertices()
		
		
		
	
	#-----------------------------------------------------------
	def breadth_first_search(self,start,goal):
		print('Running Breadth First Search between Vertex ' + start + ' and Vertex ' + goal )
		level = dict()
		parent = dict()
		frontier = deque()
		frontier.append(start)
		parent[start] = None
		level[start] = 0

		solved = False
		while len(frontier) and not solved:
			vertex = frontier.popleft()
			self.adj_list[vertex].set_visited()
			neighbors = self.adj_list[vertex].get_edge_iterator()
			for neighbor in neighbors:
				if not solved:
					if not neighbor.is_visited():
						parent[neighbor.get_label()] = vertex
						level[neighbor.get_label()] = level[vertex] + 1
						if neighbor.get_label() == goal:
							solved = True
						frontier.append(neighbor.get_label())
		if solved:
			print('Solution Found:')
			while(neighbor):
				print(neighbor.to_string())
				if parent[neighbor.get_label()]:
					neighbor = self.adj_list[parent[neighbor.get_label()]];
				else:
					break
		else:
				print('No Solution Found!')
		self.reset_vertices()  
    #-----------------------------------------------------------
	def depth_first_search(self,start,goal):
		print('Running Depth First Search between Vertex ' + start + ' and Vertex ' + goal )
		level = dict()
		parent = dict()
		frontier = deque()
		frontier.append(start)
		parent[start] = None
		level[start] = 0

		solved = False
		while len(frontier) and not solved:
			vertex = frontier.pop()
			self.adj_list[vertex].set_visited()
			neighbors = self.adj_list[vertex].get_edge_iterator()
			for neighbor in neighbors:
				if not solved:
					if not neighbor.is_visited():
						parent[neighbor.get_label()] = vertex
						level[neighbor.get_label()] = level[vertex] + 1
						if neighbor.get_label() == goal:
							solved = True
						frontier.append(neighbor.get_label())
		if solved:
			print('Solution Found:')
			while(neighbor.get_label != start):
				print(neighbor.to_string())
				if parent[neighbor.get_label()]:
					neighbor = self.adj_list[parent[neighbor.get_label()]];
				else:
					break
		else:
				print('No Solution Found!')
		self.reset_vertices()
    #-----------------------------------------------------------



if __name__ == '__main__':
	directed = True
	graph = Graph(directed)
	graph.add_vertex('S')
	graph.add_vertex('A')
	graph.add_vertex('B')
	graph.add_vertex('C')
	graph.add_vertex('D')
	graph.add_vertex('E')
	graph.add_vertex('F')
	graph.add_vertex('G')
	
	'''
	graph.add_edge('S', 'A')
	graph.add_edge('S', 'D')
	graph.add_edge('A', 'B')
	graph.add_edge('D', 'E')
	graph.add_edge('B', 'C')
	graph.add_edge('B', 'E')
	graph.add_edge('E', 'F')
	graph.add_edge('F', 'G')
	'''
	
	graph.add_weighted_edge('S', 'A', 1)
	graph.add_weighted_edge('S', 'D', 3)
	graph.add_weighted_edge('A', 'B', 2)
	graph.add_weighted_edge('D', 'E', 3)
	graph.add_weighted_edge('B', 'C', 4)
	graph.add_weighted_edge('B', 'E', 5)
	graph.add_weighted_edge('E', 'F', 2)
	graph.add_weighted_edge('F', 'G', 4)
 
	#graph.breadth_first_search('S','G')
	#graph.depth_first_search('S','G')
	graph.uniform_cost_search('S', 'G')
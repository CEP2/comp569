# -*- coding: utf-8 -*-

'''
UCS A* 
'''
import queue
from collections import deque
from GraphAI import Graph, Tree, Node
            
#-----------------------------------------------------------
def GraphSearch( graph, tree, search_type, start_label, goal_label ):
    print('-----------GraphSearch-----------', search_type)
    
    goal_node = Node('No Solution')
    
    if (search_type in {'UCS', 'GRD', 'AST'} ):
        frontier = queue.PriorityQueue()
        frontier.put(tree.GetRoot())
    else:
        frontier = deque()    
        frontier.append(tree.GetRoot())
    
    graph.GetVertex(start_label).SetVisited()
    
    solved = False
    while frontier and not solved:
        if (search_type == 'BFS'):
            pnode = frontier.popleft()
        elif (search_type == 'DFS'):
            pnode = frontier.pop()
        elif (search_type in {'UCS', 'GRD', 'AST'}):
            pnode = frontier.get()
            if pnode.GetLabel() == goal_label:    return pnode
                    
        neighbors = graph.GetVertex(pnode.GetLabel()).EdgeIterator()
        for neighbor in neighbors:
            if not solved:
                if (not neighbor[0].IsVisited() or search_type in {'UCS', 'GRD', 'AST'}):
                    neighbor[0].SetVisited()
                    
                    node = Node(neighbor[0].GetLabel())
                    node.parent = pnode
                    if (search_type == 'UCS'):
                        node.fcost = pnode.fcost + neighbor[1]
                    elif (search_type == 'GRD'):
                        node.fcost = neighbor[0].GetValue()
                    elif (search_type == 'AST'):
                        node.fcost = pnode.fcost + neighbor[0].GetValue()
                    tree.AddNode(node)
                    
                    if neighbor[0].GetLabel() == goal_label:
                        solved = True
                        goal_node = node
                    if (search_type in {'UCS', 'GRD', 'AST'}):
                        frontier.put(node)
                    else:
                        frontier.append(node)
    graph.ResetVertices()
    return goal_node
        
#-----------------------------------------------------------

if __name__ == '__main__':
    directed = True
    graph = Graph(directed)
    graph.AddVertex('S', 100)    # 'S' is the start vertex, 100 is the h()
    graph.AddVertex('A', 80)
    graph.AddVertex('B', 60)
    graph.AddVertex('C', 50)
    graph.AddVertex('D', 70)
    graph.AddVertex('E', 40)
    graph.AddVertex('F', 20)
    graph.AddVertex('G', 0)
    graph.AddEdge('S', 'D', 4)    # 4 is the edge weight, c()
    graph.AddEdge('S', 'A', 5)
    graph.AddEdge('A', 'B', 3)
    graph.AddEdge('A', 'D', 8)
    graph.AddEdge('D', 'E', 7)
    graph.AddEdge('B', 'C', 1)
    graph.AddEdge('B', 'E', 2)
    graph.AddEdge('E', 'F', 6)
    graph.AddEdge('F', 'G', 9)
 
    root = Node('S')
    root.parent = None
    search_tree = Tree(root)
    
    (GraphSearch( graph, search_tree, 'BFS', 'S', 'G' )).PrintParents()
    (GraphSearch( graph, search_tree, 'DFS', 'S', 'G' )).PrintParents()
    (GraphSearch( graph, search_tree, 'UCS', 'S', 'G' )).PrintParents()
    (GraphSearch( graph, search_tree, 'GRD', 'S', 'G' )).PrintParents()
    (GraphSearch( graph, search_tree, 'AST', 'S', 'G' )).PrintParents()
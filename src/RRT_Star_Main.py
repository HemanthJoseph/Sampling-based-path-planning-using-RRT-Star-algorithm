import random
import pygame
from pygame.locals import *
from Functions import *

width = 1000 #width of the map
height = 1000 #height of the map


class Node: #defining a Node called class to store the values
    def __init__(self, x_position, y_position):
         self.x = x_position
         self.y = y_position
    x = 0
    y = 0
    cost = 0  
    parent = None
    
	
def main():
    pygame.init() #initialize the pygame environment
    map = pygame.display.set_mode([width, height]) #creating a map to show the obstacles and the graph traversal
    white = 255, 255, 255
    map.fill(white) #filling the screen with white colour
    tree_color = 0, 0, 0
    draw_obstacle(pygame, map) #calling the obstacle function to draw on the map
    node_list = [] #create a list to save all the nodes
    
    #enter start node coordinates here
    start_coordinates = Node(100.0, 500.0) #keep in mind that the origin is at top left corner #set 1
    goal_coordinates = Node(800.0, 750.0) #creating both start and goal points as nodes
    # start_coordinates = Node(250.0, 700.0) #keep in mind that the origin is at top left corner #set 2
    # goal_coordinates = Node(900.0, 300.0) #creating both start and goal points as nodes
    start = start_coordinates
    goal = goal_coordinates
    node_list.append(start_coordinates) #appending start values to the list of nodes

    
    number_iterations = 1000 #number of iterations to run the code; change here if needed
    while True: #iterating through all node values
        rand_point = Node(random.random()*width, random.random()*height) #generate a random point in the map
        node_current = node_list[0]
        for iter_node in node_list: #iterate through the node list
            
            #check if the distance between the current node and random point is greater than distance between all nodes and random point
            #if yes, then the node in that iteration will be the current node, this way we choose the node closest to the random node to be the current node
            if dist([iter_node.x, iter_node.y], [rand_point.x, rand_point.y]) < dist([node_current.x, node_current.y], [rand_point.x, rand_point.y]):
                node_current = iter_node
        
        #selecting the new node at a distance of the threshold from the current node along the line
        #between current node and random point
        node_new = getNewNode([node_current.x, node_current.y], [rand_point.x, rand_point.y])
        newnode = Node(node_new[0], node_new[1])
        if checkForIntersection(node_current, rand_point): #check if the path between current node and random point intersects any obstacles
            #if not intersecting any obstacle, choose a parent node for the new node with the least cost from start node
            newnode, node_current = chooseBestParent(node_current, newnode, node_list)
            node_list.append(newnode) #add the new node the the list of all nodes
            
            #now we use the new node info and re wire the tree
            node_list = reWireTree(node_list, newnode, pygame, map)

            #draw a branch of the tree between the current node and the new node
            pygame.draw.line(map, tree_color, [node_current.x, node_current.y], [newnode.x, newnode.y])
            pygame.display.update() #update the map
        number_iterations -= 1 #decrementing of iteration so as to provide a change to break loop when all iterations are over
        if number_iterations == 0: #if all iterations are over, break the loop
            break
    #draw a path between the start and goal points along the nodes
    drawFinalPath(start, goal, node_list, pygame, map)
    pygame.display.update() #update the map

if __name__ == '__main__':
    main() #call main and run it
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

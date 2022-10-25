from math import sqrt
from math import cos
from math import sin
from math import atan2

max_dist_node_newnode = 5.0 #max distance at which a new node can be placed between current node and random point

#obstacle space
square_obstacle_1 = (125, 125, 150, 150)
square_obstacle_2 = (725, 125, 150, 150)
rectangle_obstacle = (350, 625, 300, 150)
obstacleSpace = [square_obstacle_1, square_obstacle_2, rectangle_obstacle]

radius_for_parent = 20 #radius from new node in which it will check for possible parents

def draw_obstacle(pygame, map): #draw the obstacles
    color = (153, 76, 0)
    for each_obstacle in obstacleSpace: 
        pygame.draw.rect(map, color, each_obstacle)

def dist(point_1, point_2): #find Euclidean distance between points
    euclidean_distance = sqrt((point_1[0] - point_2[0]) * (point_1[0] - point_2[0]) + (point_1[1] - point_2[1]) * (point_1[1] - point_2[1]))
    return euclidean_distance

def getNewNode(point_1, point_2): #Get new node
    if dist(point_1, point_2) < max_dist_node_newnode:
        return point_2
    else:
        theta = atan2(point_2[1] - point_1[1], point_2[0] - point_1[0])
        return point_1[0] + max_dist_node_newnode * cos(theta), point_1[1] + max_dist_node_newnode * sin(theta)

""" source for check intersection algorithm
https://bryceboe.com/2006/10/23/line-segment-intersection-algorithm/"""

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

# Return true if two line segments intersect each other
def checkForIntersection(nodeA, nodeB):
    A = (nodeA.x, nodeA.y)
    B = (nodeB.x, nodeB.y)
    for i in obstacleSpace: #check for all obstacles in obstacle space
        side_1 = i[0] #getting all the sides
        side_2 = i[1]
        side_3 = i[0] + i[2]
        side_4 = i[1] + i[3]
        obs = (side_1, side_2, side_3, side_4)
        C1 = (side_1, side_2) #side 1, side 2
        D1 = (side_1, side_4) #side 1, side 4
        C2 = (side_1, side_2) #side 1, side 2
        D2 = (side_3, side_2) #side 3, side 2
        C3 = (side_3, side_4) #side 3, side 4
        D3 = (side_3, side_2) #side 3, side 2
        C4 = (side_3, side_4) #side 3, side 4
        D4 = (side_1, side_4) #side 1, side 4
        #check for intersection of path for all four sides
        intersection_1= ccw(A,C1,D1) != ccw(B,C1,D1) and ccw(A,B,C1) != ccw(A,B,D1)
        intersection_2= ccw(A,C2,D2) != ccw(B,C2,D2) and ccw(A,B,C2) != ccw(A,B,D2)
        intersection_3= ccw(A,C3,D3) != ccw(B,C3,D3) and ccw(A,B,C3) != ccw(A,B,D3)
        intersection_4= ccw(A,C4,D4) != ccw(B,C4,D4) and ccw(A,B,C4) != ccw(A,B,D4)
        if intersection_1 == False and intersection_2 == False and intersection_3 == False and intersection_4 == False:
            continue #if none of the sides intersect continue
        else:
            return False
    return True

def chooseBestParent(current_node, newnode, node_list): #Choose best parent node
    for node in node_list:
        if checkForIntersection(node, newnode) and dist([node.x, node.y], [newnode.x,newnode.y]) < radius_for_parent and node.cost + dist([node.x, node.y], [newnode.x, newnode.y]) < current_node.cost + dist([current_node.x, current_node.y],[newnode.x, newnode.y]):
            current_node = node
    newnode.cost = current_node.cost + dist([current_node.x, current_node.y],[newnode.x, newnode.y])
    newnode.parent = current_node
    return newnode, current_node

def reWireTree(node_list, newnode, pygame, map): #rewiring the tree
    red = 255, 0, 0
    black = 0, 0, 0
    for i in range(len(node_list)):
        node = node_list[i]
        if checkForIntersection(node, newnode) and node != newnode.parent and dist([node.x, node.y], [newnode.x, newnode.y]) < radius_for_parent and newnode.cost + dist([node.x, node.y], [newnode.x, newnode.y]) < node.cost:
            pygame.draw.line(map, red, [node.x, node.y], [node.parent.x, node.parent.y]) #old path shown in red
            node.parent = newnode #updating the parent of that node
            node.cost = newnode.cost + dist([node.x, node.y], [newnode.x, newnode.y]) #updating the cost of that node
            node_list[i] = node #rewiring part, changing node that instance in node list with the updated node  
            pygame.draw.line(map, black, [node.x, node.y], [newnode.x, newnode.y]) #rewired path shown in black                 
    return node_list

def drawFinalPath(start, goal, node_list, pygame, map): #draw the solution path on the graph
  path_color = 178, 34, 34
  current_node = node_list[0]
  for node in node_list:
    if dist([node.x, node.y],[goal.x, goal.y]) < dist([current_node.x, current_node.y],[goal.x, goal.y]):
        current_node = node
  while current_node != start:
        pygame.draw.line(map, path_color, [current_node.x, current_node.y], [current_node.parent.x, current_node.parent.y], 4) #solution path in crimson red
        current_node = current_node.parent #updating the current node

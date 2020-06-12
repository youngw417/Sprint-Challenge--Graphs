from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)
"""
get a initial direction
"""
travel_entries = {}

def bfs(graph, starting, ending):
    q = Queue()
    q.enqueue([(starting, None)])
    visited = set()
    while q.size() > 0:
        path = q.dequeue()
        current = path[-1][0]
        while current not in visited:
            visited.add(current)
            
            if current == ending:
                return path
            else:

                neighbors = graph[current]
                for key in neighbors:
                    if neighbors[key] is not '?':
                        new_path = path + [(neighbors[key], key)]
                        q.enqueue(new_path)

# function to find the nearest node which has unvisited direction with '?'
def find_node(graph, starting):
    container = []
    nearest = []  # a list to hold all room_id with unvisited directions
    # like [ 2, 5, 7]
    target_node = False
    # container: a list hold all path information to the rooms
    # with unvisited directions
    # sample data, container = [[('s', 3), ('w', 5), ('e', 4)], 
    # [('e', 14), ('w', 21), ('s', 3), ('w', 1)]]
    for key in graph:
        for key2 in graph[key]:
           
            if graph[key][key2] == '?':
                target_node = True
        if target_node:
            nearest.append(key)
        target_node = False

    if not nearest:
        return None
  
    for each in nearest:
        container += [bfs(graph, starting, each)]
    print('container', container)
    # to dicide which path in container has the shortest room with unvisited direction
    min = len(container[0])
    min_index = 0
    for i in range(len(container)):
        if min > len(container[i]):
            min = len(container[i])
            min_index = i
    # returning a shortest path to room wiht unvisited direction
    # [('s', 3), ('w', 5), ('e', 4)]
    return container[min_index]

    
        


# graph = {0: {'n': 1, 's': '?', 'w': '?', 'e': '?'}, 1: {'n': 2, 's': 0, 'w': 15, 'e': 12}, 2: {'s': 1}, 15: {'w': 16, 'e': 1}, 16: {'n': 17, 'e': 15}, 17: {'s': 16}, 12: {'w': 1, 'e': 13}, 13: {'n': 14, 'w': 12}, 14: {'s': 13}}

# starting =  14
# ending= 0

# print(find_node(graph, starting))

# regitering travel_entries for all available exit direction
def get_entries(room, exits):
    travel_entries[room.id] = {}
    for each in exits:
        travel_entries[room.id][each] = '?'

# updating travel_entries for all dicided direction to exit
def update_entries(previous, current, direction):
    travel_entries[previous.id][direction] = current.id
    if direction == 's':
        travel_entries[current.id]['n'] = previous.id
    elif direction == 'n':
        travel_entries[current.id]['s'] = previous.id
    elif direction == 'e':
        travel_entries[current.id]['w'] = previous.id
    else:
        travel_entries[current.id]['e'] = previous.id

# regiester initial entries for starting_room
exits = world.starting_room.get_exits()
get_entries(world.starting_room, exits)


# to decide direction based on not visited direction with '?'
def get_direction(room):
    for key in travel_entries[room.id]:
        if travel_entries[room.id][key] == '?':
         
            return key
    return None

# def back_direction(dir):
#     if dir == 'n':
#         return 's'
#     elif dir == 's':
#         return 'n'
#     elif dir == 'e':
#         return 'w'
#     else: 
#         return 'e'
   

    
traversal_path = []

# for setting starting_room as a current to explore
current_room = world.starting_room
# for availalbe exit direction, get a direction to explore
direction = get_direction(current_room)


while direction:
    player.travel(direction)  # proceed to the direction
    traversal_path.append(direction)  # add the direction to the list
    previous_room = current_room # now the new room entered and re-set the room
    current_room = player.current_room
    
    exits = current_room.get_exits() # get available exit directions in the current room
    if current_room.id not in travel_entries:

        get_entries(current_room, exits)   # register and update the travel_entries for previous and current room 
    update_entries(previous_room, current_room, direction)  # based on the direction chosen

    # get a direction for other room to continue exeploration
    # if no direction (dead-end room), use bfs to find the nearest room availble 
    # with unvisited direction to other rooms
    direction = get_direction(current_room) 
    # print('cuurent room direction', current_room.id, direction, traversal_path)
    back_path = []
    if not direction:
        path_to_node = find_node(travel_entries, current_room.id)  #find the nearest room with unvisited direction via bfs
        if path_to_node:
            # path_to_node: [('s', 3), ('w', 5), ('e', 4)]
            for each in path_to_node:
                if each[1]:
                    back_path.append(each[1])
                    player.travel(each[1])
            traversal_path += back_path
            current_room = player.current_room
            direction = get_direction(current_room)
        else:
            break
print('traversal_path', traversal_path)
print(travel_entries)
   
"""
get a random direction
go direction
"""



# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")

#['n', 'n', 's', 'w', 'w', 'n', 's', 'e', 'e', 'e', 'e', 'n', 's', 'w', 'w', 'w', 'w', 'n', 's', 'e', 'e', 'n', 's', 's', 's', 's', 'w', 'w', 'n', 'n', 'e', 'e', 'e', 'e']#

#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")

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

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
# dft

def traverse_rooms(room):
    s = Stack()
    s.push(room)
    visited = []
    while s.size() > 0:
        room = s.pop()
        if room not in visited:
            visited.append(room)
            room_exits = room_graph[room][1]
            for direction in room_exits:
                if room_exits[direction] not in visited:
                    s.push(room_exits[direction])
    return visited
# dft Recursion with its own stack
def recurse_rooms(room, visited=None):
    if visited is None:
        visited = []
    if room not in visited:
        visited.append(room)
        room_exits = room_graph[room][1]
        for direction in room_exits:
            if room_exits[direction] not in visited:
                recurse_rooms(room_exits[direction], visited)
    return visited
#2011 Moves dfs
def dfs_route(starting_room, destination_room):
    s = Stack()
    s.push([starting_room])
    visited = set()
    while s.size() > 0:
        room = s.pop()
        last_room = room[-1]
        if last_room not in visited:
            if last_room == destination_room:
                return room
            room_exits = room_graph[last_room][1]
            visited.add(last_room)
            for direction in room_exits:
                new_path = room[:]
                new_path.append(room_exits[direction])
                s.push(new_path)


# BFT for traversal
def bft(room):
    q = Queue()
    q.enqueue(room)
    visited = []
    while q.size() > 0:
        room = q.dequeue()
        if room not in visited:
            visited.append(room)
            room_exits = room_graph[room][1]
            for direction in room_exits:
                if room_exits[direction] not in visited:
                    q.enqueue(room_exits[direction])
    return visited
#987 Moves bfs
def shortest_route(starting_room, destination_room):
    q = Queue()
    q.enqueue([starting_room])
    visited = []
    while q.size() > 0:
        current_path = q.dequeue()
        current_room = current_path[-1]
        if current_room not in visited:
            visited.append(current_room)
            if current_room == destination_room:
                return current_path
            room_exits = room_graph[current_room][1]
            for direction in room_exits:
                new_path = current_path[:]
                new_path.append(room_exits[direction])
                q.enqueue(new_path)
def player_traversal(player):
    path = traverse_rooms(player.current_room.id)
    for i in range(len(path) - 1):
        path_to_next = shortest_route(path[i], path[i+1])
        for y in range(len(path_to_next) - 1):
            path_exits = room_graph[path_to_next[y]][1]
            for direction in path_exits:
                if path_exits[direction] == path_to_next[y + 1]:
                    player.travel(direction)
                    traversal_path.append(direction)
player_traversal(player)
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



######
# UNCOMMENT TO WALK AROUND
######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")

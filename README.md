# Artificial-Intelliegence

The aim of the project is to implement algorithms that find good driving directions between pairs of cities in the US given by the user. The program runs on the command line like this:__
./route.py [start-city] [end-city] [routing-algorithm] [cost-function] __
where: __
• start-city and end-city are the cities we need a route between.
• routing-algorithm is one of:
-- __bfs__ uses breadth-first search (which ignores edge weights in the state graph)
-- __uniform__ is uniform cost search (the variant of bfs that takes edge weights into consideration)
-- __dfs__ uses depth-first search
-- __astar__ uses A* search, with a suitable heuristic function
• cost-function is one of:
– __segments__ tries to find a route with the fewest number of “turns” (i.e. edges of the graph)
– __distance__ tries to find a route with the shortest total distance
– __time__ tries to find the fastest route, for a car that always travels at the speed limit


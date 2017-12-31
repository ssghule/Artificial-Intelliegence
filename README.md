# Artificial-Intelliegence

The aim of the project is to implement algorithms that find good driving directions between pairs of cities in the US given by the user. The program runs on the command line like this: <br />
./route.py [start-city] [end-city] [routing-algorithm] [cost-function] <br />
where: <br />
• start-city and end-city are the cities we need a route between.<br />
• routing-algorithm is one of:<br />
-- __bfs__ uses breadth-first search (which ignores edge weights in the state graph)<br />
-- __uniform__ is uniform cost search (the variant of bfs that takes edge weights into consideration)<br />
-- __dfs__ uses depth-first search<br />
-- __astar__ uses A* search, with a suitable heuristic function<br />
• cost-function is one of:<br />
– __segments__ tries to find a route with the fewest number of “turns” (i.e. edges of the graph)<br />
– __distance__ tries to find a route with the shortest total distance<br />
– __time__ tries to find the fastest route, for a car that always travels at the speed limit<br />


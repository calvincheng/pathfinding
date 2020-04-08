class Djikstra:
    def __init__(self, board):
        self.board = board

    def search(self, start, goal, screen):
        '''Performs search using Djikstra's algorithm
        start: (x, y) tuple
        goal: (x, y) tuple
        '''
        from objects.LinearADT import PriorityQueue
        import curses

        dists = {(i, j): 9999 for i in range(len(self.board[0])) 
                              for j in range(len(self.board))}
        prevs = {(i, j) : None for i in range(len(self.board[0]))
                               for j in range(len(self.board))}
        startX, startY = start
        dists[start] = 0

        pq = PriorityQueue([], [])
        for i in range(len(self.board[0])):
            for j in range(len(self.board)):
                if self.board[j][i] == 1:
                    continue
                node = (i, j)
                pq.enqueue(node, dists[node])

        while not pq.isEmpty():
            cur = pq.dequeue()
            cur_x, cur_y = cur
            self.board[cur_y][cur_x] = 3 # Mark as "seen"
            if cur == goal:
                break
            nbrs = self.board.getNeighbours(cur)
            for nbr in nbrs:
                if self.board[nbr[1]][nbr[0]] != 3:
                    self.board[nbr[1]][nbr[0]] = 4

                dir2cur = self.getDirection(prevs[cur], cur)
                dir2nbr = self.getDirection(cur, nbr)
                dirCost = abs(dir2nbr - dir2cur) % 2

                dist2nbr = dists[cur] + self.getDist(cur, nbr) + dirCost
                if dists[nbr] > dist2nbr:
                    dists[nbr] = dist2nbr
                    prevs[nbr] = cur
                    pq.setPriority(nbr, dist2nbr)
            self.board.draw(screen)

        # Recreate path
        path = [goal]
        i, j = goal
        while prevs[(i, j)]:
            prev = prevs[(i, j)]
            path.append(prev)
            i, j = prev

        return reversed(path)

    def getDist(self, node1, node2):
        '''Finds manhattan distance between node1 and node2
        node1: (x, y) tuple
        node2: (x, y) tuple
        '''
        return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])
    
    def getDirection(self, node1, node2):
        '''Finds the bearing from node1 to node 2
        OUTPUT: 0: North, 1: East, 2: South, 3: West
        '''
        if node1 is None or node2 is None:
            return 0
        dirs = {(0, 1): 0, (1, 0): 1, (0, -1): 2, (-1, 0): 3} # N E S W
        dx = node1[0] - node2[0]
        dy = node1[1] - node2[1]
        return dirs[(dx, dy)]


class AStar:
    def __init__(self, board):
        self.board = board

    def search(self, start, goal):
        '''Performs search using AStar algorithm
        start: (x, y) tuple
        goal: (x, y) tuple
        '''

        dists = [[9999] * len(self.board[0]) for _ in range(len(self.board))]
        prevs = [[None] * len(self.board[0]) for _ in range(len(self.board))]
        startX, startY = start
        dists[startY][startX] = 0 + self.getScore(start, goal)

        from objects.LinearADT import PriorityQueue
        pq = PriorityQueue([], [])
        for i in range(len(self.board[0])):
            for j in range(len(self.board)):
                if self.board[j][i] == 1:
                    continue
                node = (i, j)
                dist = dists[j][i]
                pq.enqueue(node, dist)

        while not pq.isEmpty():
            cur = pq.dequeue()
            cur_x, cur_y = cur
            nbrs = self.board.getNeighbours(cur)
            for nbr in nbrs:
                nbr_x, nbr_y = nbr
                dist2nbr = (dists[cur_y][cur_x] 
                            + self.getDist(cur, nbr) # Cost
                            + self.getScore(nbr, goal)) # Heuristic
                if dists[nbr_y][nbr_x] > dist2nbr:
                    dists[nbr_y][nbr_x] = dist2nbr
                    prevs[nbr_y][nbr_x] = cur
                    pq.setPriority(nbr, dist2nbr)

        # Recreate path
        path = [goal]
        i, j = goal
        while prevs[j][i]:
            prev = prevs[j][i]
            path.append(prev)
            i, j = prev

        return path[::-1]

    def getDist(self, node1, node2):
        '''Finds manhattan distance between node1 and node2
        node1: (x, y) tuple
        node2: (x, y) tuple
        '''
        return abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])

    def getScore(self, node1, node2):
        '''Finds euclidean distance between node1 and node2
        node1: (x, y) tuple
        node2: (x, y) tuple
        '''
        import math
        dx = abs(node1[0] - node2[0])
        dy = abs(node1[1] - node2[1])
        dist = int(math.sqrt(dx**2 + dy**2))
        return dist


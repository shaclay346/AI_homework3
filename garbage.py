from queue import PriorityQueue
solved = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5,
          5, 5, 5, 5, 5]

unsolved = [2, 3, 3, 0, 0, 0, 0, 0, 0, 5, 2, 2, 5, 1, 1, 5, 1, 1, 3, 3, 3, 4, 2, 2, 4, 2, 2, 4, 4, 5, 3, 3, 5, 3, 3, 0, 4, 4, 1, 4, 4, 1, 2, 2, 1, 0, 5, 5, 0,
            5, 5, 4, 1, 1]


pq = PriorityQueue()
pq.put((0, solved))
pq.put((4.5, unsolved))
pq.put((3.2, [0, 2, 4, 5]))
pq.put((1, unsolved))

costToState = {}
x = [0, 4, 7, 9]
# print("U" in costToState.keys())
costToState[tuple(x)] = "12"
print(costToState[tuple(x)])

# actions = "UDLRFB"
# for i in actions:
#     print(i)

# print(pq.get(4.5))
# print(pq.get(4.5))
# print(pq.get(4.5))
# print(pq.get(4.5))
# print(pq.)
side = []
counter = 0
numDifferent = 0
for i in range(len(solved)):
    side.append(solved[i])
    counter += 1
    if(counter % 9 == 0):
        middle = side[4]
        for j in range(len(side)):
            if(side[j] != middle):
                numDifferent += 1
        side = []
        # add the num different to something to store it before we caclculate the avg
avg = numDifferent / 6
print(avg)

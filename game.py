import environment
import agent
import MakeSpaceTower as tower
from itertools import groupby
from matplotlib import pyplot



def containmentTest(spaces, xCoords, yCoords,sVal):
	obst = []
	for i in range(len(xCoords)):
		for space in spaces:
			points = space.points_ceiling
			xs = [p.x for p in points]
			ys = [p.y for p in points]

			if xCoords[i] >= min(xs) and xCoords[i] <= max(xs) and yCoords[i] >= min(ys) and yCoords[i] <= max(ys):
				obst.append((xCoords[i]/sVal,yCoords[i]/sVal))
	return obst
sVal = 4000
allSpaces = tower.makeSpaceTower()
levels = []

for key, g  in groupby(allSpaces, key = lambda x: x.level):
	levels.append(list(g))
print(len(levels))
spaces = levels[8]


for space in spaces:
	print(space.name)


floorX = 30000
floorY = 70000


u = int(floorX/sVal)
v = int(floorY/sVal)



shafts = [s for s in allSpaces if s.name == 'Shaft']
print("Shafts found: ",len(shafts))
shaft = shafts[0]

obstacles = [s for s in spaces if s.name == 'Conference']

xCoords = [i*sVal for i in range(int(u))]
yCoords = [i*sVal for i in range(int(v))]

obst = containmentTest(spaces,xCoords,yCoords,sVal)
print ('Obstacle Count',len(obst))

space = spaces[5]
start = shaft.centroid_ceiling
center = space.centroid_ceiling

# ------------------------------------environment-------------------------------------
gridH, gridW = u,v
start_pos = (4,10)#(int(int(round(start.x/sVal)*sVal)/sVal),int(int(round(start.y/sVal)*sVal)/sVal) )
print(start_pos)
end_positions = [(int(int(round(center.x/sVal)*sVal)/sVal),17)]#int(int(round(center.y/sVal)*sVal)/sVal))] #[(endX[i],endY[i]) for i in range(len(endX))]
print(end_positions)
end_rewards = [100]
blocked_positions = obst #[(obstX[i],obstY[i]) for i in range(len(obstX))]
default_reward = 0.0

env = environment.Environment(gridH, gridW, end_positions, end_rewards, blocked_positions, start_pos, default_reward)

# ---------------------------------------agent---------------------------------------------
alpha = 0.2
epsilon = 0.5
discount = 0.99
action_space = env.action_space
state_space = env.state_space

a = agent.QLearningAgent(alpha, epsilon, discount, action_space, state_space)
a.train(env,100000)

output = a.qvalues

output = a.get_path(env)
#pyplot.plot(output)
pyplot.show()
print(output)

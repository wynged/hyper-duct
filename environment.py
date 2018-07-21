import numpy as np
#import cv2
import sys

class Environment(object):
	
	def __init__(self, gridH, gridW, end_positions, end_rewards, blocked_positions, start_position, default_reward, scale=100):
		
		self.action_space = 4
		self.state_space = gridH * gridW	
		self.gridH = gridH
		self.gridW = gridW
		self.scale = scale 

		self.end_positions = end_positions
		self.end_rewards = end_rewards
		self.blocked_positions = blocked_positions
		
		self.start_position = start_position
		if self.start_position == None:
			self.position = self.init_start_state()
		else:
			self.position = self.start_position
						
		self.state2idx = {}
		self.idx2state = {}
		self.idx2reward = {}
		for i in range(self.gridH):
			for j in range(self.gridW):
				idx = i*self.gridW + j
				self.state2idx[(i, j)] = idx
				self.idx2state[idx]=(i, j)
				self.idx2reward[idx] = default_reward
				
		for position, reward in zip(self.end_positions, self.end_rewards):
			self.idx2reward[self.state2idx[position]] = reward

		self.frame = np.zeros((self.gridH * self.scale, self.gridW * self.scale, 3), np.uint8)	


	def init_start_state(self):
		
		while True:
			
			preposition = (np.random.choice(self.gridH), np.random.choice(self.gridW))
			
			if preposition not in self.end_positions and preposition not in self.blocked_positions:
				
				return preposition

	def get_state(self):
		
		return self.state2idx[self.position]
	
	def get_possible_actions(self):
		
		'''
		pos = self.position
		possible_actions = []
		
		if pos[0]+1<self.nH: and (pos[0]+1,pos[1]) not in self.blocked_positions:
			possible_actions.append(0)
				
		if pos[0]-1>=0 and (pos[0]-1,pos[1]) not in self.blocked_positions:
			possible_actions.append(1)
		
		if pos[1]+1<self.nW and (pos[0],pos[1]+1) not in self.blocked_positions:
			possible_actions.append(2)
				
		if pos[1]-1>=0 and (pos[0],pos[1]-1) not in self.blocked_positions:
			possible_actions.append(3)
		
		return possible_actions		
		'''
		
		return range(self.action_space) 
	
	def step(self, action):
		
		if action >= self.action_space:
			return

		if action == 0:
			proposed = (self.position[0] +1, self.position[1])
			
		elif action == 1:
			proposed = (self.position[0] -1, self.position[1])
			
		elif action == 2:
			proposed = (self.position[0], self.position[1] +1)
			
		elif action == 3:
			proposed = (self.position[0], self.position[1] -1)	
		
		y_within = proposed[0] >= 0 and proposed[0] < self.gridH
		x_within = proposed[1] >= 0 and proposed[1] < self.gridW
		free = proposed not in self.blocked_positions		
		
		if x_within and y_within and free:
			
			self.position = proposed
			
		next_state = self.state2idx[self.position] 
		reward = self.idx2reward[next_state]
		
		if self.position in self.end_positions:
			done = True
		else:
			done = False
			
		return next_state, reward, done
		
	def reset_state(self):
		
		if self.start_position == None:
			self.position = self.init_start_state()
		else:
			self.position = self.start_position


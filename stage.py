import cocos
import pyglet
import sys
from cocos.director import director

class Block:
	def __init__(self, type):
		self.type = type
		namemap = {}
		namemap['0'] = 'blank.png'
		namemap['1'] = 'dirt.png'
		namemap['S'] = 'human.png'
		namemap['L'] = 'left.png'
		namemap['J'] = 'jump.png'
		namemap['D'] = 'door.png'
		self.sprite = cocos.sprite.Sprite(namemap[type])

class Stage(cocos.layer.Layer):

	is_event_handler = True

	def __init__(self, map):
		super(Stage,self).__init__()
		self.cmap = map
		self.map = []
		for i in range(16):
			for j in range(12):
				x = Block(map[j][i])
				x.sprite.position = i*64+x.sprite.width/2, 768-(j*64+x.sprite.height/2)
				self.map.append(x)
		scene = cocos.scene.Scene()
		self.schedule(self.update)
		self.windowx, self.windowy = 1024,768
		self.blocksize = 64
		self.width, self.height = self.windowx // self.blocksize, self.windowy // self.blocksize
		self.stx = 0
		self.sty = 0
		self.isjump = False
		self.leftmove = False
		self.jumpmove = False
		self.isJump = False
		for j in self.map:
			if j.type =='S':
				self.player = j
				nb = cocos.sprite.Sprite('blank.png')
				nb.x, nb.y =j.sprite.x, j.sprite.y
				self.add(nb, z=1)
				self.add(j.sprite, z=2)
			else:
				self.add(j.sprite, z=1)
		
		
	def LRcalcColli(self, pxcor, xcor, ycor ):
		for i in self.map:
			if abs(i.sprite.y- ycor) < 63-1e-6 and i.type =='1':
				if abs(i.sprite.x - pxcor) > 63+1e-6 and abs(i.sprite.x-xcor) < 63-1e-6:
					return (True, i)
		return (False, None)
	
	def UDcalcColli(self, xcor, pycor, ycor ):
		for i in self.map:
			if abs(i.sprite.x- xcor) < 63-1e-6 and i.type =='1':
				if abs(i.sprite.y - pycor) > 63+1e-6 and abs(i.sprite.y-ycor) < 63-1e-6:
					return (True, i)
		return (False, None)
	
	def isOverPlaced(self, xcor, ycor):
		for i in self.map:
			if abs(i.sprite.x- xcor) < 63-1e-6 and i.type =='1':
				if abs(i.sprite.y-ycor) < 63+1e-4:
					return False
					
		return True
	
	def update(self, dt):
		stx, sty = self.stx, self.sty
		if not self.isJump: self.sty = 0
		else: self.sty -= 3*dt
		stx *= dt*100
		sty *= dt*100
		#self.player.sprite.x += stx
		#self.player.sprite.y += sty
		
		
		res, colli = self.LRcalcColli(self.player.sprite.x, self.player.sprite.x + stx, self.player.sprite.y)
		
		if not res: self.player.sprite.x += stx
		else:
			if colli.sprite.x<self.player.sprite.x: self.player.sprite.x = colli.sprite.x + 63 + 1e-5
			else: self.player.sprite.x = colli.sprite.x - 63 - 1e-5
		
		res, colli = self.UDcalcColli(self.player.sprite.x, self.player.sprite.y, self.player.sprite.y + sty)
		
		if not res: self.player.sprite.y += sty
		else:
			if colli.sprite.y < self.player.sprite.y:
				self.player.sprite.y = colli.sprite.y + 63 + 1e-5
				self.isJump = False
				self.sty = 0
			else:
				self.player.sprite.y = colli.sprite.y - 63 - 1e-5
				self.sty = 0
		
		res = self.isOverPlaced(self.player.sprite.x, self.player.sprite.y)
		if res: self.isJump = True
		
		for j in self.map:
			if abs(j.sprite.x-self.player.sprite.x) < 32 and abs(j.sprite.y-self.player.sprite.y) < 32:	
				if j.type == 'L':
					j.sprite.image = pyglet.image.load('blank.png')
					j.type = '0'
					self.leftmove = True
					
				if j.type == 'J':
					j.sprite.image = pyglet.image.load('blank.png')
					j.type = '0'
					self.jumpmove = True
				if j.type == 'D':
					exit()
							
	def restart(self):
		scene = cocos.scene.Scene()
		StageFrame = Stage(self.cmap)
		scene.add(StageFrame)
		director.replace(scene)
		
	def on_key_press(self, key, modifiers):
		if self.leftmove and key==97: self.stx = -1
		if key==100: self.stx = 1
		if key==119 and self.jumpmove and not self.isJump:
			self.sty = 3
			self.isJump = True
		if key==114:
			self.restart()
			
		
	def on_key_release(self, key, modifiers):
		if key==97 and self.stx==-1: self.stx =0 
		if key==100 and self.stx==1: self.stx = 0
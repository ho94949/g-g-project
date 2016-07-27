import cocos

class Stage(cocos.layer.Layer):

	is_event_handler = True

	def __init__(self, map):
		super(Stage,self).__init__()
		self.map = map
		scene = cocos.scene.Scene()
		self.schedule(self.update)
		self.windowx, self.windowy = 1024,768
		self.blocksize = 64
		self.width, self.height = self.windowx // self.blocksize, self.windowy // self.blocksize
		
		for i in self.map:
			for j in i:
				if j.type =='S':
					self.player = j
					nb = cocos.sprite.Sprite('blank.png')
					nb.x, nb.y =j.sprite.x, j.sprite.y
					self.add(nb, z=1)
					self.add(j.sprite, z=2)
				else:
					self.add(j.sprite, z=1)
		
		
	def update(self, dt):
		self.player.sprite.x += 1	
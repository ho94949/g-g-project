import cocos

class Block:
	def __init__(self, type):
		self.type = type
		namemap = {}
		namemap['0'] = 'blank.png'
		namemap['1'] = 'dirt.png'
		namemap['S'] = 'human.png'
		self.sprite = cocos.sprite.Sprite(namemap[type])

class MapManager:
	def __init__(self):
		pass
	
	def load(self, path):
		f = open(path, 'r')
		w, h = map(int,f.readline().split())
		
		mapx = []
		for i in range(h):
			mapx.append(f.readline())
		
		f.close()
	
		ret = []
		for i in range(16):
			b = []
			for j in range(12):
				x = Block(mapx[j][i])
				x.sprite.position = i*64+x.sprite.width/2, 768-(j*64+x.sprite.height/2)
				b.append(x)
				
			ret.append(b)
		
		return ret
import cocos



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
	
		return mapx 
import stage
import map 

import cocos
from cocos.actions import *
from cocos.director import director
from cocos import audio

def main():
	
	director.init(width = 1024, height = 768, resizable=False, caption = "GGProject")
	
	mapManager = map.MapManager()
	
	stageMap = mapManager.load('stage1.map')
	
	StageFrame = stage.Stage(stageMap)
	
	scene = cocos.scene.Scene()
	scene.add(StageFrame)
	director.run(scene)
	
if __name__ == "__main__":
	main()

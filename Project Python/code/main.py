import pygame, sys
from settings import *
from level import *
from tile import *
from player import *
from debug import *

class Game:
	def __init__(self):
		#basic setup hiển thị khung cơ bản
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH, HIGH))
		self.clock = pygame.time.Clock()

		self.level = Level()
		pygame.display.set_caption('Hoang Hai An')

	#hàm run
	def run(self):
		while True:
			#vòng lặp các event xảy ra trong game
			for event in pygame.event.get():
				#kiểm tra xem event có phải là nút X end game hay không?
				if event.type == pygame.QUIT:
					#2 dòng để end game
					pygame.quit()
					sys.exit()
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
			#fill screen bằng màu
			self.screen.fill('black')

			self.level.run()
			pygame.display.update()
			#dòng này đặt ở cuối vòng lặp
			#về cơ bản thì màn hình hiển thị là sự nhấp nháy liên tục của ảnh
			self.clock.tick(FPS)

#phương thức run
if __name__ == '__main__':
	game = Game()
	game.run()
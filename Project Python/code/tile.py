#convert tile
import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
	def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
		super().__init__(groups)
		#convert_alpha() chuyển đổi hình ảnh
		self.sprite_type = sprite_type
		self.image = surface
		if sprite_type == 'object':
			self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILESIZE))
		else:
			self.rect = self.image.get_rect(topleft = pos)
		
		#chồng chéo các sprite
		#inflate() thay đổi size của hitbox
		#ý tưởng là giảm kích thước chiều dọc so với ban đầu của hcn. Thay đổi theo chiều dọc nên x=0 là tâm sẽ giữ nguyên
		#top and bottom sẽ giảm đi y/2
		self.hitbox = self.rect.inflate(0, -10)
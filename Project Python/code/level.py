import pygame
from settings import *
from tile import *
from player import *
from debug import *
from support import *
from random import choice
from weapon import Weapon

#Sprite là khái niệm để chỉ 1 ảnh nhỏ trong 1 ảnh lớn, ảnh lớn này có thể chứa nhiều sprite
class Level:
	def __init__(self):
		#bề mặt hiển thị
		self.display_surface = pygame.display.get_surface()
		#các nhóm đối tượng
		self.hienthi_sprites = YSortCameraGroup()
		self.chuongngaivat_sprites = pygame.sprite.Group()

		#attack sprites
		self.current_attack = None

		#thiết lập đối tượng
		self.create_map()

	#tạo map
	def create_map(self):
		layout = {
			#ranh giới
			'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
			#cỏ
			'grass': import_csv_layout('../map/map_Grass.csv'),
			#20 đối tượng
			'object': import_csv_layout('../map/map_Objects.csv'),
		}
		graphics = {
			'grass': import_folder('../graphics/Grass'),
			'objects': import_folder('../graphics/objects')
		}

		#style = 'boundary'
		for style, layout in layout.items():	
			#enumerate() để lấy bộ đếm và giá trị từ biến có thể lặp cùng một lúc
			#tạo 2 vòng lặp for để in ra index các hàng và cột
			for row_index, row in enumerate(layout):
				for column_index, column in enumerate(row):
					if column != '-1':	
						x = column_index * 64
						y = row_index * 64
						if style == 'boundary':
							Tile((x, y), [self.chuongngaivat_sprites], 'invisible')
						if style == 'grass':
							#create grass
							random_grass_image = choice(graphics['grass'])
							Tile((x, y), [self.hienthi_sprites, self.chuongngaivat_sprites], 'grass', random_grass_image)
						if style == 'object':
							#create object
							surf = graphics['objects'][int(column)]
							Tile((x, y), [self.hienthi_sprites, self.chuongngaivat_sprites], 'objects', surf)

		self.player = Player((2000, 1430), [self.hienthi_sprites], self.chuongngaivat_sprites, self.create_attack, self.destroy_attack)

	def create_attack(self):
		self.current_attack = Weapon(self.player, [self.hienthi_sprites])

	def destroy_attack(self):
		if self.current_attack:
			self.current_attack.kill()
			self.current_attack = None

	def run(self):
		#update và vẽ trò chơi
		self.hienthi_sprites.custom_draw(self.player)
		self.hienthi_sprites.update()
		debug(self.player.status)

#sắp xếp các sprite theo tọa độ y và tạo chồng chéo
class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):
		#thiết lập chung
		#gọi lớp cha tiếp theo
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		#lấy 1/2 screen theo chiều ngang
		self.half_width = self.display_surface.get_size()[0] // 2
		#lấy 1/2 screen theo chiều dọc
		self.half_high = self.display_surface.get_size()[1] // 2
		
	    #tạo ra 1 vector phần bù
		self.offset = pygame.math.Vector2()

		#create the floor
		self.floor_surf = pygame.image.load('../graphics/tilemap/ground.png').convert()
		self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

	#tạo bản vẽ tùy chỉnh
	def custom_draw(self, player):
		#getting the offset
		#truy cập và lấy ra vị trí của người chơi
		
		#player.rect.centerx - self.half_width camera di chuyển theo nhân vật theo chiều ngang
		self.offset.x = player.rect.centerx - self.half_width
		#player.rect.centerx - self.half_width camera di chuyển theo nhân vật theo chiều dọc
		self.offset.y = player.rect.centery - self.half_high
		
		#vẽ floor
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf, floor_offset_pos)

		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
		#for sprite in self.sprites():
			#vị trí bù đắp
			offset_pos = sprite.rect.topleft  - self.offset
			self.display_surface.blit(sprite.image, offset_pos)



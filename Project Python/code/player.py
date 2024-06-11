#convert player
import pygame
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, group, chuongngaivat_sprites, create_attack, destroy_attack):
		super().__init__(group)
		#convert_alpha() chuyển đổi hình ảnh
		self.image = pygame.image.load('../graphics/test/player.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
		#inflate() thay đổi size của hitbox
		#ý tưởng là giảm kích thước chiều dọc so với ban đầu của hcn. Thay đổi theo chiều dọc nên x=0 là tâm sẽ giữ nguyên
		#top and bottom sẽ giảm đi y/2
		self.hitbox = self.rect.inflate(0, -26)

		#graphics setup
		self.import_player_assets()
		self.status = 'down'
		self.frame_index = 0
		self.animation_speed = 0.05

		#MOVEMENT
		#thiết lập hướng di chuyển cho player
		#vector2d ban đầu mặc định là [x:0] x speed
		#			                  [y:0] x speed
		#giả sử là [x:5] thì player sẽ di chuyển sang phải với tốc độ 5pixel/khung hình
		#          [y:0]
		self.direction = pygame.math.Vector2()
		#input speed
		self.speed = 4
		#tạo bộ đếm thời gian
		self.attacking = False
		#thời gian hồi chiêu
		self.attack_cooldown = 400
		self.attack_time = None
		self.chuongngaivat_sprites = chuongngaivat_sprites

		#weapon
		self.create_attack = create_attack
		self.destroy_attack = destroy_attack
		self.weapon_index = 0
		self.weapon = list(weapon_data.keys())[self.weapon_index]


	#all file animation player
	def import_player_assets(self):
		character_path = '../graphics/player/'
		#None là animation cho player khi di chuyển ở 4 hướng
		#_idle là animation cho player khi đứng im ở 4 hướng
		#_attack là animation cho player khi tấn công ở 4 hướng
		self.animations = {'up': [], 'down':[], 'left': [], 'right': [],
			'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
			'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []}
		
		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	#input vector
	#input điều khiển
	def input(self):
		if not self.attacking:
			keys = pygame.key.get_pressed()

			#move input
			if keys[pygame.K_UP]:
			#set đi lên là y
				self.direction.y = -1
				self.status = 'up'
			elif keys[pygame.K_DOWN]:
				#set đi xuống là y
				self.direction.y = 1
				self.status = 'down'
			#khi nhấn cả UP và DOWN thì player không di chuyển
			else:
				self.direction.y = 0

			if keys[pygame.K_RIGHT]:
				#set đi sang phải là x
				self.direction.x = 1
				self.status = 'right'
			elif keys[pygame.K_LEFT]:
				#set đi sang trái là x
				self.direction.x = -1
				self.status = 'left'
			#khi nhấn cả RIGHT và LEFT thì player không di chuyển
			else:
				self.direction.x = 0

			#attack input
			#attack bằng space
			if keys[pygame.K_SPACE]:
				#tránh attack và skill cùng 1 lúc
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				self.create_attack()
			#magic input skill
			#skill bằng ctrl
			if keys[pygame.K_LCTRL]:
				#tránh attack và skill cùng 1 lúc
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				print('magic')	

	#trạng thái hiện tại của player
	def get_status(self):
		#idle status
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status + '_idle'

		#attack status
		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					#ghi đè idle
					self.status = self.status.replace('_idle', '_attack')
				else:
					self.status = self.status + '_attack'
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('_attack', '')

	#move and direction
	def move(self, speed):
		#fix lỗi di chuyển chéo nhanh hơn các hướng khác
		#magnitude() độ lớn của vector
		#if tránh TH là vector 0
		if self.direction.magnitude() != 0:
			#normalize() chuẩn hóa để player đi bất kì hướng nào thì self.direction cũng = 1
			self.direction = self.direction.normalize()
		self.hitbox.x += self.direction.x *speed
		self.vacham('horizontal')
		self.hitbox.y += self.direction.y *speed
		self.vacham('vertical')
		self.rect.center = self.hitbox.center

	#handle vacham
	def vacham(self, direction):
		#theo chiều ngang
		if direction == 'horizontal':
			for sprite in self.chuongngaivat_sprites:
				#cho biết là sprite và player có va chạm hay không
				if sprite.hitbox.colliderect(self.hitbox):
					#nếu player di chuyển sang phải và gặp chướng ngại vật bên phải thì cho player di chuyển sang trái
					if self.direction.x > 0:
						self.hitbox.right = sprite.hitbox.left
					#nếu player di chuyển sang trái và gặp chướng ngại vật bên trái thì cho player di chuyển sang phải
					if self.direction.x < 0:
						self.hitbox.left = sprite.hitbox.right
		
		#theo chiều dọc
		if direction == 'vertical':
			for sprite in self.chuongngaivat_sprites:
				#cho biết là sprite và player có va chạm hay không
				if sprite.hitbox.colliderect(self.hitbox):
					#nếu player di chuyển lên trên và gặp chướng ngại vật bên trên thì cho player di chuyển xuống dưới
					if self.direction.y < 0:
						self.hitbox.top = sprite.hitbox.bottom
					#nếu player di chuyển xuống dưới và gặp chướng ngại vật bên dưới thì cho player di chuyển lên trên
					if self.direction.y > 0:
						self.hitbox.bottom = sprite.hitbox.top

	#thiết lập thời gian
	def cooldowns(self):
		current_time = pygame.time.get_ticks()			
		#so sánh hiệu thời gian sau khi attack với thời gian hồi chiêu
		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.attacking = False
				
	#animations
	def animate(self):
		animation = self.animations[self.status]

		#lặp lại frame_index
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		#set image
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)
	
	def update(self):
		self.input()
		self.cooldowns()
		self.get_status()
		self.animate()
		self.move(self.speed)
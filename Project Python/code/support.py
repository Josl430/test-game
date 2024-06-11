import pygame
#thư viện để đọc tệp csv
from csv import reader
#walk đi qua tất cả các tệp trong hệ thống
from os import walk

#convert 1 file csv về dưới dạng bản đồ bằng cách đưa nó thành 1 danh sách chứa nhiều danh sách con
def import_csv_layout(path):
	#bản đồ này đưa về dạng danh sách
	terrain_map = []
	with open(path) as level_map:
		layout = reader(level_map, delimiter = ',')
		for row in layout:
			#đưa các phần tử của các hàng vào 1 danh sách
			terrain_map.append(list(row))
		return terrain_map

def import_folder(path):
	surface_list = []

	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			#print(full_path) #../graphics/Grass/grass_1.png
			image_surf = pygame.image.load(full_path).convert_alpha()
			surface_list.append(image_surf)
	return surface_list



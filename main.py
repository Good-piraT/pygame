import pygame
from random import randint
import sys, os


class Board: # класс, реализующий игровое поле

  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.board = [[0] * width for _ in range(height)]
    self.left = 10
    self.top = 10
    self.cell_size = 30

  def set_view(self, left, top, cell_size): #изменение расположение правого верхнего угла и размера клеток
    self.left = left
    self.top = top
    self.cell_size = cell_size

  def render(self, screen, color='black'): #
    for x in range(self.width):
      for y in range(self.height):
        elem = self.board[y][x]
        pygame.draw.rect(screen, color,
                         (self.left + self.cell_size * x, self.top +
                          self.cell_size * y, self.cell_size, self.cell_size),
                         2)

  def get_cell(self, mouse_pos): #дает координаты клетки при клике мышкой
    mx = mouse_pos[0]
    my = mouse_pos[1]
    rx, ry = (self.left, self.top)
    lx, ly = (self.left + self.cell_size * self.width,
              self.top + self.cell_size * self.height)
    if mx <= rx or mx >= lx or my <= ry or my >= ly:
      return None
    else:
      inner_mx = mx - self.left
      inner_my = my - self.top
      cell_column = inner_mx // self.cell_size
      cell_row = inner_my // self.cell_size
      return cell_row, cell_column

  def on_click(self, cell_coords): #пишет координаты клеток в консоль
    print(cell_coords)

  def get_click(self, mouse_pos): #связующий между get_cell и on_click
    cell = self.get_cell(mouse_pos)
    self.on_click(cell)

  def move(self, direction): #делает ход, двигая клетки в указанном направлении
    pass
  
  def ones(self): #добавляет еще одну единицу на доску в путом месте
    for row in range(4):
      x = randint(0, 1)
      if 0 in self.board[row] and x == 1:
        for elem in range(4):
          num_zeros, index = zero_count(self.board[row])
          q = randint(1, num_zeros)
          print(row, index, num_zeros, q)
          self.board[row][index[num_zeros]] = 1
          break


def zero_count(mass): #подсчет нулей в массиве
  count = -1
  index = []
  for i in range(len(mass)):
    if mass[i] == 0:
      count += 1
      index.append(i)
  return count, index #возвращает количество нулей и их индексы


pygame.init()
surf = pygame.display.set_mode((400, 400))
pygame.display.set_caption('1024')


def load_image(name, colorkey=None):
  fullname = os.path.join('data', name)
  if not os.path.isfile(fullname):
    print(f"Файл с изображением '{fullname}' не найден")
    sys.exit()
  image = pygame.image.load(fullname)
  return image


icon = load_image("icon.png")
pygame.display.set_icon(icon)
board = Board(4, 4)
board.set_view(0, 0, 100)
running = True
all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = load_image("1.png")
sprite.rect = sprite.image.get_rect()
sprite.rect.x = 5
sprite.rect.y = 20
all_sprites.add(sprite)
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    elif event.type == pygame.MOUSEBUTTONDOWN:
      board.get_click(event.pos)
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        running = False
      elif event.key == pygame.K_UP:
        board.move('up')
      elif event.key == pygame.K_DOWN:
        board.move('down')
      elif event.key == pygame.K_RIGHT:
        board.move('right')
      elif event.key == pygame.K_LEFT:
        board.move('left')

  surf.fill('white')
  board.render(surf)
  pygame.display.update()
pygame.quit()

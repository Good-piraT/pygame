import pygame
from random import randint
import sys, os


class Board:  # класс, реализующий игровое поле

  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.board = [[0] * width for _ in range(height)]
    self.change_board = [[0] * width for _ in range(height)]
    self.left = 10
    self.top = 10
    self.cell_size = 30

  def set_view(
      self, left, top, cell_size
  ):  #изменение расположение правого верхнего угла и размера клеток
    self.left = left
    self.top = top
    self.cell_size = cell_size

  def texting(self, number, coos):
    x = coos[0]
    y = coos[1]
    font = pygame.font.Font(None, 10)
    text = font.render(str(number), True, 'black')
    text_x = x - text.get_width() // 2
    text_y = y - text.get_height() // 2
    return text, (text_x, text_y)

  def render(self, screen, color='black'):  #рендер
    for x in range(self.width):
      for y in range(self.height):
        elem = self.board[y][x]
        if elem == 0:
          pygame.draw.rect(
              screen, 'black',
              (self.left + self.cell_size * x, self.top + self.cell_size * y,
               self.cell_size, self.cell_size), 2)
        else:

          if elem == 1:
            color = pygame.Color(199, 0, 57)
            text_mass = self.texting(1, (self.left + self.cell_size * x,
                                         self.top + self.cell_size * y))
          elif elem == 2:
            color = pygame.Color(255, 87, 51)
            text_mass = self.texting(2, (self.left + self.cell_size * x,
                                         self.top + self.cell_size * y))
          else:
            color = 'magenta'
            text_mass = self.texting(1134, (self.left + self.cell_size * x,
                                            self.top + self.cell_size * y))
          pygame.draw.rect(
              screen, color,
              (self.left + self.cell_size * x, self.top + self.cell_size * y,
               self.cell_size, self.cell_size))
          screen.blit(text_mass[0], text_mass[1])

  def get_cell(self, mouse_pos):  #дает координаты клетки при клике мышкой
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

  def get_button(self, mouse_pos):
    mouse_x = mouse_pos[0]
    mouse_y = mouse_pos[1]
    x = mouse_x >= 87 and mouse_x <= 87 + 226
    y = mouse_y >= 423 and mouse_y <= 54 + 423
    return x and y

  def button_act(self):
    print("I'M BUTTON")
    self.board = [[0] * self.width for _ in range(self.height)]
    self.ones(True)

  def on_click(self, cell_coords):  #пишет координаты клеток в консоль
    print('board cell', cell_coords)

  def get_click(self, mouse_pos):  #связующий между get_cell и on_click
    is_button = self.get_button(mouse_pos)
    cell = self.get_cell(mouse_pos)
    self.on_click(cell)
    if is_button:
      self.button_act()

  def check_row_right(self, row, elem):
      for i in range(3, -1, -1):
        print(i)
        if row[i] == 0:
          return 'trans', i
        if row[i] == elem:
          return 'plus', i
      return 'no move', -1
    
  def check_row_left(self, row, elem):
    for i in range(4):
      if row[i] == 0:
        no_move = False
        return 'trans', i
      if row[i] == elem:
        no_move = False
        return 'plus', i
    return 'no move', -1
        
  def move(self,
           direction):  #делает ход, двигая клетки в указанном направлении
    #считать кол-во клеток прохода
    break_rule = False
    if direction == 'right':
      for i in range(4):
        for q in range(3, -1, -1):
          row = self.board[i]
          elem = self.board[i][q]
          if elem > 0:
            movement_type, index = self.check_row_right(row, elem)
            print(movement_type, index)
            if movement_type == 'trans':
              self.board[i][q] = 0
              self.board[i][index] = elem
    elif direction == 'left':
      for i in range(4):
        for q in range(4):
          row = self.board[i]
          elem = self.board[i][q]
          if elem > 0:
            movement_type, index = self.check_row_left(row, elem)
            if movement_type == 'trans':
              self.board[i][q] = 0
              self.board[i][index] = elem
              
    elif direction == 'up':
      pass
    else:  #down
      pass
    #self.ones()
    print('ТАБЛИЦА:')
    for row in self.board:
      print(row)
  
  def ones(self,
           total=False):  #добавляет еще одну единицу на доску в путом месте
    br = False
    for row in range(4):
      x = randint(0, 1)
      if 0 in self.board[row] and x == 1:
        for elem in range(4):
          num_zeros, index = zero_count(
              self.board[row])  #количество нулей, тх индексы
          q = randint(0, num_zeros - 1)
          self.board[row][index[q]] = 1
          br = True
          break
        if br == True:
          break


pygame.init()
surf = pygame.display.set_mode((400, 500))
pygame.display.set_caption('1024')


def zero_count(mass):  #подсчет нулей в массиве
  count = 0
  index = []
  for i in range(len(mass)):
    if mass[i] == 0:
      count += 1
      index.append(i)
  return count, index  #возвращает количество нулей и их индексы


def draw_button(screen):
  font = pygame.font.Font(None, 50)
  text = font.render("NEW GAME!", True, 'black')
  text_x = 200 - text.get_width() // 2
  text_y = 450 - text.get_height() // 2
  text_w = text.get_width()
  text_h = text.get_height()
  screen.blit(text, (text_x, text_y))
  pygame.draw.rect(screen, 'black',
                   (text_x - 10, text_y - 10, text_w + 20, text_h + 20), 1)


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
b_color = pygame.Color(240, 248, 255)
running = True
board.ones()
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
        print('up')
        board.move('up')
      elif event.key == pygame.K_DOWN:
        print('down')
        board.move('down')
      elif event.key == pygame.K_RIGHT:
        print('right')
        board.move('right')
      elif event.key == pygame.K_LEFT:
        print('left')
        board.move('left')
  surf.fill(b_color)
  draw_button(surf)
  board.render(surf)
  pygame.display.update()
pygame.quit()

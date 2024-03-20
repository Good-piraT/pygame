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
        self.color_pallete = {}

    def set_view(
        self, left, top, cell_size
    ):  #изменение расположение правого верхнего угла и размера клеток
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen, color='black'):  #рендер таблицы
        for x in range(self.width):
            for y in range(self.height):
                elem = self.board[y][x]
                if elem == 0:  #рендер пустых клеток
                    pygame.draw.rect(
                        screen, 'black',
                        (self.left + self.cell_size * x, self.top +
                         self.cell_size * y, self.cell_size, self.cell_size),
                        2)
                else:  #рендер занятых клеток
                    text_mass = [
                        surf,
                        (self.left + self.cell_size * x * 1.5,
                         self.top + self.cell_size * y)
                    ]
                    #цвет + текст(в будущем), в зависимости от значения клетки
                    if elem not in self.color_pallete:
                        self.color_pallete[elem] = (randint(0, 255),
                                                    randint(0, 255),
                                                    randint(0, 255))
                    color = self.color_pallete[elem]
                    pygame.draw.rect(
                        screen, color,
                        (self.left + self.cell_size * x, self.top +
                         self.cell_size * y, self.cell_size, self.cell_size))
                    text(screen, elem, (self.left + self.cell_size * x,
                                        self.top + self.cell_size * y))

    def get_button(self, mouse_pos):  #детектит нажатие на кнопку
        mouse_x = mouse_pos[0]
        mouse_y = mouse_pos[1]
        x = mouse_x >= 87 and mouse_x <= 87 + 226
        y = mouse_y >= 423 and mouse_y <= 54 + 423
        return x and y

    def get_click(self, mouse_pos):  #активирует кнопку при клике мышкой
        if self.get_button(mouse_pos):
            self.board = [[0] * self.width for _ in range(self.height)]
            self.ones(True)

    def divide(self, mass, index, direction):
        new_mass = []
        if direction == 'left' or 'up':
            for i in range(4):
                if i < index:
                    new_mass.append(mass[i])
        else:  #right or down
            for i in range(4):
                if i > index:
                    new_mass.append(mass[i])
        return new_mass

    def check_row(self, direction, row, elem):
        #высчитывает тип движения (двигаться, не двигаться, слиться с другой клеткой)
        if direction == 'left' or 'up':
            for i in range(4):
                if row[i] == 0:
                    no_move = False
                    return 'move', i
                if row[i] == elem:
                    no_move = False
                    return 'trans', i
            return 'no move', -1
        else:  #right or down
            for i in range(3, -1, -1):
                if row[i] == 0:
                    return 'move', i
                if row[i] == elem:
                    return 'trans', i
            return 'no move', -1

    def move(self,
             direction):  #делает ход, двигая клетки в указанном направлении
        #общая суть для правого и левого движения - просмотреть каждый ненулевой элемент,
        #проверить его тип движения и двинуть, кудо нужно
        if direction == 'right':
            for i in range(4):
                for q in range(3, -1, -1):
                    row = self.board[i]
                    elem = self.board[i][q]
                    if elem > 0:
                        check_mass = self.divide(row, q, direction)
                        movement_type, index = self.check_row(
                            direction, check_mass, elem)
                        if q == 3:
                            movement_type = 'no move'
                        if movement_type == 'move':
                            self.board[i][q] = 0
                            self.board[i][index] = elem
                        elif movement_type == 'trans':
                            self.board[i][q] = 0
                            self.board[i][index] = elem * 2
        elif direction == 'left':
            for i in range(4):
                for q in range(4):
                    row = self.board[i]
                    elem = self.board[i][q]
                    if elem > 0:
                        check_mass = self.divide(row, q, direction)
                        movement_type, index = self.check_row(
                            direction, check_mass, elem)
                        if q == 0:
                            movement_type = 'no move'
                        if movement_type == 'move':
                            self.board[i][q] = 0
                            self.board[i][index] = elem
                        elif movement_type == 'trans':
                            self.board[i][q] = 0
                            self.board[i][index] = elem * 2
        #вверх и них работают так же, но для начала они 'переворчивают' все игровое поле
        #и пользуясь уже готовым алгоритмом действий и функциями высчитывают новое положение
        elif direction == 'up':
            disg_board = [[0] * self.width for _ in range(self.height)]
            for y in range(4):  # запись всех q элементов в disg_row[i]
                for x in range(4):
                    disg_board[y][x] = self.board[x][y - 4]
            for i in range(4):
                for q in range(4):
                    row = disg_board[i]
                    elem = disg_board[i][q]
                    if elem > 0:
                        check_mass = self.divide(row, q, direction)
                        movement_type, index = self.check_row(
                            direction, check_mass, elem)
                        if q == 0:
                            movement_type = 'no move'
                        if movement_type == 'move':
                            disg_board[i][q] = 0
                            disg_board[i][index] = elem
                        elif movement_type == 'trans':
                            disg_board[i][q] = 0
                            disg_board[i][index] = elem * 2
            for y in range(4):  # запись всех q элементов в disg_row[i]
                for x in range(4):
                    self.board[y][x] = disg_board[x][y - 4]
        else:  #down
            disg_board = [[0] * self.width for _ in range(self.height)]
            for y in range(4):  # запись всех q элементов в disg_row[i]
                for x in range(4):
                    disg_board[y][x] = self.board[x][y - 4]
            for i in range(4):
                for q in range(3, -1, -1):
                    row = disg_board[i]
                    elem = disg_board[i][q]
                    if elem > 0:
                        check_mass = self.divide(row, q, direction)
                        movement_type, index = self.check_row(
                            direction, check_mass, elem)
                        if q == 3:
                            movement_type = 'no move'
                        if movement_type == 'move':
                            disg_board[i][q] = 0
                            disg_board[i][index] = elem
                        elif movement_type == 'trans':
                            disg_board[i][q] = 0
                            disg_board[i][index] = elem * 2
            for y in range(4):  # запись всех q элементов в disg_row[i]
                for x in range(4):
                    self.board[y][x] = disg_board[x][y - 4]
        self.ones()
        print(direction)
        print('ТАБЛИЦА:')
        for i in range(4):
            print(self.board[i])

    def ones(self,
             total=False):  #добавляет еще одну единицу на доску в путом месте
        br = False
        for row in range(4):
            if total:
                ready = []
                for i in range(4):
                    if 0 in self.board[i]:
                        ready.append(i)
                y = randint(0, len(ready) - 1)
                row = ready[y]
                for elem in range(4):
                    num_zeros, index = zero_count(
                        self.board[row])  #количество нулей, тх индексы
                    q = randint(0, num_zeros - 1)
                    self.board[row][index[q]] = 1
                    br = True
                    break
                if br == True:
                    break
            else:
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


def text(screen, number, coos):
    x = coos[0]
    y = coos[1]
    font = pygame.font.Font(None, 75)
    text = font.render(str(number), True, 'black')
    text_x = x - text.get_width() // 20
    text_y = y - text.get_height() // 20
    screen.blit(text, (text_x, text_y))


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
b_color = pygame.Color(255, 245, 238)
running = True
board.ones(True)
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
    surf.fill(b_color)
    draw_button(surf)
    board.render(surf)
    pygame.display.update()
pygame.quit()

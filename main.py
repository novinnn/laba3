from tkinter import *
from random import choice

# Глобальные переменные
buttons = []  # Список кнопок
width, height = 16, 16  # Размер игрового поля
mines_count = width * height * 10 // 64  # Количество мин
field = []  # Список для хранения информации о поле
moves = 0  # Количество ходов
markers = 0  # Количество помеченных мин
first_click = True  # Флаг для первого хода

# Инициализация Tkinter
root = Tk()
root.title('Minesweeper')
root.geometry(f'{width * 40}x{height * 40}')

# Завершение игры

def end_game(win):
    for i in range(len(field)):
        if field[i] == -1:  # Если мина
            buttons[i].config(text='💣', bg='red' if not win else 'green', state=DISABLED)
        else:
            buttons[i].config(state=DISABLED)
    root.title("You Win!" if win else "Game Over")

# Обработка хода

def play(n):
    global moves, markers, first_click
    if buttons[n]["state"] == DISABLED:
        return

    if first_click:  # Если это первый ход
        first_click = False
        place_mines(n)
        calculate_adjacent_mines()

    if field[n] == -1:  # Если кликнули на мину
        buttons[n].config(text='💣', bg='red')
        end_game(False)
        return

    moves += 1
    buttons[n].config(text=str(field[n]) if field[n] > 0 else ' ', bg='lightgrey', state=DISABLED)

    if field[n] == 0:  # Если клетка пустая, открываем соседние
        open_neighbors(n)

    if moves == width * height - mines_count:  # Победа
        end_game(True)

# Пометка клеток флажками

def mark_cell(event, n):
    global markers
    if buttons[n]["state"] == DISABLED:
        return

    current_text = buttons[n]["text"]
    if current_text == '🚩':
        buttons[n].config(text='')
        markers -= 1
    else:
        buttons[n].config(text='🚩', fg='blue')
        markers += 1

# Открытие соседних клеток

def open_neighbors(n):
    queue = [n]
    visited = set()

    while queue:
        current = queue.pop(0)
        if current in visited:
            continue

        visited.add(current)
        row, col = divmod(current, width)

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue

                nr, nc = row + dr, col + dc
                if 0 <= nr < height and 0 <= nc < width:
                    neighbor = nr * width + nc
                    if buttons[neighbor]["state"] != DISABLED:
                        buttons[neighbor].config(text=str(field[neighbor]) if field[neighbor] > 0 else ' ', bg='lightgrey', state=DISABLED)
                        if field[neighbor] == 0:
                            queue.append(neighbor)

# Расстановка мин

def place_mines(first_click_index):
    global field
    placed_mines = 0

    while placed_mines < mines_count:
        index = choice(range(width * height))
        if field[index] == 0 and index != first_click_index:
            field[index] = -1
            placed_mines += 1

# Подсчёт мин вокруг клеток

def calculate_adjacent_mines():
    for i in range(len(field)):
        if field[i] == -1:
            continue

        count = 0
        row, col = divmod(i, width)

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue

                nr, nc = row + dr, col + dc
                if 0 <= nr < height and 0 <= nc < width:
                    neighbor = nr * width + nc
                    if field[neighbor] == -1:
                        count += 1

        field[i] = count

# Новая игра

def new_game(new_width=None, new_height=None):
    global field, buttons, moves, markers, first_click, width, height, mines_count
    if new_width and new_height:
        width, height = new_width, new_height
        mines_count = width * height * 10 // 64
    
    field = [0] * (width * height)
    moves = 0
    markers = 0
    first_click = True

    for widget in root.winfo_children():
        widget.destroy()

    create_grid()

# Создание игрового поля

def create_grid():
    global buttons
    buttons = []
    root.geometry(f'{width * 40}x{height * 40}')

    for r in range(height):
        frame = Frame(root)
        frame.pack(expand=True, fill=BOTH)
        for c in range(width):
            index = r * width + c
            button = Button(frame, text='', width=2, height=1, font=('Arial', 14), bg='grey', command=lambda n=index: play(n))
            button.bind('<Button-3>', lambda event, n=index: mark_cell(event, n))
            button.pack(side=LEFT, expand=True, fill=BOTH)
            buttons.append(button)

# Главное меню

def main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    Label(root, text="Choose Board Size", font=('Arial', 18)).pack(pady=20)

    Button(root, text="Small (8x8)", font=('Arial', 14), command=lambda: new_game(8, 8)).pack(pady=5)
    Button(root, text="Medium (10x10)", font=('Arial', 14), command=lambda: new_game(10, 10)).pack(pady=5)
    Button(root, text="Large (16x16)", font=('Arial', 14), command=lambda: new_game(16, 16)).pack(pady=5)

# Меню
menu = Menu(root)
game_menu = Menu(menu, tearoff=0)
game_menu.add_command(label="Main Menu", command=main_menu)
game_menu.add_command(label="New Game (16x16)", command=lambda: new_game(16, 16))
game_menu.add_command(label="New Game (10x10)", command=lambda: new_game(10, 10))
game_menu.add_command(label="New Game (8x8)", command=lambda: new_game(8, 8))
menu.add_cascade(label="Game", menu=game_menu)
root.config(menu=menu)

# Запуск главного меню
main_menu()
root.mainloop()

from tkinter import *
master = Tk()
w = Canvas(master, width=300, height=400, bg="#000000")
w.pack()

w.create_line(0, 200, 300, 200, fill="#00ff00")
w.create_line(0, 300, 300, 300, fill="#00ff00")
w.create_line(100, 100, 100, 400, fill="#00ff00")
w.create_line(200, 100, 200, 400, fill="#00ff00")
w.create_rectangle(0, 0, 301, 100, fill="#333333")

click = False
click_data = False
click_duration = 0
click_x = 0
click_y = 0
fresh_click = False
game_over_loop = 0
game_status = "Running"
letter_x = PhotoImage(file="x.gif")
letter_o = PhotoImage(file="o.gif")
letter = ["", 0]
main_count = 1
o_move = PhotoImage(file="o move.gif")
o_wins = PhotoImage(file="o wins.gif")
placing = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
turn = 0
x = 0
x_move = PhotoImage(file="x move.gif")
x_wins = PhotoImage(file="x wins.gif")
y = 0

def click_release(event):
    global click
    click = False

def click_set(event):
    global click, click_data, click_x, click_y, x, y
    click = True
    click_data = True
    click_x = event.x
    click_y = event.y
    x = event.x
    y = event.y

def click_in_range(x1, y1, x2, y2):
    global click_x, click_y, click_data
    if click_data:
        if click_x > x1:
            if click_x < x2:
                if click_y > y1:
                    if click_y < y2:
                        return True

def click_refresh():
    global click, click_duration, fresh_click
    if click == 1:
        if click_duration == 0:
            click_duration = 1
            fresh_click = True
        else:
            click_duration = 1
            fresh_click = False
    else:
        click_duration = 0
        fresh_click = False
    master.after(1, click_refresh)

def find_winner():
    global placing, game_status
    if placing[1] == 1:
        if placing[2] == 1:
            if placing[3] == 1:
                game_status = "o wins"
                game_update()
        if placing[5] == 1:
            if placing[9] == 1:
                game_status = "o wins"
                game_update()
        if placing[4] == 1:
            if placing[7] == 1:
                game_status = "o wins"
                game_update()
    if placing[2] == 1:
        if placing[5] == 1:
            if placing[8] == 1:
                game_status = "o wins"
                game_update()
    if placing[3] == 1:
        if placing[5] == 1:
            if placing[7] == 1:
                game_status = "o wins"
                game_update()
        if placing[6] == 1:
            if placing[9] == 1:
                game_status = "o wins"
                game_update()
    if placing[4] == 1:
        if placing[5] == 1:
            if placing[6] == 1:
                game_status = "o wins"
                game_update()
    if placing[7] == 1:
        if placing[8] == 1:
            if placing[9] == 1:
                game_status = "o wins"
                game_update()
    if placing[1] == 2:
        if placing[2] == 2:
            if placing[3] == 2:
                game_status = "x wins"
                game_update()
        if placing[5] == 2:
            if placing[9] == 2:
                game_status = "x wins"
                game_update()
        if placing[4] == 2:
            if placing[7] == 2:
                game_status = "x wins"
                game_update()
    if placing[2] == 2:
        if placing[5] == 2:
            if placing[8] == 2:
                game_status = "x wins"
                game_update()
    if placing[3] == 2:
        if placing[5] == 2:
            if placing[7] == 2:
                game_status = "x wins"
                game_update()
        if placing[6] == 2:
            if placing[9] == 2:
                game_status = "x wins"
                game_update()
    if placing[4] == 2:
        if placing[5] == 2:
            if placing[6] == 2:
                game_status = "x wins"
                game_update()
    if placing[7] == 2:
        if placing[8] == 2:
            if placing[9] == 2:
                game_status = "x wins"
                game_update()

def game_over():
    global game_status, game_over_loop
    if game_over_loop == 0:
        if game_status=="x wins":
            w.create_image((75, 200), image=x_wins, anchor="nw")
            game_over_loop = 1
        elif game_status=="o wins":
            w.create_image((75, 200), image=o_wins, anchor="nw")
            game_over_loop = 1
    else:
        if click_data:
            if fresh_click:
                if click_in_range(106, 255, 195, 283):
                    exit()
    master.after(1, game_over)
        

def game_update():
    global game_status
    if game_status == "x wins":
        print("X wins!")
        game_over()
    elif game_status == "o wins":
        print("O wins!")
        game_over()
                
def get_turn():
    global turn, letter
    turn += 1
    if is_odd(turn):
        letter[0] = letter_o
        letter[1] = 1
    else:
        letter[0] = letter_x
        letter[1] = 2

def is_odd(num):
    return num & 0x1

def scoreboard():
    global o_move, x_move
    if is_odd(turn):
        w.create_image((0, 0), image=x_move, anchor="nw")
    else:
        w.create_image((0, 0), image=o_move, anchor="nw")

def main():
    global click, main_count, click_data, click_x, click_y, letter
    if main_count == 1:
        click_refresh()
    main_count += 1
    scoreboard()
    if click_data:
        if fresh_click:
            if click_in_range(0, 100, 100, 200):
                get_turn()
                placing[1] = letter[1]
                w.create_image((1,101), image=letter[0], anchor="nw")
                find_winner()
            elif click_in_range(100, 100, 200, 200):
                get_turn()
                placing[2] = letter[1]
                w.create_image((101,101), image=letter[0], anchor="nw")
                find_winner()
            elif click_in_range(200, 100, 300, 200):
                get_turn()
                placing[3] = letter[1]
                w.create_image((201,101), image=letter[0], anchor="nw")
                find_winner()
            elif click_in_range(0, 200, 100, 300):
                get_turn()
                placing[4] = letter[1]
                w.create_image((1,201), image=letter[0], anchor="nw")
                find_winner()
            elif click_in_range(100, 200, 200, 300):
                get_turn()
                placing[5] = letter[1]
                w.create_image((101,201), image=letter[0], anchor="nw")
                find_winner()
            elif click_in_range(200, 200, 300, 300):
                get_turn()
                placing[6] = letter[1]
                w.create_image((201,201), image=letter[0], anchor="nw")
                find_winner()
            elif click_in_range(0, 300, 100, 400):
                get_turn()
                placing[7] = letter[1]
                w.create_image((1,301), image=letter[0], anchor="nw")
                find_winner()
            elif click_in_range(100, 300, 200, 400):
                get_turn()
                placing[8] = letter[1]
                w.create_image((101,301), image=letter[0], anchor="nw")
                find_winner()
            elif click_in_range(200, 300, 300, 400):
                get_turn()
                placing[9] = letter[1]
                w.create_image((201,301), image=letter[0], anchor="nw")
                find_winner()
    master.after(1, main)

main()
master.bind_all("<Button-1>", click_set)
master.bind_all("<ButtonRelease>", click_release)

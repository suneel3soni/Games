import random
from playing_field import *
from objects import I, T, O, J, L, S, Z


class Game_tetris():
    def __init__(self):
        self.canvas_ = win.return_canvas()  # canvas
        self.coordinate = win.return_table_coordinates()  # coordinates
        self.cells = self.create_game_cells()             # cells (true or false)
        self.cells2 = self.create_game_cells(n2=15)     # cells (true or false)
        self.im2 = None
        self.im = self.random_obj()  # create first item
        self.canvas_.bind("<Right>", self.im.turn_right)
        self.canvas_.bind("<Left>", self.im.turn_left)
        self.canvas_.bind("<Up>", self.im.expand)
        self.canvas_.bind("<Down>", self.im.turn_both)
        self.speed = 700  # game speed
        self.game_loop()
        self.imgl = []  # save img
        self.game_points = 0
        self.points = self.canvas_.create_text(250, 350, text=self.game_points)
        self.counter = 0
        win.mainloop()

    def create_game_cells(self, n2=10):
        table = {}
        lis = []
        for i in range(20):
            for j in range(n2):
                lis.append(False)
            table[i] = lis
            lis = []
        return table

    def del_window(self):
        exit()

    def game_loop(self):
        self.canvas_.bind("<Right>", self.im.turn_right)
        self.canvas_.bind("<Left>", self.im.turn_left)
        self.canvas_.bind("<Up>", self.im.expand)
        self.canvas_.bind("<Down>", self.im.turn_both)

        if self.im.get_item_status() != "passive":
            self.im.turn_both("<Down>")
            win.after(self.speed, self.game_loop)
        else:
            self.imgl.append(self.im)
            self.recovery_cells()
            self.im = None
            if self.cells[0][3] or self.cells[0][4] or self.cells[0][5] or self.cells[1][3] or self.cells[1][4] or self.cells[1][5]:
                self.canvas_.create_text(150, 200, text="Game over")
                win.after(5000, self.del_window)
                return None
            self.im = self.random_obj()

            ###################
            self.canvas_.bind("<Right>", self.im.turn_right)
            self.canvas_.bind("<Left>", self.im.turn_left)
            self.canvas_.bind("<Up>", self.im.expand)
            self.canvas_.bind("<Down>", self.im.turn_both)
            ###################
            win.after(self.speed, self.game_loop)

    random_obj_next = None

    def random_obj(self):
        def update_random_img(random_obj_next, objects_list):
            if self.random_obj_next == objects_list[0]:
                self.im2 = Z(self.canvas_, self.coordinate,
                             self.cells2, x=11, y=6)
            if self.random_obj_next == objects_list[1]:
                self.im2 = S(self.canvas_, self.coordinate,
                             self.cells2, x=11, y=6)
            if self.random_obj_next == objects_list[2]:
                self.im2 = I(self.canvas_, self.coordinate,
                             self.cells2, x=11, y=6)
            if self.random_obj_next == objects_list[3]:
                self.im2 = T(self.canvas_, self.coordinate,
                             self.cells2, x=11, y=6)
            if self.random_obj_next == objects_list[4]:
                self.im2 = O(self.canvas_, self.coordinate,
                             self.cells2, x=11, y=6)
            if self.random_obj_next == objects_list[5]:
                self.im2 = J(self.canvas_, self.coordinate,
                             self.cells2, x=11, y=6)
            if self.random_obj_next == objects_list[6]:
                self.im2 = L(self.canvas_, self.coordinate,
                             self.cells2, x=11, y=6)

        objects_list = [lambda: Z(self.canvas_, self.coordinate, self.cells),
                        lambda: S(self.canvas_, self.coordinate, self.cells),
                        lambda: I(self.canvas_, self.coordinate, self.cells),
                        lambda: T(self.canvas_, self.coordinate, self.cells),
                        lambda: O(self.canvas_, self.coordinate, self.cells),
                        lambda: J(self.canvas_, self.coordinate, self.cells),
                        lambda: L(self.canvas_, self.coordinate, self.cells),
                        ]
        if self.random_obj_next is None:
            self.random_obj_next = random.choice(objects_list)
            update_random_img(self.random_obj_next, objects_list)
            return random.choice(objects_list)()
        else:
            return_random_obj = self.random_obj_next
            self.random_obj_next = random.choice(objects_list)
            update_random_img(self.random_obj_next, objects_list)
            return return_random_obj()

    def recovery_cells(self):
        lines = []
        for i in self.imgl:
            for j in i.get_obj():
                if False not in self.cells[j.get()[0]]:
                    i.del_item2(j)
                    if j.get()[0] not in lines:
                        lines.append(j.get()[0])

        if len(lines) != 0:
            self.game_points += len(lines) * 100
            self.canvas_.delete(self.points)
            self.points = self.canvas_.create_text(250, 350, text=self.game_points)
            self.counter += len(lines)
            if self.counter > 5:
                self.speed -= 100
                self.counter = self.counter - 5
            for q in lines:
                for k in range(len(self.cells[q])):
                    self.cells[q][k] = False
            lines.sort()
            lines.reverse()
            while len(lines) != 0:
                for ob in self.imgl:
                    for o in ob.get_obj():
                        if o.get()[0] > lines[-1]:
                            continue
                        else:
                            o.move_both()
                lines.pop()

Game_tetris()

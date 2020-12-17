"""
figures
"""

from tkinter import *


class Obj():
    def __init__(self, parent, coordinate, cells, x, y, image):
        self.parent = parent
        self.coordinate = coordinate  # coordinates
        self.cells = cells  # cells
        self.x = x
        self.y = y
        self.image = PhotoImage(file="block.gif")
        self.item_id = self.create_obj()

    def del_item(self):
        return self.parent.delete(self.item_id)

    def create_obj(self):
        self.cells[self.y][self.x] = True
        return self.parent.create_image(self.coordinate[self.y][self.x][0], self.coordinate[self.y][self.x][1],
                                        image=self.image)

    def get(self):
        return([self.y, self.x])

    def set_(self, x, y):
        self.parent.delete(self.item_id)
        self.cells[self.y][self.x] = False
        self.x = x
        self.y = y
        self.cells[self.y][self.x] = True
        self.item_id = self.parent.create_image(self.coordinate[self.y][self.x][0], self.coordinate[self.y][self.x][1],
                                                image=self.image)

    def move_right(self):
        self.parent.delete(self.item_id)
        self.item_id = self.parent.create_image(self.coordinate[self.y][self.x+1][0], self.coordinate[self.y][self.x][1],
                                                image=self.image)
        self.cells[self.y][self.x+1] = True
        self.cells[self.y][self.x] = False
        self.x = self.x + 1

    def move_left(self):
        self.parent.delete(self.item_id)
        self.item_id = self.parent.create_image(self.coordinate[self.y][self.x-1][0], self.coordinate[self.y][self.x][1],
                                                image=self.image)
        self.cells[self.y][self.x-1] = True
        self.cells[self.y][self.x] = False
        self.x = self.x - 1

    def move_both(self):
        self.parent.delete(self.item_id)
        self.item_id = self.parent.create_image(self.coordinate[self.y+1][self.x][0], self.coordinate[self.y+1][self.x][1],
                                                image=self.image)
        self.cells[self.y+1][self.x] = True
        self.cells[self.y][self.x] = False
        self.y = self.y + 1

    def find_right(self):
        return ([self.y, self.x+1])

    def find_left(self):
        return ([self.y, self.x-1])

    def find_both(self):
        return ([self.y+1, self.x])


class I():
    orientation = "0"
    status = "active"
    image = PhotoImage(file="block.gif")

    def __init__(self, parent, coordinate, cells, x=3, y=0):
        self.parent = parent  # canvas
        self.coordinate = coordinate  # coordinates
        self.cells = cells  # cells
        self.obj0 = Obj(self.parent, self.coordinate, self.cells, x, y, self.image)
        self.obj1 = Obj(self.parent, self.coordinate, self.cells, x+1, y, self.image)
        self.obj2 = Obj(self.parent, self.coordinate, self.cells, x+2, y, self.image)
        self.obj3 = Obj(self.parent, self.coordinate, self.cells, x+3, y, self.image)
        self.obj = [self.obj3, self.obj2, self.obj1, self.obj0]  # order is important

    def del_item2(self, j):  # I can't remove an item from self.obj.
        list = []
        for i in self.obj:
            if i != j:
                list.append(i)
        self.obj = list
        j.del_item()

    def get_obj(self):
        return self.obj

    def get_item_status(self):
        return self.status

    def neighbors_right(self):
        coordinate_objs = []
        for i in self.obj:
            coordinate_objs.append(i.get())

        coordinate_objs_right = []
        for j in self.obj:
            coordinate_objs_right.append(j.find_right())
        res = []
        for ob in coordinate_objs_right:
            if ob in coordinate_objs:
                continue
            else:
                if ob[1] != 10:
                    res.append(ob)
                else:
                    return None
        if len(res) != 0:
            for q in res:
                if self.cells[q[0]][q[1]] == True:
                    return None
            return True

    def neighbors_left(self):
        coordinate_objs = []
        for i in self.obj:
            coordinate_objs.append(i.get())
        coordinate_objs_left = []
        for j in self.obj:
            coordinate_objs_left.append(j.find_left())
        res = []
        for ob in coordinate_objs_left:
            if ob in coordinate_objs:
                continue
            else:
                if ob[1] != -1:
                    res.append(ob)
                else:
                    return None
        if len(res) != 0:
            for q in res:
                if self.cells[q[0]][q[1]] == True:
                    return None
            return True

    def neighbors_bot(self):
        coordinate_objs = []
        for i in self.obj:
            coordinate_objs.append(i.get())
        coordinate_objs_both = []
        for j in self.obj:
            coordinate_objs_both.append(j.find_both())
        res = []
        for ob in coordinate_objs_both:
            if ob in coordinate_objs:
                continue
            else:
                res.append(ob)

        if len(res) != 0:
            for q in res:
                if q[0] >= 20:
                    return None
                if self.cells[q[0]][q[1]] == True:
                    return None
            return True

    def turn_right(self, event):
        if self.neighbors_right():
            for i in self.obj:
                i.move_right()

    def turn_left(self, event):
        self.obj.reverse()
        if self.neighbors_left():
            for i in self.obj:
                i.move_left()
        self.obj.reverse()

    def turn_both(self, event):
        if self.neighbors_bot():
            for i in self.obj:
                i.move_both()
        else:
            self.status = "passive"

    def expand(self, event):
        x = self.obj[2].get()[0] - 1
        y = self.obj[2].get()[1] - 1

        cor_obj = []

        for q in self.obj:
            cor_obj.append(q.get())

        for i in range(4):
            for j in range(4):
                if [x, y] in cor_obj:
                    y = y + 1
                    continue
                else:
                    if y < 0:
                        return None
                    try:
                        if self.cells[x][y] == True:
                                return None
                    except IndexError:
                        return None
                    except KeyError:
                        return None
                    y = y + 1

            x = x + 1
            y = self.obj[2].get()[1] - 1

        if self.orientation == "1":  # vertical

            x = self.obj1.get()[1]
            y = self.obj1.get()[0]

            self.obj0.set_(x-1, y)
            self.obj2.set_(x+1, y)
            self.obj3.set_(x+2, y)

            self.orientation = "0"

        else:  # horizontal
            x = self.obj1.get()[1]
            y = self.obj1.get()[0]

            self.obj0.set_(x, y-1)
            self.obj2.set_(x, y+1)
            self.obj3.set_(x, y+2)
            self.orientation = "1"


class O(I):
    def __init__(self, parent, coordinate, cells, x=3, y=0):
        self.parent = parent
        self.coordinate = coordinate
        self.cells = cells
        self.obj0 = Obj(self.parent, self.coordinate, self.cells, x, y, self.image)
        self.obj1 = Obj(self.parent, self.coordinate, self.cells, x+1, y, self.image)
        self.obj2 = Obj(self.parent, self.coordinate, self.cells, x, y+1, self.image)
        self.obj3 = Obj(self.parent, self.coordinate, self.cells, x+1, y+1, self.image)
        self.obj = [self.obj3, self.obj2, self.obj1, self.obj0]

    def expand(self, event): # this method is not needed
        pass


class T(I):
    def __init__(self, parent, coordinate, cells, x=3, y=0):
        self.parent = parent
        self.coordinate = coordinate
        self.cells = cells
        self.obj0 = Obj(self.parent, self.coordinate, self.cells, x, y+1, self.image)
        self.obj1 = Obj(self.parent, self.coordinate, self.cells, x+1, y, self.image)
        self.obj2 = Obj(self.parent, self.coordinate, self.cells, x+1, y+1, self.image)
        self.obj3 = Obj(self.parent, self.coordinate, self.cells, x+2, y+1, self.image)
        self.obj = [self.obj3, self.obj2, self.obj1, self.obj0]

    def checking_neighbors(self, x, y):
        cor_obj = []
        default_y = y
        for q in self.obj:
            cor_obj.append(q.get())

        for i in range(3):
            for j in range(3):
                if [x, y] in cor_obj:
                    y = y + 1
                    continue
                else:
                    if y < 0:
                        return None
                    try:
                        if self.cells[x][y] == True:
                            return None
                    except IndexError:
                        return None
                    except KeyError:
                        return None
                    y = y + 1
            x = x + 1
            y = default_y
        return True

    def expand(self, event):
        x = self.obj1.get()[0] - 1
        y = self.obj1.get()[1] - 1

        if self.checking_neighbors(x, y) != True:
            return None

        if self.orientation == "3":
            x = self.obj1.get()[1]
            y = self.obj1.get()[0]

            self.obj = [self.obj3, self.obj1, self.obj2, self.obj0]

            self.obj0.set_(x-1, y+1)
            self.obj2.set_(x, y+1)
            self.obj3.set_(x+1, y+1)
            self.orientation = "0"
            return None

        if self.orientation == "2":
            x = self.obj1.get()[1]
            y = self.obj1.get()[0]

            self.obj = [self.obj0, self.obj2, self.obj3, self.obj1]

            self.obj0.set_(x+1, y+1)
            self.obj2.set_(x+1, y)
            self.orientation = "3"

        if self.orientation == "1":

            x = self.obj1.get()[1]
            y = self.obj1.get()[0]

            self.obj3.set_(x+1, y-1)
            self.obj2.set_(x, y-1)

            self.orientation = "2"

        if self.orientation == "0":

            x = self.obj1.get()[1]
            y = self.obj1.get()[0]

            self.obj = [self.obj3, self.obj1, self.obj2, self.obj0]

            self.obj0.set_(x-1, y-1)
            self.obj2.set_(x-1, y)
            self.obj3.set_(x-1, y+1)
            self.orientation = "1"


class J(T):
    def __init__(self, parent, coordinate, cells, x=3, y=0):
        self.parent = parent
        self.coordinate = coordinate
        self.cells = cells
        self.obj0 = Obj(self.parent, self.coordinate, self.cells, x, y, self.image)
        self.obj1 = Obj(self.parent, self.coordinate, self.cells, x, y+1, self.image)
        self.obj2 = Obj(self.parent, self.coordinate, self.cells, x+1, y+1, self.image)
        self.obj3 = Obj(self.parent, self.coordinate, self.cells, x+2, y+1, self.image)
        self.obj = [self.obj3, self.obj2, self.obj1, self.obj0]

    def expand(self, event):
        x = self.obj2.get()[0] - 1
        y = self.obj2.get()[1] - 1

        if self.checking_neighbors(x, y) != True:
            return None

        if self.orientation == "3":

            x = self.obj2.get()[1]
            y = self.obj2.get()[0]

            self.obj = [self.obj3, self.obj2, self.obj1, self.obj0]

            self.obj0.set_(x-1, y-1)
            self.obj1.set_(x-1, y)
            self.obj3.set_(x+1, y)
            self.orientation = "0"
            return None

        if self.orientation == "2":

            x = self.obj2.get()[1]
            y = self.obj2.get()[0]

            self.obj = [self.obj3, self.obj2, self.obj1, self.obj0]

            self.obj0.set_(x, y-1)
            self.obj1.set_(x-1, y+1)
            self.obj3.set_(x, y+1)

            self.orientation = "3"

        if self.orientation == "1":
            x = self.obj2.get()[1]
            y = self.obj2.get()[0]

            self.obj = [self.obj1, self.obj3, self.obj2, self.obj0]

            self.obj0.set_(x-1, y)
            self.obj1.set_(x+1, y+1)
            self.obj3.set_(x+1, y)

            self.orientation = "2"

        if self.orientation == "0":

            x = self.obj2.get()[1]
            y = self.obj2.get()[0]

            self.obj0.set_(x, y-1)
            self.obj1.set_(x+1, y-1)
            self.obj3.set_(x, y+1)

            self.orientation = "1"


class L(T):
    def __init__(self, parent, coordinate, cells, x=3, y=0):
        self.parent = parent
        self.coordinate = coordinate
        self.cells = cells
        self.obj0 = Obj(self.parent, self.coordinate, self.cells, x+2, y, self.image)
        self.obj1 = Obj(self.parent, self.coordinate, self.cells, x, y+1, self.image)
        self.obj2 = Obj(self.parent, self.coordinate, self.cells, x+1, y+1, self.image)
        self.obj3 = Obj(self.parent, self.coordinate, self.cells, x+2, y+1, self.image)
        self.obj = [self.obj3, self.obj2, self.obj1, self.obj0]

    def expand(self, event):
        x = self.obj2.get()[0] - 1
        y = self.obj2.get()[1] - 1

        if self.checking_neighbors(x, y) != True:
            return None

        if self.orientation == "3":

            x = self.obj2.get()[1]
            y = self.obj2.get()[0]

            self.obj = [self.obj3, self.obj2, self.obj1, self.obj0]

            self.obj0.set_(x+1, y-1)
            self.obj1.set_(x-1, y)
            self.obj3.set_(x+1, y)
            self.orientation = "0"
            return None

        if self.orientation == "2":

            x = self.obj2.get()[1]
            y = self.obj2.get()[0]

            self.obj0.set_(x-1, y-1)
            self.obj1.set_(x, y-1)
            self.obj3.set_(x, y+1)

            self.orientation = "3"

        if self.orientation == "1":

            x = self.obj2.get()[1]
            y = self.obj2.get()[0]

            self.obj = [self.obj3, self.obj2, self.obj1, self.obj0]

            self.obj0.set_(x-1, y)
            self.obj1.set_(x-1, y+1)
            self.obj3.set_(x+1, y)

            self.orientation = "2"

        if self.orientation == "0":

            x = self.obj2.get()[1]
            y = self.obj2.get()[0]

            self.obj = [self.obj1, self.obj3, self.obj2, self.obj0]

            self.obj0.set_(x, y-1)
            self.obj1.set_(x+1, y+1)
            self.obj3.set_(x, y+1)

            self.orientation = "1"


class S(T):
    def __init__(self, parent, coordinate, cells, x=3, y=0):
        self.parent = parent
        self.coordinate = coordinate
        self.cells = cells
        self.obj0 = Obj(self.parent, self.coordinate, self.cells, x, y+1, self.image)
        self.obj1 = Obj(self.parent, self.coordinate, self.cells, x+1, y, self.image)
        self.obj2 = Obj(self.parent, self.coordinate, self.cells, x+2, y, self.image)
        self.obj3 = Obj(self.parent, self.coordinate, self.cells, x+1, y+1, self.image)
        self.obj = [self.obj3, self.obj0, self.obj2, self.obj1]

    def expand(self, event):
        x = self.obj3.get()[0] - 1
        y = self.obj3.get()[1] - 1

        if self.checking_neighbors(x, y) != True:
            return None

        if self.orientation == "0":
            x = self.obj3.get()[1]
            y = self.obj3.get()[0]

            self.obj = [self.obj2, self.obj0, self.obj3, self.obj1]

            self.obj0.set_(x+1, y)
            self.obj2.set_(x+1, y+1)

            self.orientation = "1"

        else:
            x = self.obj3.get()[1]
            y = self.obj3.get()[0]

            self.obj = [self.obj3, self.obj0, self.obj2, self.obj1]

            self.obj0.set_(x-1, y)
            self.obj2.set_(x+1, y-1)

            self.orientation = "0"


class Z(T):
    def __init__(self, parent, coordinate, cells, x=3, y=0):
        self.parent = parent
        self.coordinate = coordinate
        self.cells = cells
        self.obj0 = Obj(self.parent, self.coordinate, self.cells, x, y, self.image)
        self.obj1 = Obj(self.parent, self.coordinate, self.cells, x+1, y, self.image)
        self.obj2 = Obj(self.parent, self.coordinate, self.cells, x+1, y+1, self.image)
        self.obj3 = Obj(self.parent, self.coordinate, self.cells, x+2, y+1, self.image)
        self.obj = [self.obj3, self.obj2, self.obj1, self.obj0]

    def expand(self, event):
        x = self.obj2.get()[0] - 1
        y = self.obj2.get()[1] - 1

        if self.checking_neighbors(x, y) != True:
            return None

        if self.orientation == "0":
            x = self.obj2.get()[1]
            y = self.obj2.get()[0]

            self.obj = [self.obj0, self.obj3, self.obj2, self.obj1]

            self.obj0.set_(x+1, y+1)

            self.orientation = "1"
        else:
            x = self.obj2.get()[1]
            y = self.obj2.get()[0]

            self.obj = [self.obj3, self.obj2, self.obj1, self.obj0]
            self.obj0.set_(x-1, y-1)
            self.orientation = "0"

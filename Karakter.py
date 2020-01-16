import time

# this class is used to represent player 1 and player 2's characters
class Karakter:

    def __init__(self, name: str, jumping: int, filepath1, filepath2, movement_speed, falling_speed=2, height=80, width=80, max_health=100):
        self.__name = name
        self.max_health = max_health
        self.__health = max_health
        self.jumping = jumping
        self.__coordinate = [0, 0]
        self.__weapon = None
        self.__image1 = filepath1
        self.__image2 = filepath2
        self.__movement_speed = movement_speed
        self.__falling_speed = falling_speed
        self.__direction = "RIGHT"
        self.height = height
        self.width = width
        self.walk_count = 0


    """
    this method is to trigger the character to fire
    doesn't have any parameter
    doesn't return anything
    """
    def fire(self):
        if self.__direction == "RIGHT":
            self.__weapon.firing(self.__coordinate[0] + self.width, self.__coordinate[1] + self.height // 2)
        else:
            self.__weapon.firing(self.__coordinate[0], self.__coordinate[1] + self.height // 2)

    """
    this method is to set the direction whether it's left or right, this affects the directions of the bullets too
    the parameter is the desired direction, can only be "LEFT" or "RIGHT" (string)
    doesn't return anything
    """
    def set_direction(self, new_direction):
        self.init_direction(new_direction)
        self.__weapon.direction = self.__direction

    def get_image1(self):
        return self.__image1

    def get_image2(self):
        return self.__image2

    def set_weapon(self, new_weapon):
        self.__weapon = new_weapon
        self.__weapon.direction = self.__direction

    def get_weapon(self):
        return self.__weapon

    def health_lost(self, damage):
        if damage > self.__health:
            damage = self.__health
        self.__health = self.__health - damage

    def get_health(self):
        return self.__health

    def set_health(self, new_health):
        self.__health = new_health

    def set_movement_speed(self, new_speed):
        self.__movement_speed = new_speed

    def get_movement_speed(self):
        return self.__movement_speed

    def movement(self, direction, x_limit_right, x_limit_left, y_limit_down, y_limit_up=0):
        if direction == "UP" :#lompat
            self.__coordinate[1] -= self.jumping
            if self.__coordinate[1] <= y_limit_up:
                self.__coordinate[1] = y_limit_up
        elif direction == "LEFT":#gerak k kiri
            self.__coordinate[0] -= self.__movement_speed
            if self.__coordinate[0] <= x_limit_left:
                self.__coordinate[0] = x_limit_left
        elif direction == "RIGHT":#gerak k kanan
            self.__coordinate[0] += self.__movement_speed
            if self.__coordinate[0] >= x_limit_right - self.width:
                self.__coordinate[0] = x_limit_right - self.width
        elif direction == "DOWN":#jatuh
            self.__coordinate[1] += self.__falling_speed
            if self.__coordinate[1] >= y_limit_down - self.height:
                self.__coordinate[1] = y_limit_down - self.height

    def init_coordinate(self, x, y):
        self.__coordinate[0] = x
        self.__coordinate[1] = y

    def get_coordinate(self):
        return self.__coordinate

    def init_direction(self, new_direction):
        self.__direction = new_direction

    def __repr__(self):
        string = ""
        string += "Name: " + self.__name + "; "
        string += "Jumping: " + str(self.jumping) + "; "
        string += "Movement Speed: " + str(self.__movement_speed) + "; "
        string += "Health: " + str(self.max_health)
        if self.__weapon is not None:
            string += "; Weapon: " + self.__weapon.name
        return string


class Weapon:
    def __init__(self, name: str, damage: int, interval, x_speed,  y_speed=0):
        self.name = name
        self.damage = damage
        self.fired_bullets = []
        self.min_fire_interval = interval
        self.last_shot = 0
        self.__x_speed = x_speed
        self.__y_speed = y_speed
        self.direction = ""
        self.coordinate = [0, 0]

    def firing(self, x, y):
        if (time.time() - self.last_shot) > self.min_fire_interval:
            self.fired_bullets.append([x, y])
            self.last_shot = time.time()

    def update_bullets_list(self, char_target: Karakter, x_limit):
        idx = 0
        while idx < len(self.fired_bullets):
            if self.direction == "RIGHT":
                if self.fired_bullets[idx][0] < self.coordinate[0]:
                    self.fired_bullets[idx][0] -= self.__x_speed
                else:
                    self.fired_bullets[idx][0] += self.__x_speed

            elif self.direction == "LEFT":
                if self.fired_bullets[idx][0] > self.coordinate[0]:
                    self.fired_bullets[idx][0] += self.__x_speed
                else:
                    self.fired_bullets[idx][0] -= self.__x_speed

            if self.fired_bullets[idx][0] <= 0 or self.fired_bullets[idx][0] >= x_limit:
                del self.fired_bullets[idx]
                continue

            # if bullets hits the enemy, bullets are deleted and method of losing health are applied to the target
            if self.fired_bullets[idx][0] >= char_target.get_coordinate()[0] and self.fired_bullets[idx][0] <= char_target.get_coordinate()[0] + char_target.width and self.fired_bullets[idx][1] >= char_target.get_coordinate()[1] and self.fired_bullets[idx][1] <= char_target.get_coordinate()[1] + char_target.height:
                del self.fired_bullets[idx]
                idx -= 1
                char_target.health_lost(self.damage)
            idx += 1

    def init_bullet_speed(self, x, y=0):
        self.__x_speed = x
        if y != 0:
            self.__y_speed = y

    def get_bullet_speed(self):
        return self.__x_speed, self.__y_speed

    def reset_bullets(self):
        self.fired_bullets = []

    def __repr__(self):
        string = ""
        string += "Name: " + self.name + "; "
        string += "Damage: " + str(self.damage) + "; "
        string += "Interval: " + str(self.min_fire_interval) + "; "
        string += "Travel Speed: " + str(self.__x_speed)
        return string

class Threeway(Weapon):
    def __init__(self, name: str, damage: int, interval, x_speed, y_speed):
        super().__init__(name, damage, interval, x_speed, y_speed)

    def firing(self, x, y):
        if (time.time() - self.last_shot) > self.min_fire_interval:
            self.fired_bullets.append([x, y, 'UP'])
            self.fired_bullets.append([x, y, 'HORIZONTAL'])
            self.fired_bullets.append([x, y, "DOWN"])
            self.last_shot = time.time()

    def update_bullets_list(self, char: Karakter, x_limit):
        x_speed, y_speed = self.get_bullet_speed()
        idx = 0
        while idx < len(self.fired_bullets):
            if self.fired_bullets[idx][2] == "UP":
                self.fired_bullets[idx][1] -= y_speed
            if self.fired_bullets[idx][2] == "DOWN":
                self.fired_bullets[idx][1] += y_speed

            if self.direction == "RIGHT":
                if self.fired_bullets[idx][0] < self.coordinate[0]:
                    self.fired_bullets[idx][0] -= x_speed
                else:
                    self.fired_bullets[idx][0] += x_speed

            elif self.direction == "LEFT":
                if self.fired_bullets[idx][0] > self.coordinate[0]:
                    self.fired_bullets[idx][0] += x_speed
                else:
                    self.fired_bullets[idx][0] -= x_speed

            if self.fired_bullets[idx][0] >= x_limit or self.fired_bullets[idx][0] <= 0:
                del self.fired_bullets[idx]
                # idx -= 1
                continue

            if self.fired_bullets[idx][0] >= char.get_coordinate()[0] and self.fired_bullets[idx][0] <= char.get_coordinate()[0] + char.width and self.fired_bullets[idx][1] >= char.get_coordinate()[1] and self.fired_bullets[idx][1] <= char.get_coordinate()[1] + char.height:
                del self.fired_bullets[idx]
                idx -= 1
                char.health_lost(self.damage)
            idx += 1


class Doublefire(Weapon):
    def __init__(self, name: str, damage: int, interval, x_speed, y_speed=0):
        super().__init__(name, damage, interval, x_speed, y_speed)

    def firing(self, x, y):
        if (time.time() - self.last_shot) > self.min_fire_interval:
            self.fired_bullets.append([x, y])
            self.fired_bullets.append([x - 20, y])
            self.last_shot = time.time()


class Quadruplefire(Weapon):
    def __init__(self, name: str, damage: int, interval, x_speed,y_speed=0):
        super().__init__(name, damage, interval, x_speed, y_speed)

    def firing(self, x, y):
        if (time.time() - self.last_shot) > self.min_fire_interval:
            self.fired_bullets.append([x, y])
            self.fired_bullets.append([x - 1, y])
            self.fired_bullets.append([x - 2, y])
            self.fired_bullets.append([x - 3, y])
            self.fired_bullets.append([x - 4, y])
            self.fired_bullets.append([x - 5, y])
            self.fired_bullets.append([x - 6, y])
            self.fired_bullets.append([x - 7, y])
            self.fired_bullets.append([x - 8, y])
            self.fired_bullets.append([x - 9, y])
            self.fired_bullets.append([x - 10, y])
            self.fired_bullets.append([x - 11, y])
            self.fired_bullets.append([x - 12, y])
            self.fired_bullets.append([x - 13, y])
            self.fired_bullets.append([x - 14, y])
            self.fired_bullets.append([x - 15, y])
            self.fired_bullets.append([x - 16, y])
            self.fired_bullets.append([x - 17, y])
            self.fired_bullets.append([x - 18, y])
            self.fired_bullets.append([x - 19, y])
            self.fired_bullets.append([x - 20, y])
            self.last_shot = time.time()

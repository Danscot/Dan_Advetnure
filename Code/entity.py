
import pygame

from Code.animation import AnimateSprite


class Entity(AnimateSprite):

    def __init__(self, name, x, y):

        super().__init__(name)

        self.image = self.get_image(0, 0)

        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect() # player rect

        self.position = [x, y]

        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)

        self.old_position = self.position.copy()

        self.default_speed = 2

        # entity stats

        self.stats = {
            "health": 100,

            "magic": 100,

            "power": 50,

            "defense": 45

        }

        self.health = 100

        self.magic = 100

    # Entity movement

    def save_position(self):

        self.old_position = self.position.copy()

    def move_up(self):

        self.position[1] -= self.speed

        self.change_animation("up")

    def move_down(self):

        self.position[1] += self.speed

        self.change_animation("down")

    def move_left(self):

        self.position[0] -= self.speed

        self.change_animation("left")

    def move_right(self):

        self.position[0] += self.speed

        self.change_animation("right")

    def move_back(self):

        self.position = self.old_position

        self.rect.topleft = self.position

        self.feet.midbottom = self.rect.midbottom

    # updating the entity xtics

    def update(self):

        self.rect.topleft = self.position

        self.feet.midbottom = self.rect.midbottom


class Enemy(Entity):

    def __init__(self, name, target, map_pos):

        super().__init__(name, 0, 0)

        self.player = target

        self.name = map_pos

        self.speed = 1.5

    def basic_position(self, map):

        point = map.get_object(self.name)

        self.rect = pygame.Rect(point.x, point.y, point.width, point.height)

    def teleport_spawn(self):

        self.position[0] = self.rect.x

        self.position[1] = self.rect.y

        self.save_position()

    def monsters_movement(self):

        target_rect_x = self.player.old_position[0]

        target_rect_y = self.player.old_position[1]

        if target_rect_x-self.rect.x < 0:

            self.move_left()

        if target_rect_x - self.rect.x > 0:

            self.move_right()

        if target_rect_y - self.rect.y > 0:

            self.move_down()

        if target_rect_y - self.rect.y < 0:

            self.move_up()


class Player(Entity):

    def __init__(self, name, x, y):

        super().__init__("player", 0, 0)

        self.speed = 2


class NPC(Entity):

    def __init__(self, name, nb_points, dialog):

        super().__init__(name, 0, 0)

        self.nb_points = nb_points

        self.points = []

        self.current_point = 0

        self.name = name

        self.speed = 2

        self.dialog = dialog

    def teleport_spawn(self):

        location = self.points[self.current_point]

        self.position[0] = location.x

        self.position[1] = location.y

        self.save_position()

    def load_points(self, map):

        for num in range(1, self.nb_points + 1):

            point = map.get_object(f"{self.name}_{num}")

            rect = pygame.Rect(point.x, point.y, point.width, point.height)

            self.points.append(rect)

    def npcs_movement(self):

        current_point = self.current_point

        target_point = self.current_point + 1

        if target_point >= self.nb_points:

            target_point = 0

        current_rect = self.points[current_point]

        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 3:

            self.move_down()

        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 3:

            self.move_up()

        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 3:

            self.move_right()

        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 3:

            self.move_left()

        if self.rect.colliderect(target_rect):

            self.current_point = target_point






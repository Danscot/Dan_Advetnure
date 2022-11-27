
import pygame

import pyscroll

import pytmx

from dataclasses import dataclass

from Code.entity import *


@dataclass
class Portal:

    from_world: str

    origin_point: str

    target_world: str

    teleport_point: str


# creating a class that represent the map xtics
@dataclass
class Map:

    name: str

    walls: list[pygame.Rect]

    group: pyscroll.PyscrollGroup

    tmx_data: pytmx.TiledMap

    portals: list[Portal]

    npcs: list[NPC]

    enemies: list[Enemy]


class MapManager:

    def __init__(self, player):

        self.screen = pygame.display.get_surface()

        self.player = player

        # creating a dictionary that will store all map with their xtics
        self.maps = dict()

        self.current_map = 'world'

        # registring the maps xtics

        self.register_map('world', portal=[

            Portal(from_world="world", origin_point="enter_house", target_world="house", teleport_point="spawn_in_house"),

            Portal(from_world="world", origin_point="enter_libary", target_world="libary", teleport_point="spawn_in_libary"),

            Portal(from_world="world", origin_point="enter_dongeon", target_world="dongeon", teleport_point="spawn_in_dongeon")
        ], npcs=[

            NPC("paul", nb_points=10, dialog=["Good morning my name is Paul", "Welcome to the test Land", "Try your best to survive !!"])

        ])

        self.register_map('house', portal=[

            Portal(from_world="house", origin_point="exit_house", target_world="world", teleport_point="spawn_out_house")
        ])

        self.register_map('libary', portal=[

            Portal(from_world="libary", origin_point="exit_libary", target_world="world", teleport_point="spawn_out_libary",)
        ])

        self.register_map('dongeon', portal=[

            Portal(from_world="dongeon", origin_point="exit_dongeon", target_world="world", teleport_point="spawn_out_dongeon")
        ], enemies=[

            Enemy("enemy", self.player, "enemy1")
        ])

        self.teleport('player')

        self.teleport_npcs()

        self.teleport_enemies()

    def teleport_enemies(self):

        for map in self.maps:

            map_data = self.maps[map]

            enemies = map_data.enemies

            for enemie in enemies:

                enemie.basic_position(self)

                enemie.teleport_spawn()

    def check_npc_collision(self, dialog):

        for sprite in self.get_group().sprites():

            if sprite.feet.colliderect(self.player.rect) and type(sprite) is NPC:

                dialog.execute(sprite.dialog)

    def monster_collision(self):

        for sprite in self.get_group().sprites:

            if type(sprite) is Enemy:

                if sprite.feet.colliderect(sprite):

                    sprite.move_back()

                if sprite.feet.colliderect(self.player):

                    self.player.health -= 1

    def collision_checker(self):

        # for portals

        for portal in self.get_map().portals:

            if portal.from_world == self.current_map:

                point = self.get_object(portal.origin_point)

                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):

                    copy_portal = portal

                    self.current_map = portal.target_world

                    self.teleport(copy_portal.teleport_point)

        # for OTHER

        for sprite in self.get_group().sprites():

            # checking collision btw the NPC and player

            if type(sprite) is NPC:

                if sprite.feet.colliderect(self.player.rect):

                    sprite.speed = 0

                    self.player.health -= 1

                else:

                    sprite.speed = self.player.default_speed

            # checking collision btw sprite(player , ...) and walls

            if sprite.feet.collidelist(self.get_walls()) > -1:

                sprite.move_back()

            if type(sprite) is Enemy:

                enemy = sprite

                if sprite.feet.colliderect(self.player):

                    self.player.health -= 0.25

                if sprite.feet.collidelist(self.get_walls()) > -1:

                    sprite.move_back()

    def teleport(self, name):

            point = self.get_object(name)

            self.player.position[0] = point.x

            self.player.position[1] = point.y

            self.player.save_position()

    def register_map(self, name, portal=None, npcs=[], enemies=[]):

        # creating the map (tmx)

        tmx_data = pytmx.util_pygame.load_pygame(f"../Map/tmx_file/{name}.tmx")

        map_data = pyscroll.data.TiledMapData(tmx_data)

        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())

        map_layer.zoom = 2.30

        # creating the wall list

        walls = []

        for obj in tmx_data.objects:

            if obj.type == 'collision':

                walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        # drawing the layer group

        group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=6)

        group.add(self.player)

        # adding all npcs to the group

        for npc in npcs:

            group.add(npc)

        # adding the enemies to the group

        for enemy in enemies:

            group.add(enemy)

        # creating a map object

        self.maps[name] = Map(name, walls, group, tmx_data, portal, npcs, enemies)

    def get_map(self): return self.maps[self.current_map]

    def get_group(self): return self.get_map().group

    def get_walls(self): return self.get_map().walls

    def get_object(self, name): return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_npcs(self):

        for map in self.maps:

            map_data = self.maps[map]

            npcs = map_data.npcs

            for npc in npcs:

                npc.load_points(self)

                npc.teleport_spawn()

    def draw(self):

        self.get_group().draw(self.screen)

        self.get_group().center(self.player.rect.center)

    def update(self):

        self.get_group().update()

        self.collision_checker()

        for npc in self.get_map().npcs:

            npc.npcs_movement()

        for enemy in self.get_map().enemies:

            enemy.monsters_movement()







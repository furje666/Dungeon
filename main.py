import arcade
import math
import ctypes
import random


user32 = ctypes.windll.user32
SCREEN_WIDTH = user32.GetSystemMetrics(0)
SCREEN_HEIGHT = user32.GetSystemMetrics(1)


class MenuView(arcade.View):

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Menu Screen", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance.", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, x, y, button, modifiers):
        game = GameView()
        self.window.show_view(game)

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.fireball_timer = 0
        self.fireball_cast_timer = 0.5
        self.shoot_cd = False
        self.player_move = False
        self.onetime_health = True
        self.player_life = 5
        self.slime_spawn_timer = 10
        self.stage_timer = 10


        self.background = arcade.load_texture(file_name="images/background.png")


        self.wall_up_list = arcade.SpriteList()
        self.wall_down_list = arcade.SpriteList()
        self.wall_right_list = arcade.SpriteList()
        self.wall_left_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.crosshair_list = arcade.SpriteList()
        self.fireball_list = arcade.SpriteList()
        self.health_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
#player
        self.player = arcade.AnimatedWalkingSprite()
        self.character_scale = 1

        self.player.stand_right_textures = []
        self.player.stand_right_textures.append(arcade.load_texture("images/Mage_1.png",scale=self.character_scale))

        self.player.stand_left_textures = []
        self.player.stand_left_textures.append(arcade.load_texture("images/Mage_1.png",scale=self.character_scale,mirrored=True))

        self.player.walk_right_textures = []

        self.player.walk_right_textures.append(arcade.load_texture("images/Mage_1.png",scale=self.character_scale))
        self.player.walk_right_textures.append(arcade.load_texture("images/Mage_2.png",scale=self.character_scale))


        self.player.walk_left_textures = []

        self.player.walk_left_textures.append(arcade.load_texture("images/Mage_1.png",scale=self.character_scale,mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture("images/Mage_2.png",scale=self.character_scale,mirrored=True))


        self.player.texture_change_distance = 50

        self.player.center_x = SCREEN_WIDTH//2
        self.player.center_y = SCREEN_HEIGHT//2
        self.player.scale = 1
        self.player_list.append(self.player)

#walls
        self.wall = arcade.Sprite("images/wall.png")
        self.wall.center_x = SCREEN_WIDTH//2
        self.wall.center_y = 100
        self.wall_down_list.append(self.wall)

        self.wall = arcade.Sprite("images/wall.png")
        self.wall.center_x = SCREEN_WIDTH//2
        self.wall.center_y = SCREEN_HEIGHT-100
        self.wall_up_list.append(self.wall)

        self.wall = arcade.Sprite("images/wall_y.png")
        self.wall.center_x = 100
        self.wall.center_y = SCREEN_HEIGHT//2
        self.wall_left_list.append(self.wall)

        self.wall = arcade.Sprite("images/wall_y.png")
        self.wall.center_x = SCREEN_WIDTH-100
        self.wall.center_y = SCREEN_HEIGHT//2
        self.wall_right_list.append(self.wall)

#crosshair
        self.crosshair = arcade.Sprite("images/crosshair.png")
        self.crosshair.center_x = SCREEN_WIDTH//2
        self.crosshair.center_y = SCREEN_HEIGHT//2
        self.crosshair.scale = 0.75
        self.crosshair_list.append(self.crosshair)


    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT,
                                      self.background)
        arcade.draw_text("{0:1}".format(int(self.stage_timer)), SCREEN_WIDTH/2, SCREEN_HEIGHT - 75, arcade.color.WHITE, 35, align="center", anchor_x="center",anchor_y="center")
        arcade.draw_text("x " + str(self.player_life), color=arcade.color.WHITE, start_x = 120, start_y= SCREEN_HEIGHT - 75, font_size= 45)
        self.enemy_list.draw()
        self.player_list.draw()
        self.crosshair_list.draw()
        self.fireball_list.draw()
        self.health_list.draw()



    def on_key_press(self, symbol, modifiers:int):
        if self.shoot_cd == False:
            if symbol == arcade.key.W:
                self.player.change_y = 5
            if symbol == arcade.key.S:
                self.player.change_y = -5
            if symbol == arcade.key.D:
                self.player.change_x = 5
            if symbol == arcade.key.A:
                self.player.change_x = -5
        if symbol == arcade.key.ESCAPE:
            # pass self, the current view, to preserve this view's state
            pause = PauseView(self)
            self.window.show_view(pause)


    def on_key_release(self, symbol, modifiers:int):
        if symbol == arcade.key.W:
            self.player.change_y = 0
        if symbol == arcade.key.S:
            self.player.change_y = 0
        if symbol == arcade.key.D:
            self.player.change_x = 0
        if symbol == arcade.key.A:
            self.player.change_x = 0

    def on_mouse_motion(self, x, y, dx, dy):
        self.crosshair.center_y = y
        self.crosshair.center_x = x
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        if self.fireball_timer < 0.1:
            self.shoot_cd = True

    def player_health(self):
        if self.onetime_health == True:
            health = arcade.Sprite(filename="images/player_health.png", scale=0.15, center_x= 60, center_y= SCREEN_HEIGHT - 50)
            self.health_list.append(health)
            self.onetime_health = False

    def slime_enemy(self):
        #slime = arcade.AnimatedWalkingSprite()
        #slime_scale = 1

        slime = arcade.Sprite(filename="images/slime_1.png")

        #slime.stand_left_textures = []
        #slime.stand_left_textures.append(arcade.load_texture("images/slime_1.png",scale=slime_scale))

        #slime.stand_right_textures = []
        #slime.stand_right_textures.append(arcade.load_texture("images/slime_1.png", scale=slime_scale,mirrored=True))

        #slime.walk_right_textures = []
        #slime.walk_right_textures.append(arcade.load_texture("images/slime_1.png",scale=slime_scale,mirrored=True))
        #slime.walk_right_textures.append(arcade.load_texture("images/slime_2.png",scale=slime_scale,mirrored=True))

        #slime.walk_left_textures = []
        #slime.walk_left_textures.append(arcade.load_texture("images/slime_1.png",scale=slime_scale))
        #slime.walk_left_textures.append(arcade.load_texture("images/slime_2.png",scale=slime_scale))

        #slime.texture_change_distance = 50

        slime.center_y = random.randrange(200, SCREEN_HEIGHT-200)
        slime.center_x = random.randrange(200, SCREEN_WIDTH-100)
        slime_coords_spawn_x = False
        slime_coords_spawn_y = False

        while slime_coords_spawn_x == False:
            if slime.center_x < self.player.center_x + 100 and slime.center_x > self.player.center_x - 100:
                slime.center_x = random.randrange(200, SCREEN_WIDTH)
            else:
                slime_coords_spawn_x = True


        while slime_coords_spawn_y == False:
            if slime.center_y < self.player.center_y + 100 and slime.center_y > self.player.center_y - 100:
                slime.center_y = random.randrange(200, SCREEN_HEIGHT)
            else:
                slime_coords_spawn_y = True


        self.enemy_list.append(slime)



    def fireball(self):
        fireball = arcade.Sprite(filename= "images/fireball1.png",scale=0.15)
        #fireball = arcade.AnimatedTimeSprite()
        #fireball_scale = 0.25

        #fireball.textures = []
        #fireball.textures.append(arcade.load_texture("images/fireball1.png", scale=fireball_scale))
        #fireball.textures.append(arcade.load_texture("images/fireball2.png", scale=fireball_scale))
        #fireball.textures.append(arcade.load_texture("images/fireball3.png", scale=fireball_scale))


        start_x = self.player.center_x
        start_y = self.player.center_y + 50
        fireball.center_x = start_x
        fireball.center_y = start_y

        dest_x = self.mouse_x
        dest_y = self.mouse_y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        fireball.angle = math.degrees(angle)

        fireball.change_x = math.cos(angle) * 5
        fireball.change_y = math.sin(angle) * 5

        self.fireball_list.append(fireball)

        self.fireball_timer = 1
        self.fireball_cast_timer = 0


    def update(self, delta_time):

        self.crosshair_list.update()
        self.health_list.update()
        self.player_health()
        self.enemy_list.update()

        self.fireball_list.update()
        self.fireball_list.update_animation()

        self.player_list.update()
        self.player_list.update_animation()

        self.slime_spawn_timer += delta_time

        if self.fireball_timer > 0:
            self.fireball_timer -= delta_time

        self.stage_timer -= delta_time


#fireball_cast_animation
        if self.fireball_cast_timer > 0:
            self.fireball_cast_timer -= delta_time
        if self.fireball_cast_timer < 0.1 and self.player_move == False and self.shoot_cd == True:
            self.player.stand_right_textures.clear()
            self.player.stand_right_textures.append(arcade.load_texture("images/Mage_3.png",scale = self.character_scale))
            self.player.stand_left_textures.clear()
            self.player.stand_left_textures.append(arcade.load_texture("images/Mage_3.png",scale = self.character_scale,mirrored=True))
            self.fireball_cast_timer = 1
        if self.fireball_cast_timer < 0.87 and self.fireball_cast_timer > 0.5 and self.player_move == False and self.shoot_cd == True:
            self.player.stand_right_textures.clear()
            self.player.stand_right_textures.append(arcade.load_texture("images/Mage_4.png",scale = self.character_scale))
            self.player.stand_left_textures.clear()
            self.player.stand_left_textures.append(arcade.load_texture("images/Mage_4.png",scale=self.character_scale,mirrored=True))
            self.fireball_cast_timer = 1.5
        if self.fireball_cast_timer < 1.37 and self.fireball_cast_timer > 1 and self.player_move == False and self.shoot_cd == True:
            self.player.stand_right_textures.clear()
            self.player.stand_right_textures.append(arcade.load_texture("images/Mage_5.png",scale = self.character_scale))
            self.player.stand_left_textures.clear()
            self.player.stand_left_textures.append(arcade.load_texture("images/Mage_5.png",scale=self.character_scale,mirrored=True))
            self.fireball_cast_timer = 2
        if self.fireball_cast_timer < 1.87 and self.fireball_cast_timer > 1.5 and self.player_move == False and self.shoot_cd == True:
            self.fireball()
            self.player.stand_right_textures.clear()
            self.player.stand_right_textures.append(arcade.load_texture("images/Mage_1.png",scale = self.character_scale))
            self.player.stand_left_textures.clear()
            self.player.stand_left_textures.append(arcade.load_texture("images/Mage_1.png",scale=self.character_scale,mirrored=True))
            self.fireball_cast_timer = 0
            self.shoot_cd = False


#slime_movement + spawn

        if self.slime_spawn_timer > 5:
            self.slime_enemy()
            self.slime_spawn_timer = 0
        for slime in self.enemy_list:
            if self.player.center_x > slime.center_x:
                slime.change_x = 1
            else:
                slime.change_x = -1
            if self.player.center_y > slime.center_y:
                slime.change_y = 1
            else:
                slime.change_y = -1


#game_over
        if self.player_life < 1:
            arcade.close_window()
            print("Noob, you lost.")


#slime hitbox
        slime_hit_with_player = arcade.check_for_collision_with_list(self.player, self.enemy_list)
        for slime in slime_hit_with_player:
            self.player_life -= 1
            slime.kill()

        for slime in self.enemy_list:
            slime_hit_with_projectile = arcade.check_for_collision_with_list(slime, self.fireball_list)
            for slime_hit in slime_hit_with_projectile:
                slime.kill()

        for slime in self.enemy_list:
            if slime.bottom > SCREEN_HEIGHT - 150 or slime.top < 150 or slime.right < 150 or slime.left > SCREEN_WIDTH - 150:
                slime.kill()


#wall_hitbox
        wall_down_hit_list = arcade.check_for_collision_with_list(self.player, self.wall_down_list)
        for wall in wall_down_hit_list:
            self.player.center_y += 5

        wall_up_hit_list = arcade.check_for_collision_with_list(self.player, self.wall_up_list)
        for wall in wall_up_hit_list:
            self.player.center_y -= 5

        wall_left_hit_list = arcade.check_for_collision_with_list(self.player, self.wall_left_list)
        for wall in wall_left_hit_list:
            self.player.center_x += 5

        wall_right_hit_list = arcade.check_for_collision_with_list(self.player, self.wall_right_list)
        for wall in wall_right_hit_list:
            self.player.center_x -= 5


#fireball_hitbox
        for fireball in self.fireball_list:
            if fireball.bottom > SCREEN_HEIGHT - 200 or fireball.top < 200 or fireball.right < 200 or fireball.left > SCREEN_WIDTH - 200:
                fireball.kill()


class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view


    def on_show(self):
        arcade.draw_text("PAUSED", SCREEN_WIDTH/2, SCREEN_HEIGHT/2+50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")


        # Show tip to return or reset
        arcade.draw_text("Press Esc. to return",
                         SCREEN_WIDTH/2,
                         SCREEN_HEIGHT/2,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Press Enter to reset",
                         SCREEN_WIDTH/2,
                         SCREEN_HEIGHT/2-30,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")


    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.game_view)
        elif symbol == arcade.key.ENTER:  # reset game
            game = GameView()
            self.window.show_view(game)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Instruction and Game Over Views Example", fullscreen=True)
    menu = MenuView()
    window.show_view(menu)
    arcade.run()


if __name__ == "__main__":
    main()

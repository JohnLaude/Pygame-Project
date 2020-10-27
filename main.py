# Platformer Game
import pygame as pg
import random 
from Config import *
from sprites import *
import math
from os import path

class Game:
    def __init__(self):
        # Initialize game window
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        # Loading the highscore file
        with open(path.join(self.dir, HS_FILE), 'w') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        # Cloud Images
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(pg.image.load(path.join(img_dir, 'cloud{}.png'.format(i))).convert())
        # Loading images from spritesheet
        self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))
        # Load sounds
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir,'Bunny_Hop.wav' ))
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir,'Powerup.wav' ))
        
    def new(self):
        # Start a new game
        self.score = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.player = Player(self)
        for plt in PLATFORM_LIST:
            Platform(self, *plt)
        self.mob_timer = 0
        pg.mixer.music.load(path.join(self.snd_dir, 'Polka.ogg'))
        for i in range(4):
            c = Cloud(self)
            c.rect.y += 500
        self.run()

    def run(self):
        # Game loop
        pg.mixer.music.play(loops = -1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(FADE)
    def update(self):
        # Game loop Update
        self.all_sprites.update()
        # Spawn Mob
        now = pg.time.get_ticks()
        if now - self.mob_timer > 5000 + random.choice([-1000, -500, 0 , 500, 1000]):
            self.mob_timer = now
            Mob(self)

        # Mob Collision?
        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, \
                                           pg.sprite.collide_mask)
        if mob_hits:
            self.playing = False
        # Collision Check
        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > hits[0].rect.bottom:
                        lowest = hit
                # Helps us fall off
                if self.player.pos.x < lowest.rect.right + 10 and \
                    self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.bottom:
                        self.player.pos.y = lowest.rect.top  
                        self.player.vel.y = 0
                        self.player.jumping = False

        # Update window to move up with player
        if self.player.rect.top <= HEIGHT/ 4:
            if random.randrange(100) < CLOUD_FREQ:
                Cloud(self)
            self.player.pos.y += max(abs(self.player.vel.y),2) ## Needs to let player move while scrolling 
            for plt in self.platforms:
                plt.rect.y += max(abs(self.player.vel.y),2)
                if plt.rect.top > HEIGHT:
                    plt.kill()
                    self.score += 10
            for m in self.mobs:
                m.rect.y += max(abs(self.player.vel.y),2)
            for c in self.clouds:
                c.rect.y += max(abs(self.player.vel.y / 2),2)

        # If player hits powerup
        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for power in pow_hits:
            if power.type == 'boost':
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False
                self.boost_sound.play()
        # Death
        if self.player.rect.bottom > HEIGHT:
            # simulate falling 
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
            # Ends the game
        if len(self.platforms) == 0:
            self.playing = False

        # Spawn new platform
        while len(self.platforms) < 7:
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0, WIDTH-width), 
                         random.randrange(-44, -30))
            

    def events(self):
        # Game loop Events
        for event in pg.event.get():
        # Check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                        self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()
    def draw(self):
        # Game loop Draw
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, TXT_COLOR, WIDTH / 2, 15)
        #Display Flip 
        pg.display.flip()

    def show_start_screen(self):
        # Game start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, TXT_COLOR, WIDTH / 2, HEIGHT/ 4)
        self.draw_text("A for left, D for right, Space to jump", 22, TXT_COLOR, WIDTH / 2, HEIGHT/ 2)
        self.draw_text("Press a key to begin", 22, TXT_COLOR, WIDTH/ 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str(self.highscore), 22, TXT_COLOR, WIDTH/ 2, 15)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # Game over screen
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, TXT_COLOR, WIDTH / 2, HEIGHT/ 4)
        self.draw_text("Score:" + str(self.score), 22, TXT_COLOR, WIDTH / 2, HEIGHT/ 2)
        self.draw_text("Press a key to play again", 22, TXT_COLOR, WIDTH/ 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            if self.score >= SCORE_TO_BEAT:
                self.draw_text("CONGRATULATIONS!!!!", 22, TXT_COLOR, WIDTH/2, HEIGHT / 2 + 40)
                self.draw_text("YOU ARE THE FIRST PERSON TO MAKE IT THIS FAR",22, TXT_COLOR, WIDTH/2, HEIGHT / 2 + 80)
                pg.mixer.music.load(path.join(self.snd_dir, 'Birthday.ogg'))
                pg.mixer.music.play(loops = -1)
            else:
                pg.mixer.music.load(path.join(self.snd_dir, 'Jovial.ogg'))
                pg.mixer.music.play(loops = -1)
                self.draw_text("NEW HIGH SCORE!!", 22, TXT_COLOR, WIDTH/2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, BLACK, WIDTH/ 2, HEIGHT / 2 + 40)
            self.draw_text("Better luck next time",22, TXT_COLOR, WIDTH/2, HEIGHT / 2 + 80)
            pg.mixer.music.load(path.join(self.snd_dir, 'GameOver.ogg'))
            pg.mixer.music.play(loops = -1)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(FADE)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


game = Game()
game.show_start_screen()
while game.running:
    game.new()
    game.show_go_screen()

pg.quit








from ursina import *
import random
import os

app = Ursina()

window.color = color.light_gray
camera.orthographic = True
camera.fov = 10

SAVE_FILE = 'highscore.txt'

def load_highscore():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as f:
            try: return int(f.read())
            except: return 0
    return 0

def save_highscore(score):
    with open(SAVE_FILE, 'w') as f:
        f.write(str(score))

class Tamagotchi(Entity):
    def __init__(self):
        super().__init__(
            model='quad',
            texture='cat_face.jpg',
            scale=(2, 2),
            position=(0, 0, 0),
            collider='box'
        )
        self.health = 100
        self.hunger = 0
        self.is_playing = False
        self.velocity_y = 0
        self.ground_y = -2
        self.is_alive = True
        self.score = 0
        self.highscore = load_highscore()

    def update(self):
        if not self.is_alive: return

        if self.is_playing:
            self.y += self.velocity_y * time.dt
            self.velocity_y -= 35 * time.dt 

            if self.y <= self.ground_y:
                self.y = self.ground_y
                self.velocity_y = 0
            
            hit_info = self.intersects()
            if hit_info.hit:
                self.stop_mini_game()
        else:
            self.hunger += time.dt * 1.0
            self.x = lerp(self.x, 0, time.dt * 3)
            self.y = lerp(self.y, 0, time.dt * 3)
            self.scale = 2 + math.sin(time.time() * 5) * 0.05

        if self.hunger >= 100: self.die()

    def jump(self):
        if self.y <= self.ground_y + 0.1:
            self.velocity_y = 14

    def die(self):
        self.is_alive = False
        self.animate_rotation_z(180, duration=0.5)
        self.color = color.black

    def stop_mini_game(self):
        if self.score > self.highscore:
            self.highscore = self.score
            save_highscore(self.highscore)
        
        self.is_playing = False
        for c in cacti: destroy(c)
        cacti.clear()
        self.shake()

pet = Tamagotchi()
cacti = []

status = Text(text='', position=(-0.8, 0.45), scale=1.3, color=color.black)
score_text = Text(text='', position=(0.5, 0.45), scale=1.3, color=color.dark_gray)

def update():
    status.text = f'Hunger: {int(pet.hunger)}% | Health: {int(pet.health)}%'
    score_text.text = f'Score: {pet.score}\nBest: {pet.highscore}'
    
    if pet.is_playing:
        if random.randint(1, 100) < 5: 
            if len(cacti) == 0 or cacti[-1].x < 5:
                h = random.uniform(1, 1.8)
                spike = Entity(
                    model = Mesh(vertices=[(-0.5,0,0), (0.5,0,0), (0,1,0)], triangles=[(0,1,2)]), 
                    color = color.gray, 
                    scale = (0.8, h), 
                    x = 12, 
                    y = -2.5, 
                    collider = 'box'
                )
                cacti.append(spike)
        
        for c in cacti[:]:
            c.x -= 10 * time.dt
            if c.x < -12:
                cacti.remove(c)
                destroy(c)
                pet.score += 1
                pet.hunger = max(0, pet.hunger - 0.5)

def input(key):
    if key == 'space' and pet.is_playing:
        pet.jump()

def start_play():
    if pet.is_alive:
        pet.is_playing = True
        pet.score = 0
        pet.x = -4
        pet.y = -2

def feed():
    if pet.is_alive and not pet.is_playing:
        pet.hunger = max(0, pet.hunger - 25)
        pet.animate_scale(2.6, duration=0.1)
        pet.animate_color(color.green, duration=0.1)
        invoke(setattr, pet, 'scale', 2, delay=0.2)
        invoke(setattr, pet, 'color', color.white, delay=0.2)

Button(text='Feed', color=color.azure, scale=(0.15, 0.08), position=(-0.3, -0.4), on_click=feed)
Button(text='Play', color=color.orange, scale=(0.15, 0.08), position=(0.3, -0.4), on_click=start_play)

app.run()
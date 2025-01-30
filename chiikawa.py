import tkinter as tk
import random
import os
import sys
import threading
from PIL import Image, ImageTk
from playsound3 import playsound

# 获取资源的绝对路径
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# 音效播放控制（避免短时间重复播放）
class SoundPlayer:
    def __init__(self):
        self.sounds_playing = {}
        self.sound_lock = threading.Lock()

    def play_sound(self, file_path):
        with self.sound_lock:
            if file_path in self.sounds_playing:
                return
            self.sounds_playing[file_path] = True

        def _play():
            playsound(file_path)
            with self.sound_lock:
                self.sounds_playing.pop(file_path, None)

        threading.Thread(target=_play, daemon=True).start()

# 游戏窗口类
class GameWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("烏薩奇吃檸檬")
        self.root.geometry("600x700")
        self.root.resizable(False, False)

        self.sound_player = SoundPlayer()
        self.load_background()
        self.load_images()

        self.score = 0
        self.running = False  # 控制游戏状态
        self.falling_objects = []
        self.fall_speed = 10  # 掉落速度

        self.score_text = self.canvas.create_text(50, 20, text=f"分數: {self.score}", font=("Arial", 16), fill="black")
        self.create_buttons()
        self.bind_events()

    def load_background(self):
        background_path = resource_path("resources/images/background_grass.png")
        background_image = Image.open(background_path).resize((600, 600))
        self.background_photo = ImageTk.PhotoImage(background_image)

        self.canvas = tk.Canvas(self.root, width=600, height=600)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.background_photo, anchor="nw")

    def load_images(self):
        self.rabbit_photo = self.load_image("resources/images/rabbit_upside_down.png", (100, 100))
        self.rabbit_get_lemon_photo = self.load_image("resources/images/rabbit_get_lemon.png", (100, 100))
        self.rabbit_spicy_photo = self.load_image("resources/images/rabbit_spicy.png", (100, 100))
        self.goblin_photo = self.load_image("resources/images/goblin.png", (100, 100))
        self.lemon_photo = self.load_image("resources/images/lemon.png", (60, 60))
        self.broccoli_photo = self.load_image("resources/images/brocoli.png", (60, 60))
        self.pepper_photo = self.load_image("resources/images/pepper.png", (60, 60))

        self.player = self.canvas.create_image(300, 500, image=self.rabbit_photo)

    def load_image(self, image_path, size):
        return ImageTk.PhotoImage(Image.open(resource_path(image_path)).resize(size))

    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        start_button = tk.Button(button_frame, text="Start", command=self.start_game)
        start_button.pack(side="left", padx=10)

        stop_button = tk.Button(button_frame, text="Stop", command=self.stop_game)
        stop_button.pack(side="left", padx=10)

        restart_button = tk.Button(button_frame, text="Clear", command=self.restart_game)
        restart_button.pack(side="left", padx=10)

    def bind_events(self):
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

    def move_left(self, event):
        x, _ = self.canvas.coords(self.player)
        if x > 25:
            self.canvas.move(self.player, -20, 0)

    def move_right(self, event):
        x, _ = self.canvas.coords(self.player)
        if x < 575:
            self.canvas.move(self.player, 20, 0)

    def start_game(self):
        if not self.running:
            self.running = True
            self.fall_speed = 10  # 重置掉落速度
            self.update_game()

    def stop_game(self):
        self.running = False

    def restart_game(self):
        self.stop_game()
        self.score = 0
        self.fall_speed = 10  # 确保每次重新开始时掉落速度都重置
        self.canvas.itemconfig(self.score_text, text=f"分數: {self.score}")
        for obj in self.falling_objects:
            self.canvas.delete(obj.image)
        self.falling_objects.clear()

    def update_game(self):
        if self.running:
            self.create_falling_object()
            self.update_falling_objects()
            self.root.after(50, self.update_game)

    def create_falling_object(self):
        if random.random() < 0.05:
            obj_type = random.choice(["lemon", "broccoli", "pepper"])
            image = getattr(self, f"{obj_type}_photo")
            self.falling_objects.append(FallingObject(self.canvas, image, obj_type, self.fall_speed))

    def update_falling_objects(self):
        for obj in self.falling_objects[:]:
            obj.fall()
            if obj.is_collided(self.player):
                self.handle_collision(obj)
            elif obj.y > 600:
                self.canvas.delete(obj.image)
                self.falling_objects.remove(obj)

    def handle_collision(self, obj):
        effects = {"lemon": (1, "wolayaha.wav", self.rabbit_get_lemon_photo),
                   "broccoli": (3, "ha.wav", self.goblin_photo),
                   "pepper": (-5, "yaha_spicy.wav", self.rabbit_spicy_photo)}
        
        score_change, sound, new_image = effects[obj.type]
        self.score += score_change
        self.sound_player.play_sound(resource_path(f"resources/audios/{sound}"))
        self.change_rabbit_state(new_image, 2000)
        
        self.canvas.itemconfig(self.score_text, text=f"分數: {self.score}")
        self.canvas.delete(obj.image)
        self.falling_objects.remove(obj)

    def change_rabbit_state(self, new_image, duration):
        self.canvas.itemconfig(self.player, image=new_image)
        self.root.after(duration, lambda: self.canvas.itemconfig(self.player, image=self.rabbit_photo))

# 物体类
class FallingObject:
    def __init__(self, canvas, image, obj_type, fall_speed):
        self.canvas = canvas
        self.image_obj = image
        self.x = random.randint(20, 580)
        self.y = 0
        self.image = canvas.create_image(self.x, self.y, image=self.image_obj)
        self.type = obj_type
        self.fall_speed = fall_speed  # 掉落速度

    def fall(self):
        self.canvas.move(self.image, 0, self.fall_speed)
        self.y += self.fall_speed

    def is_collided(self, player):
        px, py = self.canvas.coords(player)
        # Correcting the formula by removing the complex number operation
        distance = ((self.x - px) ** 2 + (self.y - py) ** 2) ** 0.5
        return distance < 40


def main():
    root = tk.Tk()
    GameWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()

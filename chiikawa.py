import tkinter as tk
import random
import os
import sys
import threading
from PIL import Image, ImageTk
from playsound3 import playsound


# 获取资源的绝对路径，适配开发和打包环境
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


# 加载音频并播放
def play_sound(file_path):
    def _play_sound():
        playsound(file_path)
    
    threading.Thread(target=_play_sound, daemon=True).start()


# 创建游戏窗口
class GameWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("烏薩奇吃檸檬")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(self.root, width=600, height=600, bg="skyblue")
        self.canvas.pack()

        self.score = 0
        self.score_text = self.canvas.create_text(50, 20, text=f"分數: {self.score}", font=("Arial", 16), fill="black")

        self.falling_objects = []

        self.load_images()
        self.bind_events()
        self.update_game()

    def load_images(self):
        # 加载图片
        self.rabbit_image = self.load_image("resources/images/rabbit_upside_down.png", (100, 100))
        self.rabbit_photo = ImageTk.PhotoImage(self.rabbit_image)
        self.lemon_image = self.load_image("resources/images/lemon.png", (60, 60))
        self.lemon_photo = ImageTk.PhotoImage(self.lemon_image)
        self.rabbit_get_lemon_image = self.load_image("resources/images/rabbit_get_lemon.png", (100, 100))
        self.rabbit_get_lemon_photo = ImageTk.PhotoImage(self.rabbit_get_lemon_image)

        # 创建玩家控制的兔子
        self.player = self.canvas.create_image(300, 500, image=self.rabbit_photo)

    def load_image(self, image_path, size):
        path = resource_path(image_path)
        image = Image.open(path).resize(size)
        return image

    def bind_events(self):
        # 绑定键盘事件
        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

    def move_left(self, event):
        x, y = self.canvas.coords(self.player)
        if x > 25:
            self.canvas.move(self.player, -20, 0)

    def move_right(self, event):
        x, y = self.canvas.coords(self.player)
        if x < 575:
            self.canvas.move(self.player, 20, 0)

    def update_game(self):
        # 更新游戏状态
        self.create_falling_object()
        self.update_falling_objects()

        # 游戏循环
        self.root.after(50, self.update_game)

    def create_falling_object(self):
        if random.random() < 0.05:
            self.falling_objects.append(FallingObject(self.canvas, self.lemon_photo))

    def update_falling_objects(self):
        for obj in self.falling_objects[:]:
            obj.fall()
            if obj.is_collided(self.player):
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"分數: {self.score}")
                play_sound(resource_path("resources/audios/wolayaha.wav"))  # 在后台播放音效
                self.canvas.itemconfig(self.player, image=self.rabbit_get_lemon_photo)
                
                # 延时恢复兔子图片
                self.root.after(3000, lambda: self.canvas.itemconfig(self.player, image=self.rabbit_photo))
                
                self.canvas.delete(obj.image)
                self.falling_objects.remove(obj)
            elif obj.y > 600:
                self.canvas.delete(obj.image)
                self.falling_objects.remove(obj)


class FallingObject:
    def __init__(self, canvas, lemon_photo):
        self.canvas = canvas
        self.lemon_photo = lemon_photo
        self.x = random.randint(20, 580)
        self.y = 0
        self.image = canvas.create_image(self.x, self.y, image=self.lemon_photo)

    def fall(self):
        self.canvas.move(self.image, 0, 10)
        self.y += 10

    def is_collided(self, player):
        player_coords = self.canvas.coords(player)
        player_x, player_y = player_coords[0], player_coords[1]
        distance = ((self.x - player_x) ** 2 + (self.y - player_y) ** 2) ** 0.5
        return distance < 40


# 创建主窗口并启动游戏
def main():
    root = tk.Tk()
    game = GameWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()

import turtle
import paho.mqtt.client as mqtt
import random
import threading
import time

class Game:
    def __init__(self, name_player):
        self.name_player = name_player
        self.jogadores = {}
        self.broker = "localhost"
        self.port = 1883
        self.topic = "/data"

        self.client_mqtt = mqtt.Client(name_player)
        self.client_mqtt.on_message = self.on_message
        self.client_mqtt.connect(self.broker, self.port)
        self.client_mqtt.subscribe(self.topic)
        self.client_mqtt.loop_start()

        self.delay = 0.06

        self.score = 0
        self.high_score = 0

        self.wn = None
        self.head = None

        self.screen_width = 500
        self.screen_height = 500

        self.is_key_pressed = False
        self.last_update_time = time.time()
        self.update_interval = 0.01  # Intervalo de atualização em segundos (ajuste conforme necessário)

    def go_up(self):
        self.head.direction = "up"
        self.is_key_pressed = True
        self.send_player_movement("up")

    def go_down(self):
        self.head.direction = "down"
        self.is_key_pressed = True
        self.send_player_movement("down")

    def go_left(self):
        self.head.direction = "left"
        self.is_key_pressed = True
        self.send_player_movement("left")

    def go_right(self):
        self.head.direction = "right"
        self.is_key_pressed = True
        self.send_player_movement("right")

    def release_key(self):
        self.is_key_pressed = False

    def close(self):
        self.wn.bye()
        self.client_mqtt.publish(self.topic, f"{self.name_player}: close")

    def move(self):
        screen_width = self.screen_width / 2
        screen_height = self.screen_height / 2

        if self.is_key_pressed:
            current_time = time.time()
            time_diff = current_time - self.last_update_time

            if time_diff >= self.delay:
                if self.head.direction == "up":
                    y = self.head.ycor() + 10
                    if y > screen_height:
                        y = -screen_height
                    self.head.sety(y)

                if self.head.direction == "down":
                    y = self.head.ycor() - 10
                    if y < -screen_height:
                        y = screen_height
                    self.head.sety(y)

                if self.head.direction == "left":
                    x = self.head.xcor() - 10
                    if x < -screen_width:
                        x = screen_width
                    self.head.setx(x)

                if self.head.direction == "right":
                    x = self.head.xcor() + 10
                    if x > screen_width:
                        x = -screen_width
                    self.head.setx(x)

                self.last_update_time = current_time

    def update_player_position(self, name, x, y, direction):
        if name != self.name_player:
            if name in self.jogadores:
                head = self.jogadores[name]
            else:
                head = turtle.Turtle()
                head.speed(0)
                head.shape("circle")
                head.color((random.random(), random.random(), random.random()))
                head.penup()
                head.goto(0, 0)
                head.direction = "stop"
                self.jogadores[name] = head

            step_size = 6

            if direction == "up":
                y = head.ycor() + step_size
                if y > self.screen_height:
                    y = -self.screen_height
                head.sety(y)
            elif direction == "down":
                y = head.ycor() - step_size
                if y < -self.screen_height:
                    y = self.screen_height
                head.sety(y)
            elif direction == "left":
                x = head.xcor() - step_size
                if x < -self.screen_width:
                    x = self.screen_width
                head.setx(x)
            elif direction == "right":
                x = head.xcor() + step_size
                if x > self.screen_width:
                    x = -self.screen_width
                head.setx(x)

            head.clear()
            head.write(name, align="center", font=("Courier", 16, "normal"))

    def send_player_movement(self, direction):
        message = f"{self.name_player}:{self.head.xcor()}:{self.head.ycor()}:{direction}"
        self.client_mqtt.publish(self.topic, message)

    def on_message(self, client, userdata, msg):
        jogador_info = msg.payload.decode().split(':')
        if len(jogador_info) == 4:
            name, x, y, direction = jogador_info
            self.update_player_position(name, float(x), float(y), direction)

    def run(self):
        self.wn = turtle.Screen()
        self.wn.title(f"Move Game by {self.name_player}")
        self.wn.bgcolor("black")
        self.wn.setup(width=self.screen_width, height=self.screen_height)
        self.wn.tracer(0)

        self.head = turtle.Turtle()
        self.head.speed(0)
        self.head.shape("circle")
        self.head.color((random.random(), random.random(), random.random()))
        self.head.penup()
        self.head.goto(0, 0)
        self.head.direction = "stop"
        self.head.name = self.name_player
        self.head.clear()
        self.head.write(self.name_player, align="center", font=("Courier", 16, "normal"))

        self.wn.listen()
        self.wn.onkeypress(self.go_up, "w")
        self.wn.onkeypress(self.go_down, "s")
        self.wn.onkeypress(self.go_left, "a")
        self.wn.onkeypress(self.go_right, "d")
        self.wn.onkey(self.release_key, "w")
        self.wn.onkey(self.release_key, "s")
        self.wn.onkey(self.release_key, "a")
        self.wn.onkey(self.release_key, "d")
        self.wn.onkeypress(self.close, "Escape")

        def game_loop():
            while True:
                self.move()
                self.wn.update()
                time.sleep(self.delay)

        t = threading.Thread(target=game_loop)
        t.daemon = True
        t.start()

        self.wn.mainloop()

if __name__ == "__main__":
    name_player = input("Digite seu nome: ")
    game = Game(name_player)
    game.run()

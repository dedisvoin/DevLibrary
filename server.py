import lib
import random


server = lib.Server(max_client_=10)


class Ball:
    def __init__(self) -> None:
        self.rad = random.randint(10, 50)
        self.pos = lib.Vector2(
            random.randint(0 + self.rad, 500 - self.rad),
            random.randint(0 + self.rad, 500 - self.rad),
        )
        self.color = lib.Color.random().rgb
        self.speed = lib.Vector2(random.randint(-5, 5), random.randint(-5, 5))

    def simulate(self):
        self.pos.x += self.speed.x
        self.pos.y += self.speed.y
        self.speed.x = (
            self.speed.x * -1
            if self.pos.x - self.rad < 0 or self.pos.x + self.rad > 500
            else self.speed.x * 1
        )
        self.speed.y = (
            self.speed.y * -1
            if self.pos.y - self.rad < 0 or self.pos.y + self.rad > 500
            else self.speed.y * 1
        )


balls = []


@lib.NewProcess
def waitcon():
    global balls
    while server.max_connected:
        server.waitcon(0.1)
        try:
            data = lib.packet_with_name(
                lib.string_to_list(server._end_conn_client.recv(1024).decode()), "id"
            )
            print(data)
        except:
            ...
        if server.clientcon:
            balls.append(Ball())


@lib.NewProcess
def simulate():
    while True:
        lib.sleep(0.01)
        [ball.simulate() for ball in balls]


@lib.NewProcess
def data_send():
    while True:
        lib.socket_sleep(0.01)
        data = list(
            map(lambda elem: [[elem.pos.x, elem.pos.y], elem.rad, elem.color], balls)
        )
        server.send_packet(lib.packing(data, "balls"))


waitcon()

simulate()
data_send()

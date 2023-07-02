import lib
import random

client = lib.Client()
id = random.randint(0, 99999)
print(id)
client.send_packet(lib.packing([id], "id"))
balls = []


@lib.NewProcess
def get_data():
    global balls
    while True:
        lib.socket_sleep(0.01)
        data = client.recv_packet()
        if data != "":
            try:
                data = lib.string_to_list(data)
                if lib.packet_with_name(data, "balls") is not None:
                    balls = lib.packet_with_name(data, "balls")
            except:
                ...


get_data()
win = lib.Window(size=[500, 500])

while win.update():
    [lib.Draw.draw_circle(win(), ball[0], ball[1], ball[2]) for ball in balls]

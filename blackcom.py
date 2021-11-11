import paho.mqtt.client as mqtt

verbosity = 1
last = None

def on_connect(client, userdata, flags, rc):

    if rc == 0:
        print("Connected to MQTT Broker!")

    else:
        print("Failed to connect, return code %d\n", rc)


def on_disconnect(client, userdata, rc):

    print('Client got disconnected')


def on_message(client, userdata, message):

    global verbosity
    global last

    last = message.payload.decode()

    if verbosity > 0:
        print("Message Received: " + last)


class BlackConnect:

    def __init__(self, 
                    broker = 'broker.hivemq.com', 
                    port = 1883, 
                    thread = 'fox/status/',
                    qos = 1,
                    client_id = 'BLKZN', 
                    username = 'generic', 
                    password = 'generic1',
                    verb = 1,
                    ):

        global verbosity
        verbosity = verb

        self.client = mqtt.Client()

        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        self.client.on_message = on_message

        self.client.connect(broker, port, 60)

        self.client.username_pw_set(username = username,password=password)

        self.client.subscribe([(thread, qos)])

    def refresh(self, t = 0.5):

        global last

        self.client.loop(timeout = t)

        return last

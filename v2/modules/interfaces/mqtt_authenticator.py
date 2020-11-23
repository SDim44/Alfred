#       Homestead MQTT Listener
#
#       Autor:              Stefan Dimnik
#       Date:               13.11.2020
#       Python:             3.7
#       Projekt Details:    https://github.com/SDim44/Homestead
#       ------------------------------------------------------------
#       
#       V0.1
#       Recieved MQTT messages and Authenticate devices
#       Save new devices in .pkl file
#   
#     ------------------------------------------------------------




def run(broker="localhost",port=1883,topic="homestead/Authentication/#"):

    # ------------------------------------------------------------------------------------------------------
    # Libraries
    
    import paho.mqtt.client as mqtt
    from uuid import getnode as get_mac

    # ------------------------------------------------------------------------------------------------------
    # MQTT Connect

    def on_connect(client, userdata, flags, rc):

        try:
            client.subscribe(topic)
        except:
            print("\n\n\tBroker is down!!!")

    # ------------------------------------------------------------------------------------------------------
    # MQTT Disconnect

    def on_disconnect(client, userdata, flags, rc):
        
        print("\tTrying to reconnect ...")
        client.subscribe(g_topic)


    # ------------------------------------------------------------------------------------------------------
    # MQTT message recieved

    def on_message(client, userdata, message):
        requests = {}

        msg = str(message.payload.decode("utf-8"))

        splitted = msg.split(";")
        data = {}

        #print("\n\n\tDevice found: ")

        for dataset in splitted:
            info = dataset.split(",")
            #print("\n\t\t{0} :  {1}".format(info[0],info[1]))
                
            data[info[0]] = info[1]

        requests[data["mac_address"]] = data

        g_requests = requests

    # ------------------------------------------------------------------------------------------------------
    # MQTT message sent

    def on_publish(client,userdata,result):
        #print("data published\n")
        pass

# ------------------------------------------------------------------------------------------------------
# Main loop

    g_requests = {}

    try:
        client = mqtt.Client()
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_publish = on_publish
        client.on_disconnect = on_disconnect


        client.connect(broker,port)
        client.loop_start()

        time.sleep(5)

        client.loop_stop()

        print(g_requests)

        return g_requests

    
    except KeyboardInterrupt:
        client.loop_stop()
        
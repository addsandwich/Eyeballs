"""
MIT License

Copyright (c) 2023 Christopher J. Watson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Purpose:
The VisualCortex module provides a collection of functions for the server section of the eyeballs library.
The main purpose of the server is to collect images from individual eyeballs and make them accessible to any
underlying program as an image frame

Libraries: https://github.com/opencv/opencv

"""

import socket
import pickle
import time
import cv2
import pickle
import struct
import math
import numpy


class Eyeball:
    def __init__(self, config_dict, external_interface_dict):
        self.LOCALHOST = config_dict.get('LOCALHOST', '127.0.0.1')
        self.PORT = config_dict.get('PORT', 9898)
        self.BUFFER_SIZE = config_dict.get('BUFFER_SIZE', 1024*4)
        self.TIME_OUT = config_dict.get('TIME_OUT', 10)
        self.External = external_interface_dict.get('External', '127.0.0.1')

        if self.External == '0.0.0.0':
            self.External = self.LOCALHOST

        #self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.client_socket.connect((self.External, self.PORT))

    def send_data(self, data):
        try:
            serialized_data = pickle.dumps(data)
            self.client_socket.sendall(serialized_data)
        except Exception as e:
            print("Error sending data:", e)

    def receive_response(self):
        try:
            response_data = self.client_socket.recv(self.BUFFER_SIZE)
            if response_data:
                response_message = pickle.loads(response_data)
                print("Received response:", response_message)
        except Exception as e:
            print("Error receiving response:", e)

    def get_video(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Using UDP
        host_ip = '127.0.0.1'
        port = 9999
        max_size = 1024*20
        x_chunks = 1
        y_chunks = 3
        width = 480
        height = 360
        data_size = max_size-struct.calcsize("Q")*2
        try:
            while True:
                # upon successful connection
                vid = cv2.VideoCapture(0)
                while vid.isOpened():
                    ret_f, cap = vid.read()
                    image = cv2.resize(cap, (width, height))
                    #print(image)
                    if ret_f:

                        i = 0
                        buffs = []
                        for x in range(x_chunks):
                            for y in range(y_chunks):
                                x_coord = int(width/x_chunks)
                                y_coord = int(height/y_chunks)
                                x_coord = (x_coord*x, x_coord*(x+1))
                                y_coord = (y_coord*y, y_coord*(y+1))
                                temp = image[y_coord[0]:y_coord[1], x_coord[0]:x_coord[1]]

                                ret_j, buffer = cv2.imencode(".jpg", temp)
                                buffer = buffer.tobytes()
                                # pack the size
                                msg = struct.pack("Q", len(buffer))
                                # pack the index
                                msg = msg + struct.pack("Q", i)
                                msg = msg + buffer
                                # pack the message
                                buffs.append(msg)
                                i = i+1
                        for buff in buffs:
                            client_socket.sendto(buff, (host_ip, port))


        except KeyboardInterrupt:
            pass

    def run(self):
        try:
            #while not msvcrt.kbhit():  # Loop until a key is pressed
            message_to_send = {'command': 'sample_command', 'value': 42}
            self.send_data(message_to_send)
            self.receive_response()  # Receive and process response
            time.sleep(3)
        except KeyboardInterrupt:
            pass
        finally:
            self.client_socket.close()

# Example usage:
if __name__ == "__main__":
    config = {
        'LOCALHOST': '127.0.0.1',
        'PORT': 9898,
        'BUFFER_SIZE': 1024*4,
        'TIME_OUT': 10
    }
    external_interface = {
        'External': '192.168.10.203'  # Change to the desired external interface IP
    }


eyeball = Eyeball(config, external_interface)
#eyeball.run()
eyeball.get_video()

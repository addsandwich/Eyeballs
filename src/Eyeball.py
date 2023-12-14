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
import queue
import socket
import threading
import time
import cv2
import pickle
import struct
import math
from EyeUtils import DataFrameWork as dfw


class Eyeball:
    def __init__(self, config_dict):
        self.LOCALHOST = config_dict.get('LOCALHOST', '127.0.0.1')
        self.PORT = config_dict.get('PORT', 9898)
        self.C2PORT = config_dict.get('C2PORT', 9999)
        self.BUFFER_SIZE = config_dict.get('BUFFER_SIZE', 1024*4)
        self.V_BUFFER_SIZE = config_dict.get('V_BUFFER_SIZE', 1024*32)
        self.TIME_OUT = config_dict.get('TIME_OUT', 10)
        self.EXTERNAL = config_dict.get('EXTERNAL', '127.0.0.1')
        self.IMAGE_QUEUE = config_dict.get('IMAGE_QUEUE', 30)
        self.THREAD_LIMIT = 4
        self.THREAD_COUNT = 0
        self.OUT_QUEUE = queue.Queue(self.IMAGE_QUEUE)
        self.PROCESS_QUEUE = queue.Queue(self.IMAGE_QUEUE)
        self.FULL_STOP = 0
        self.LOCK = threading.Lock()

        if self.EXTERNAL == '0.0.0.0':
            self.EXTERNAL = self.LOCALHOST

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
        x_chunks = 2
        y_chunks = 1
        width = 480
        height = 360
        count_time = 0
        start = time.time()
        ranges = dfw.DataFrameWork.calc_ranges(x_chunks, y_chunks, width, height)

        try:
            while not self.FULL_STOP:
                # upon successful connection
                vid = cv2.VideoCapture(0)
                vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                while vid.isOpened():
                    ret_f, cap = vid.read()
                    #print(cap.shape)
                    image = cv2.resize(cap, (width, height))

                    if ret_f:
                        i = 0

                        for x_coord, y_coord in ranges:
                            temp = cap[y_coord[0]:y_coord[1], x_coord[0]:x_coord[1]]
                            self.process_chunk(client_socket, i, temp)
                            i = i+1

                        if count_time < 10:
                            count_time += 1
                        else:
                            end = time.time()
                            fps = math.trunc(count_time / (end - start))
                            print(fps)
                            count_time = 0
                            start = end

        except KeyboardInterrupt:
            pass

        finally:
            self.FULL_STOP = 1

    def process_chunk(self, client_socket, i, temp):
        ret_j, buffer = cv2.imencode(".jpg", temp)
        buffer = buffer.tobytes()
        # pack the size
        msg = struct.pack("Q", len(buffer))
        # pack the index
        msg = msg + struct.pack("Q", i)
        msg = msg + buffer
        client_socket.sendto(msg, (self.EXTERNAL, self.PORT))

    def run(self):
        try:
            while not self.FULL_STOP:
                message_to_send = {'command': 'sample_command', 'value': 42}
                self.send_data(message_to_send)
                self.receive_response()  # Receive and process response
                time.sleep(3)
        except KeyboardInterrupt:
            pass
        finally:
            self.client_socket.close()



if __name__ == "__main__":
    config = {
        'LOCALHOST': '127.0.0.1',
        'PORT': 9898,
        'BUFFER_SIZE': 1024*4,
        'TIME_OUT': 10
    }
    external_interface = {
        'EXTERNAL': '192.168.0.10'  # Change to the desired external interface IP
    }

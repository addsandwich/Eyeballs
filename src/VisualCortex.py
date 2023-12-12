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
import threading
from queue import Queue
import struct
import time
import math
import cv2
import numpy


class VisualCortex:
    def __init__(self, config_dict):
        self.LOCALHOST = config_dict.get('LOCALHOST', '127.0.0.1')
        self.PORT = config_dict.get('PORT', 9898)
        self.BUFFER_SIZE = config_dict.get('BUFFER_SIZE', 1024)
        self.TIME_OUT = config_dict.get('TIME_OUT', 300)
        self.IMAGE_QUEUE = config_dict.get('IMAGE_QUEUE', 30)
        self.SENSOR_COUNT = config_dict.get('SENSOR_COUNT', 5)
        self.External = config_dict.get('External', '127.0.0.1')

        if self.External == '0.0.0.0':
            self.External = self.LOCALHOST

        self.connections = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.External, self.PORT))
        self.server_socket.listen(self.SENSOR_COUNT)
        self.image_streams = []

    def cmd_loader(self, conn, data):
        try:
            received_data = pickle.loads(data)
            print("Received:", received_data)
            # Example response message
            response_message = {'response': 'Message received successfully'}
            serialized_response = pickle.dumps(response_message)
            conn.sendall(serialized_response)  # Send response back to the client
        except pickle.UnpicklingError as e:
            print("Error unpacking:", e)

    def handle_connection(self, conn):
        try:
            conn.settimeout(self.TIME_OUT)  # Set timeout for receiving data
            while True:
                data = conn.recv(self.BUFFER_SIZE)
                if not data:
                    break  # Exit loop if no data is received
                self.cmd_loader(conn, data)
        except socket.timeout:
            print("Connection timed out.")
        finally:
            conn.close()

    def run(self):
        try:
            while True:
                conn, addr = self.server_socket.accept()
                if len(self.connections) < self.SENSOR_COUNT:
                    thread = threading.Thread(target=self.handle_connection, args=(conn,))
                    thread.start()
                    self.connections.append(thread)
                else:
                    conn.close()
        except KeyboardInterrupt:
            self.close_connections()
            print("Server stopped.")

    def get_video_stream(self):
        # connection info
        host_ip = '127.0.0.1'
        port = 9999
        buffer_size = 1024 * 32
        payload_size = struct.calcsize("Q")  # Size of the payload
        # image info
        x_chunks = 1
        y_chunks = 3
        width = 480
        height = 360
        image = numpy.ones((height, width, 3), dtype=numpy.uint8)
        #stuff
        frame_queue = []
        data = b""
        ranges = self.calc_ranges(x_chunks, y_chunks, width, height)
        # time processing
        count_time = 0
        fps = 0
        start = time.time()

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind((host_ip, port))

        print(f"[LISTENING] Server is listening on {host_ip}:{port}")


        counter = 0
        while True:
            try:
                while len(data) < payload_size:
                    # receiving the packets and appending them into the data
                    packet, addr = server_socket.recvfrom(buffer_size)  # 4k of byte buffer
                    if not packet:
                        break
                    # adding packet to data
                    data += packet
                    # first 8 bytes contain size of packet message
                packed_msg_size = data[:payload_size]
                # rest of data contains video frame
                data = data[payload_size:]
                msg_size = struct.unpack("Q", packed_msg_size)[0]

                while len(data) < msg_size:
                    data += server_socket.recvfrom(buffer_size)

                if msg_size and len(data) >= msg_size:
                    packed_index = data[:payload_size]
                    index_img = struct.unpack("Q", packed_index)[0]
                    data = data[payload_size:]
                    frame_data = data[:msg_size]
                    data = data[msg_size:]
                    frame = numpy.frombuffer(frame_data, dtype=numpy.uint8)
                    frame = frame.reshape(frame.shape[0], 1)
                    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                    #frame = cv2.flip(frame, 1)
                    #print(ranges[index_img])

                    image[ranges[index_img][1][0]:
                          ranges[index_img][1][1], ranges[index_img][0][0]:ranges[index_img][0][1]] = frame
                    #print(frame.dtype)
                    #print(image.dtype)

                    if (count_time < 10):
                        count_time += 1
                    else:
                        end = time.time()
                        fps = math.trunc(count_time / (end - start))
                        count_time = 0
                        start = end
                    cv2.putText(image, f"{fps}", (25, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    cv2.imshow(f"Received {addr}", image)

                    key = cv2.waitKey(1) & 0xFF
                    if key == ord('q'):
                        break

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"[ERROR] {e}")

        cv2.destroyAllWindows()
    def process_video(self):
        pass

    def calc_ranges(self, x_chunks, y_chunks, frame_width, frame_height):
        ranges = []
        for x in range(x_chunks):
            for y in range(y_chunks):
                x_coord = int(frame_width / x_chunks)
                y_coord = int(frame_height / y_chunks)
                x_coord = (x_coord * x, x_coord * (x + 1))
                y_coord = (y_coord * y, y_coord * (y + 1))
                ranges.append([x_coord, y_coord])
        return ranges

    def close_connections(self):
        for thread in self.connections:
            thread.join()
        self.server_socket.close()
        print("All connections closed.")

# Example usage:
if __name__ == "__main__":
    config = {
        'LOCALHOST': '127.0.0.1',
        'PORT': 9898,
        'BUFFER_SIZE': 1024*4,
        'TIME_OUT': 300,
        'SENSOR_COUNT': 3,
        'External': '192.168.10.203'  # Change to '127.0.0.1' or other IP if needed
    }

eyeballs = VisualCortex(config)
#eyeballs.run()
eyeballs.get_video_stream()

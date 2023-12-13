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


class DataFrameWork:
    def __init__(self):
        pass

    @staticmethod
    def calc_ranges(x_chunks, y_chunks, frame_width, frame_height):
        ranges = []
        for x in range(x_chunks):
            for y in range(y_chunks):
                x_coord = int(frame_width / x_chunks)
                y_coord = int(frame_height / y_chunks)
                x_coord = (x_coord * x, x_coord * (x + 1))
                y_coord = (y_coord * y, y_coord * (y + 1))
                ranges.append([x_coord, y_coord])
        return ranges

#!/usr/bin/env python
"""
Visualise maze generation using Matplotlib with WXPython backend.
"""

import threading
import time
from functools import partial
from itertools import chain
from operator import mul

import wx
import numpy
import matplotlib; matplotlib.use('WXAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure

from maze import maze


class GraphFrame(wx.Frame):
    def __init__(self, maze_width=70, maze_height=70, magnification=8):
        wx.Frame.__init__(self, None, -1, 'Maze Generator')
        self.Bind(wx.EVT_CLOSE, self.OnClose, self)

        self.running = False

        self.maze_width = maze_width
        self.maze_height = maze_height
        self.magnification = magnification

        sizer = wx.BoxSizer(wx.VERTICAL)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(hSizer)

        btnStart = wx.Button(self, -1, "Start")
        self.Bind(wx.EVT_BUTTON, self.OnStart, btnStart)
        hSizer.Add(btnStart)

        btnStop = wx.Button(self, -1, "Stop")
        self.Bind(wx.EVT_BUTTON, self.OnStop, btnStop)
        hSizer.Add(btnStop)

        self.fig = Figure()
        self.canvas = FigureCanvasWxAgg(self, -1, self.fig)
        sizer.Add(self.canvas, 1, wx.LEFT|wx.TOP|wx.GROW)

        self.SetSizer(sizer)
        self.SetSize((800, 500))

    def OnClose(self, evt):
        self.running = False
        self.plot_thread.join()
        evt.Skip()

    def OnStart(self, evt):
        self.Plot()

    def OnStop(self, evt):
        self.running = False

    def Plot(self):
        if self.running:
            return

        def thread():
            self.running = True
            for m in maze(self.maze_width, self.maze_height):
                if not self.running:
                    break
                wx.CallAfter(self.plot_data, magnify(m, magnification=self.magnification))
                time.sleep(0.05)
            
        self.plot_thread = threading.Thread(target=thread)
        self.plot_thread.start()

    def plot_data(self, snapshot):
        self.fig.clear()
        self.fig.figimage(snapshot, 0, 0, cmap=plt.cm.binary)
        self.canvas.draw()


def magnify(arr, magnification=2):
    """Magnify and return an int32 numpy array.

    For example::
        >>> a = numpy.array([[1, 2], [2, 3]])
        >>> magnify(a, 2)
            array([[ 1,  1,  2,  2],
                   [ 1,  1,  2,  2],
                   [ 2,  2,  3,  3],
                   [ 2,  2,  3,  3]], dtype=int32)
    """
    # Is there a better way to do this in numpy?
    result = numpy.ndarray(map(partial(mul, magnification), arr.shape), dtype=numpy.int32)
    for r, row in enumerate(arr):
        line = list(chain.from_iterable([c] * magnification for c in row))
        for i in range(magnification):
            result[r * magnification + i] = line
    return result


if __name__ == '__main__':
    app = wx.PySimpleApp(False)
    frame = GraphFrame(maze_width=50, maze_height=50)
    frame.Show()
    app.MainLoop()

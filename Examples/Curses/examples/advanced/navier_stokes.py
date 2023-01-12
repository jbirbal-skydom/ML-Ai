"""
Click to add fluid. `r` to reset.

`cv2` convolutions (`filter2D`) currently don't support boundary wrapping. This is done manually by creating
pressure and momentum arrays with sizes equal to the widget's texture's size plus a 2-width border and
copying data into that border.

This simulates discrete Navier-Stokes with 0 viscosity and a rho of 1. Note that using DIFFUSION kernel instead of
POISSON kernel (for the convolutions that used POISSON) will achieve almost identical results.

An alternative (read: *possibly better*) visualization is to copy the derivative of the pressure array into the
widget's texture instead. This can be approximated by taking the difference of current pressure and previous pressure.
"""
import asyncio

import numpy as np
from cv2 import filter2D

from nurses_2.app import run_widget_as_app
from nurses_2.colors import AColor
from nurses_2.io import MouseButton
from nurses_2.widgets.graphic_widget import GraphicWidget

# Kernels
CONVECTION = np.array([
    [   0, .25,    0],
    [ .25,  -1,  .25],
    [   0, .25,    0],
])
DIFFUSION = np.array([
    [.025,  .1, .025],
    [  .1,  .5,   .1],
    [.025,  .1, .025],
])
POISSON = np.array([
    [   0, .25,    0],
    [ .25,   0,  .25],
    [   0, .25,    0],
])

WATER_COLOR = AColor.from_hex("1259FF")

def wrap_border(array):
    array[:2] = array[-4: -2][::-1]
    array[-2:] = array[2: 4][::-1]
    array[2: -2, :2] = array[2: -2, -4: -2][::-1]
    array[2: -2, -2:] = array[2: -2, 2: 4][::-1]

def sigmoid(array):
    return 1 / (1 + np.e**-array)


class Fluid(GraphicWidget):
    def on_add(self):
        super().on_add()
        self.on_size()
        self._update_task = asyncio.create_task(self._update())

    def on_remove(self):
        super().on_remove()
        self._update_task.cancel()

    def on_size(self):
        h, w = self._size

        size_with_border = 2 * h + 4, w + 4

        self.texture = np.zeros((2 * h, w, 4), dtype=int)
        self.pressure = np.zeros(size_with_border, dtype=float)
        self.momentum = np.zeros(size_with_border, dtype=float)

    def on_mouse(self, mouse_event):
        if not self.collides_point(mouse_event.position):
            return False

        if mouse_event.button is not MouseButton.NO_BUTTON:
            y, x = self.to_local(mouse_event.position)

            Y = 2 * y + 2

            self.pressure[Y: Y + 2, x + 2: x + 4] += 2.0

            return True

    def on_key(self, key_event):
        match key_event.key:
            case "r" | "R":
                self.on_size()  # Reset
                return True

    async def _update(self):
        while True:
            pressure = self.pressure
            momentum = self.momentum

            wrap_border(momentum)
            wrap_border(pressure)

            self.momentum = filter2D(momentum, -1, DIFFUSION) + filter2D(pressure, -1, CONVECTION)

            delta = filter2D(self.momentum, -1, POISSON)

            self.pressure = filter2D(pressure, -1, POISSON) + .5 * (delta - delta**2)

            # Note the alpha channel is affected by `pressure` as well.
            self.texture[:] = (sigmoid(self.pressure[2: -2, 2: -2, None]) * WATER_COLOR).astype(int)

            await asyncio.sleep(0)


run_widget_as_app(Fluid(size_hint=(1.0, 1.0)))

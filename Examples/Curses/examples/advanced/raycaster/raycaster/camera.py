import asyncio

import numpy as np

def rotation_matrix(theta):
    """
    Returns a 2-dimensional rotation array of a given angle.

    Notes
    -----
    Matrix multiplication of a rotation matrix with a camera's plane will
    rotate the plane.
    """
    x = np.cos(theta)
    y = np.sin(theta)

    return np.array(
        [
            [ x, y],
            [-y, x],
        ],
        dtype=float,
    )


class Camera:
    FIELD_OF_VIEW = .66
    FRAMES = 20

    INITIAL_PLANE = np.array(
        [
            [1.001, 0.001],
            [0.0, FIELD_OF_VIEW],
        ],
        dtype=float,
    )

    pos = np.array([2.5, 2.5], dtype=float)

    def __init__(self):
        self.plane = self.INITIAL_PLANE.copy()
        self._camera_task = asyncio.create_task(self._move_camera())

    def turn(self, angle):
        np.dot(self.INITIAL_PLANE, rotation_matrix(angle), out=self.plane)

    async def rotate(self, start, end):
        if end > start:
            end -= 2 * np.pi

        for theta in np.linspace(start, end, self.FRAMES):
            self.turn(theta)
            await asyncio.sleep(0)

    async def move(self, start, end):
        for position in np.linspace(start, end, self.FRAMES):
            self.pos = position
            await asyncio.sleep(0)

    async def _move_camera(self):
        NW = 2.5, 2.5
        NE = 2.5, 7.5
        SE = 7.5, 7.5
        SW = 7.5, 2.5
        NORTH = np.pi
        EAST = np.pi / 2
        SOUTH = 0
        WEST = 3 * np.pi / 2

        while True:
            await self.rotate(NORTH, EAST)
            await self.move(NW, NE)

            await self.rotate(EAST, SOUTH)
            await self.move(NE, SE)

            await self.rotate(SOUTH, WEST)
            await self.move(SE, SW)

            await self.rotate(WEST, NORTH)
            await self.move(SW, NW)

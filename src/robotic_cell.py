from typing import List
from .robot import Robot

import asyncio


class RoboticCell:
    def __init__(self, assembly, *constrains):
        self.robots: List[Robot] = [Robot(assembly.get_components()[index], constrains[index])
                                    for index in range(len(constrains))]

    def drive(self, targets: List[List[float]], speed: float):
        max_drive_time = max(rbt.get_max_drive_time(tar, speed) for rbt, tar in zip(self.robots, targets))
        ranges = [max(rbt.get_ranges(tar)) for rbt, tar in zip(self.robots, targets)]
        speeds = [rng / max_drive_time for rng in ranges]

        async def async_drive():
            tasks = [rbt.drive(tar, sp) for rbt, tar, sp in zip(self.robots, targets, speeds)]
            await asyncio.gather(*tasks)

        asyncio.run(async_drive())

    def set_random_position(self, speed: float = 8.0):
        targets = [rbt.get_random_positions() for rbt in self.robots]
        self.drive(targets, speed)

    def launch(self):
        for rbt in self.robots:
            rbt.launch()

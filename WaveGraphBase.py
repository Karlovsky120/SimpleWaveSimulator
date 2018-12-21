import matplotlib.gridspec as gridspec
import numpy as np

from abc import ABC, abstractmethod
from matplotlib import animation
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, CheckButtons

PI = np.pi


class WaveGraphBase(ABC):
    def __init__(self, name, granularity, x_range, x_offset, y_range, y_offset, time_factor, waves, slider_data, checkbox_data):
        self.granularity = granularity
        self.x_range = x_range
        self.x_offset = x_offset
        self.y_range = y_range
        self.y_offset = y_offset
        self.waves = waves
        self.slider_data = slider_data
        self.checkbox_data = checkbox_data
        self.time_factor = time_factor
        self.checkboxes_ticked = [True] * len(self.waves)

        self.fig = plt.figure(figsize=(16, 9))
        self.fig.canvas.set_window_title(name)

        self.main_grid = gridspec.GridSpec(2, 1)
        self.graph_cell = plt.subplot(self.main_grid[0, :])
        self.graph_cell.set(xlim=(-self.x_range - self.x_offset, self.x_range - self.x_offset),
                            ylim=(-self.y_range - self.y_offset, self.y_range - self.y_offset))

        self.x_data = np.linspace(-3*self.x_range - 3*self.x_offset, 3*self.x_range - 3*self.x_offset, self.granularity)
        self.y_data = [[]] * len(self.waves)

        self.lines = [plt.plot([], [])[0] for _ in range(len(self.waves))]
        self.patches = self.lines

        self.control_cell = self.main_grid[1, :]
        self.control_grid = gridspec.GridSpecFromSubplotSpec(1, 7, self.control_cell)

        self.checkbox_cell = self.control_grid[0, 0]
        self.checkbox_grid = gridspec.GridSpecFromSubplotSpec(1, 1, self.checkbox_cell)
        self.checkboxes = []
        self.checkboxAx = plt.subplot(self.checkbox_grid[0, 0:1])
        self.checkbox = CheckButtons(self.checkboxAx, tuple(x["name"] for x in self.checkbox_data),
                                     tuple(x["init"] for x in self.checkbox_data))
        self.checkbox.on_clicked(self.update)

        self.slider_cell = self.control_grid[0, 2:6]
        self.slider_grid = gridspec.GridSpecFromSubplotSpec(len(self.slider_data), 1, self.slider_cell)
        self.sliders = []
        for i in range(0, len(self.slider_data)):
            self.sliderAx = plt.subplot(self.slider_grid[i, 0])
            self.slider = Slider(self.sliderAx, self.slider_data[i]["name"], self.slider_data[i]["min"],
                                 self.slider_data[i]["max"], valinit=self.slider_data[i]["init"],
                                 valstep=self.slider_data[i]["step"])
            self.sliders.append(self.slider)
        for slider in self.sliders:
            slider.on_changed(self.update)

    def init(self):
        for line in self.lines:
            line.set_data([], [])
        return self.patches

    def start(self):
        self.animation = animation.FuncAnimation(self.fig, self.animate, init_func=self.init, frames=999999, repeat=True, interval=20, blit=True)
        plt.show()

    @abstractmethod
    def update(self, event=None):
        """Register sliders and checkboxes"""

    @abstractmethod
    def animate(self, i):
        """Animation function"""

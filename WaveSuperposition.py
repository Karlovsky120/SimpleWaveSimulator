import numpy as np

from Wave import Wave
from WaveGraphBase import WaveGraphBase

PI = np.pi

sliderDataList = [{'name': 'Left amplitude', 'min': 0, 'max': 8.0, 'init': 2, 'step': 0.01},
                  {'name': 'Right amplitude', 'min': 0, 'max': 8.0, 'init': 2, 'step': 0.01},
                  {'name': 'Left period', 'min': 0.01, 'max': 8 * PI, 'init': 2 * PI, 'step': 0.01},
                  {'name': 'Right period', 'min': 0.01, 'max': 8 * PI, 'init': 2 * PI, 'step': 0.01},
                  {'name': 'Wire tension', 'min': 0.01, 'max': 8.0, 'init': 1, 'step': 0.01},
                  {'name': 'Wire mass density', 'min': 0.01, 'max': 8.0, 'init': 1, 'step': 0.01},
                  {'name': 'Simulation speed', 'min': 0.001, 'max': 2.0, 'init': 0.1, 'step': 0.001}]

checkboxDataList = [{'name': 'Left wave', 'init': True},
                    {'name': 'Right wave', 'init': True},
                    {'name': 'Sum wave', 'init': True}]
                   #{'name': 'Impulse only', 'init': False}]

waveList = [Wave(amplitude=2, period=2*PI, direction=1),
            Wave(amplitude=2, period=2*PI, direction=-1),
            None]


class WaveSuperposition(WaveGraphBase):
    def __init__(self, granularity=1024, x_range=4 * PI, x_offset=0, y_range=6, y_offset=0, time_factor=0.1, waves=[], slider_data=[], checkbox_data=[]):
        super().__init__(granularity, x_range, x_offset, y_range, y_offset, time_factor, waves, slider_data, checkbox_data)
        self.checkboxes_ticked = self.checkbox.get_status()

    def update(self, event=None):
        self.waves[0].amplitude = self.sliders[0].val
        self.waves[1].amplitude = self.sliders[1].val
        self.waves[0].period = self.sliders[2].val
        self.waves[1].period = self.sliders[3].val
        self.waves[0].tension = self.sliders[4].val
        self.waves[1].tension = self.sliders[4].val
        self.waves[0].mass_density = self.sliders[5].val
        self.waves[1].mass_density = self.sliders[5].val
        self.time_factor = self.sliders[6].val
        self.checkboxes_ticked = self.checkbox.get_status()
        #self.waves[0].show_full_wave = not self.checkboxes_ticked[3]
        #self.waves[1].show_full_wave = not self.checkboxes_ticked[3]

    def animate(self, i):
        self.y_data[0] = self.waves[0].get_y_array(i * self.time_factor, self.x_data, dynamic_show=[-self.x_range - self.waves[0].get_length() / 2, -self.x_range])
        self.y_data[1] = self.waves[1].get_y_array(i * self.time_factor, self.x_data, dynamic_show=[self.x_range, self.x_range + self.waves[1].get_length() / 2])
        self.y_data[2] = [x + y for x, y in zip(self.y_data[0], self.y_data[1])]

        if not self.checkboxes_ticked[0]:
            self.y_data[0] = [0] * self.granularity
        if not self.checkboxes_ticked[1]:
            self.y_data[1] = [0] * self.granularity
        if not self.checkboxes_ticked[2]:
            self.y_data[2] = [0] * self.granularity

        self.lines[0].set_data(self.x_data, self.y_data[0])
        self.lines[1].set_data(self.x_data, self.y_data[1])
        self.lines[2].set_data(self.x_data, self.y_data[2])

        return self.patches


graph = WaveSuperposition(waves=waveList, slider_data=sliderDataList, checkbox_data=checkboxDataList)
graph.start()


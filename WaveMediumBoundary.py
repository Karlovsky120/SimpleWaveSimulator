import numpy as np
from matplotlib import pyplot as plt

from Wave import Wave
from WaveGraphBase import WaveGraphBase

PI = np.pi

sliderDataList = [{'name': 'Source amplitude', 'min': 0.1, 'max': 8.0, 'init': 2, 'step': 0.01},
                  {'name': 'Source period', 'min': 0.1, 'max': 8 * PI, 'init': 2 * PI, 'step': 0.01},
                  {'name': 'Left tension', 'min': 0.1, 'max': 8.0, 'init': 1, 'step': 0.01},
                  {'name': 'Right tension', 'min': 0.1, 'max': 8.0, 'init': 2, 'step': 0.01},
                  {'name': 'Left mass density', 'min': 0.1, 'max': 8.0, 'init': 1, 'step': 0.01},
                  {'name': 'Right mass density', 'min': 0.1, 'max': 8.0, 'init': 0.5, 'step': 0.01},
                  {'name': 'Simulation speed', 'min': 0.001, 'max': 2.0, 'init': 0.1, 'step': 0.001},
                  {'name': 'Line thickness', 'min': 1, 'max': 10, 'init': 5, 'step': 0.1}]

checkboxDataList = [{'name': 'Source wave', 'init': True},
                    {'name': 'Reflected wave', 'init': True},
                    {'name': 'Transmitted wave', 'init': True},
                    {'name': 'Source + reflected', 'init': False}]

waveList = [Wave(amplitude=2, period=2*PI, direction=1),
            None,
            None,
            None]


class WavesChangingMedium(WaveGraphBase):
    def __init__(self, name='Waves medium boundary', granularity=512, x_range=4 * PI, x_offset=0, y_range=6, y_offset=0, time_factor=0.1, line_thickness=5, waves=[], slider_data=[], checkbox_data=[], tension=2, mass_density=0.5):
        super().__init__(name, granularity, x_range, x_offset, y_range, y_offset, time_factor, line_thickness, waves, slider_data, checkbox_data)
        self.tension = tension
        self.mass_density = mass_density
        self.checkboxes_ticked = self.checkbox.get_status()

    def update(self, event=None):
        self.waves[0].amplitude = self.sliders[0].val
        self.waves[0].period = self.sliders[1].val
        self.waves[0].tension = self.sliders[2].val
        self.tension = self.sliders[3].val
        self.waves[0].mass_density = self.sliders[4].val
        self.mass_density = self.sliders[5].val
        self.time_factor = self.sliders[6].val
        self.line_thickness = self.sliders[7].val
        self.checkboxes_ticked = self.checkbox.get_status()

    def animate(self, i):
        self.waves[1] = self.waves[0].get_reflected_wave(self.tension, self.mass_density)
        self.waves[2] = self.waves[0].get_transmitted_wave(self.tension, self.mass_density)

        self.y_data[0] = self.waves[0].get_y_array(i * self.time_factor, self.x_data,
                                                   static_show=[-self.x_range, 0],
                                                   dynamic_show=[0, self.waves[0].get_length() / 2],
                                                   dynamic_offset=-(int(self.x_range/self.waves[0].get_length())+1)*
                                                                  self.waves[0].get_length())
        self.y_data[1] = self.waves[1].get_y_array(i * self.time_factor, self.x_data,
                                                   static_show=[-self.x_range, 0],
                                                   dynamic_show=[-self.waves[1].get_length() / 2, 0],
                                                   dynamic_offset=(int(self.x_range/self.waves[1].get_length())+1)*
                                                                  self.waves[1].get_length())
        self.y_data[2] = self.waves[2].get_y_array(i * self.time_factor, self.x_data,
                                                   static_show=[0, self.x_range],
                                                   dynamic_show=[0, self.waves[2].get_length() / 2],
                                                   dynamic_offset=-(int(self.x_range/self.waves[0].get_length())+1)*
                                                                  self.waves[0].get_length()*
                                                                  self.waves[0].get_velocity()/self.waves[2].get_velocity())
        self.y_data[3] = [x + y for x, y in zip(self.y_data[0], self.y_data[1])]

        for j in range(len(self.y_data)):
            if not self.checkboxes_ticked[j]:
                plt.setp(self.lines[j], linewidth=0)
            else:
                plt.setp(self.lines[j], linewidth=self.line_thickness)

            self.lines[j].set_data(self.x_data, self.y_data[j])

        return self.patches


graph = WavesChangingMedium(waves=waveList, slider_data=sliderDataList, checkbox_data=checkboxDataList)
graph.start()

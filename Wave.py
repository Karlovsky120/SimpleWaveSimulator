import math
import numpy as np


class Wave:
    def __init__(self, amplitude=1, period=2 * np.pi, direction=1, mass_density=1, tension=1, show_full_wave=True):
        self.amplitude = amplitude
        self.period = period
        self.direction = direction
        self.mass_density = mass_density
        self.tension = tension
        self.show_full_wave = show_full_wave

    def get_velocity(self):
        return math.sqrt(self.tension/self.mass_density)

    @staticmethod
    def calculate_velocity(tension, mass_density):
        return math.sqrt(tension/mass_density)

    def get_length(self):
        return self.get_velocity() * self.period

    def get_omega(self):
        return 2 * np.pi / self.period

    def get_y_array_plain(self, time, x_array):
        return [self.amplitude * np.sin(self.get_omega() * (time - self.direction * x / self.get_velocity())) for x in x_array]

    def get_y_array(self, time, x_array, static_show=[-99999, 99999]):
        y_array = []
        velocity = self.get_velocity()
        omega = self.get_omega()
        for x in x_array:
            if x < static_show[0] or x > static_show[1]:
                y_array.append(np.nan)
            else:
                y_array.append(self.amplitude * np.sin(omega * (time - self.direction * x / velocity)))
        return y_array

    def get_reflected_wave(self, tension=1, mass_density=1):
        source_velocity = self.get_velocity()
        transmitted_velocity = self.calculate_velocity(tension, mass_density)
        reflected_amplitude = self.amplitude * (transmitted_velocity - source_velocity) / (
                source_velocity + transmitted_velocity)
        return Wave(reflected_amplitude, self.period, -self.direction, self.tension, self.mass_density)

    def get_transmitted_wave(self, tension=1, mass_density=1):
        transmitted_velocity = self.calculate_velocity(tension, mass_density)
        transmitted_amplitude = self.amplitude * 2 * transmitted_velocity / (self.get_velocity() + transmitted_velocity)
        return Wave(transmitted_amplitude, self.period, self.direction, tension, mass_density)

class Process:
    def __init__(self, young_modulus, poisson_ratio, density, thermal_conductivity, viscosity,
                 permittivity, sheet_resisitance, **kwargs):
        self.E = young_modulus
        self.v = poisson_ratio
        self.rho = density
        self.K = thermal_conductivity
        self.mu = viscosity
        self.eps = permittivity
        self.Rs = sheet_resisitance
        self.__dict__.update(kwargs)  # used for additional variables not included above


class Layer(Process):
    def __init__(self, process, h, **kwargs):
        super().__init__(**process.__dict__, **kwargs)
        self.h = h

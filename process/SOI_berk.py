from process import Process, Layer


class SOI_berk:
    def __init__(self):
        poly = Process(young_modulus=169e9,  # [N/m^2]
                       poisson_ratio=0.3,  # []
                       density=2300,  # [kg/m^3]
                       thermal_conductivity=2.33e-6,  # [/C]
                       viscosity=1.78e-5,  # []
                       permittivity=8.854e-12,  # [C^2/(uN.um^2)] = [(C.s)^2/kg.um^3]
                       sheet_resisitance=20  # Poly-Si sheet resistance [ohm/square]
                       )
        self.p1 = Layer(poly, h=40e-6, fluid_gap=2e-6)
        self.ox = Layer(poly, h=2e-6)
        self.p2 = Layer(poly, h=550e-6)

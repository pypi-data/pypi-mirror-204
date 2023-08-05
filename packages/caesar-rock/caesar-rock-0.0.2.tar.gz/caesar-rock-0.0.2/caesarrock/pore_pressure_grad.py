import numpy as np

class Eaton:
    def __init__ (self, df, seabed_depth, unconsolidated_density, pre_data_rock_density, data_depth, normal_pore_pressure_gradient):
        self.df = df
        self.seabed_depth = seabed_depth
        self.unconsolidated_density = unconsolidated_density
        self.pre_data_rock_density = pre_data_rock_density
        self.data_depth = data_depth
        self.normal_pore_pressure_gradient = normal_pore_pressure_gradient

        self.calcule_sigma_ov()
        self.calcule_gov()
        self.calcule_coeff()
        self.calcule_pore_pressure_grad()

    def calcule_sigma_ov(self):
        sigma_ov_init = 1.02 * self.seabed_depth + self.unconsolidated_density * 50 + self.pre_data_rock_density * (self.data_depth - (self.seabed_depth + 50))
    
        aux = 0
        for j in range(1, len(self.df)):
            aux = aux + self.df.iloc[j-1, 1] * (self.df.iloc[j, 0] - self.df.iloc[j-1, 0])

        self.sigma_ov = 1.422 * (sigma_ov_init + aux)
    
    def calcule_gov(self):
        self.df['Gov'] = self.df.apply(lambda row: self.sigma_ov / (0.1704 * row.iloc[0]), axis=1) # lb/gal
    
    def calcule_coeff(self):
        self.coeff = np.polyfit(self.df.iloc[:, 0], self.df.iloc[:, 2], 1)
    
    def calcule_pore_pressure_row(self, depth, delta_tc, gov):
        y = self.coeff[0] * depth + self.coeff[1]
        return gov - (gov - self.normal_pore_pressure_gradient) * (y / delta_tc) ** 1.2
    
    def calcule_pore_pressure_grad(self):
        self.df['Pore Pressure Grad. (Eaton) - ppg'] = self.df.apply(lambda row: self.calcule_pore_pressure_row(row[0], row[2], row[3]), axis=1)
        self.df = self.df.drop(columns=self.df.columns[3], axis=1)
    
    
class Zamora:
    def __init__ (self, df, normal_pore_pressure_gradient):
        self.df = df
        self.normal_pore_pressure_gradient = normal_pore_pressure_gradient

        self.calcule_coeff()
        self.calcule_pore_pressure_grad()
    
    def calcule_coeff(self):
        self.coeff = np.polyfit(self.df.iloc[:, 0], self.df.iloc[:, 1], 1)
    
    def calcule_pore_pressure_grad_row(self, depth, corrected_drilling_exponent):
        y = self.coeff[0] * depth + self.coeff[1]
        return self.normal_pore_pressure_gradient * (y / corrected_drilling_exponent)

    def calcule_pore_pressure_grad(self):
        self.df['Pore Pressure Grad. (Zamora) - ppg'] = self.df.apply(lambda row: self.calcule_pore_pressure_grad_row(row[0], row[1]), axis=1)
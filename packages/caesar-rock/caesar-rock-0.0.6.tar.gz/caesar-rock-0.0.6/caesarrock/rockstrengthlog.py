import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import matplotlib.colors as mcolors
import sympy as sym
import math
from enum import Enum
import numpy as np

class Data(Enum):
    POROSITY = 'porosity'
    DELTA_TC = 'delta_tc'

class Lit(Enum):
    CLAYSTONE = 'claystone'
    LIMESTONE = 'limestone'
    MARL = 'marl'
    SANDSTONE = 'sandstone'
    SILTSTONE = 'siltstone'

class RockStrengthLog:
    def __init__(self, df, variable, shale_list=None, shale_equation=None, limestone_list=None, limestone_equation=None, \
                 sandstone_list=None, sandstone_equation=None):
        self.df = df
        self.variable = variable
        self.shale_list = [item.value if isinstance(item, Enum) else item for item in shale_list]
        self.limestone_list = [item.value if isinstance(item, Enum) else item for item in limestone_list]
        self.sandstone_list = [item.value if isinstance(item, Enum) else item for item in sandstone_list]
        self.shale_equation = shale_equation
        self.limestone_equation = limestone_equation
        self.sandstone_equation = sandstone_equation
        self.rows_obj = []
        
        self.add_row_obj()
        self.get_result_df()
    
    def add_row_obj (self):
        for i, lithology in self.df.iloc[:, 1].iteritems():
            equation = self.id_lit(lithology.split('-')[0].lower())
            porosity = self.df.iloc[i, 4] if self.variable == Data.POROSITY else None
            delta_tc = self.df.iloc[i, 4] if self.variable == Data.DELTA_TC else None

            row_obj = RockCompressiveStrength(depth = self.df.iloc[i, 0],  
                                              ecd = self.df.iloc[i, 2], 
                                              pore_pressure_grad = self.df.iloc[i, 3],
                                              delta_tc = delta_tc,
                                              porosity = porosity,
                                              equation = equation,
                                              variable = self.variable)
            
            self.rows_obj.append(row_obj)
    
    def id_lit(self, main_lit):
        if main_lit in self.shale_list:
            equation = self.shale_equation
        elif main_lit in self.limestone_list:
            equation = self.limestone_equation
        elif main_lit in self.sandstone_list:
            equation = self.sandstone_equation
        else:
            assert False, 'The lithology is not included in any list.'
        
        return equation
        
    def get_result_df(self):
        list_aux = []

        for obj in self.rows_obj:
            dict_obj = {}
            dict_obj['Angle of internal friction - deg'] = obj.angle
            dict_obj['UCS - MPa'] = obj.ucs
            dict_obj['CCS - MPa'] = obj.ccs
            list_aux.append(dict_obj)

        df_calc = pd.DataFrame(list_aux)

        self.result_df = pd.concat([self.df, df_calc], axis=1)
        self.df = self.result_df
 
    def plot(self):
        fig, axs = plt.subplots(1, 5, figsize=(14, 8))

        axs[0].set_title('Lithology')
        axs[0].set_xticks([])
        axs[0].invert_yaxis()

        dd = self.df.drop_duplicates(subset=self.df.columns[1], keep="first").iloc[:, 1].to_list()
        d2 = dict(zip(dd, np.arange(0,len(dd))))

        cmap = plt.get_cmap('Oranges')
        colors = cmap(np.linspace(0, 1, len(dd)))
        axs[0].pcolormesh([0, 1], self.df.iloc[:, 0], self.df.iloc[:-1, 1].map(d2).to_numpy().reshape(-1, 1), \
                  cmap=cmap, vmin=0, vmax=len(colors)-1)
        axs[0].set_xticks([])
        hands = [Patch(color=col, label=k) for k, col in zip(d2, colors)]
        axs[0].legend(handles=hands, loc='upper right', bbox_to_anchor=(-0.3, 1), fontsize=10, facecolor='lightgrey')
        plt.gca().invert_yaxis()

        axs[1].plot(self.df['UCS - MPa'], self.df.iloc[:, 0], color='orange', label='UCS')
        axs[1].plot(self.df['CCS - MPa'], self.df.iloc[:, 0], color='blue', label = 'CCS')
        axs[1].set_title('UCS and CCS (MPa)')
        axs[1].set_yticks([])
        axs[1].invert_yaxis()
        axs[1].legend(loc='upper right', fontsize=10)

        axs[2].plot(self.df['Angle of internal friction - deg'], self.df.iloc[:, 0], color='red')
        axs[2].set_title('φ (deg)')
        axs[2].set_yticks([])
        axs[2].invert_yaxis()

        title3 = 'Porosity (fr)' if self.variable == Data.POROSITY else 'Δtc (µs/ft)'

        axs[3].plot(self.df.iloc[:, 4], self.df.iloc[:, 0])
        axs[3].set_title(title3)
        axs[3].set_yticks([])
        axs[3].invert_yaxis()

        axs[4].plot(self.df.iloc[:, 2], self.df.iloc[:, 0], color='magenta', label='ECD')
        axs[4].invert_yaxis()
        axs[4].plot(self.df.iloc[:, 3], self.df.iloc[:, 0], color='green', label = 'Grad. PP.')
        axs[4].set_title('ECD and Grad. PP. (ppg)')
        axs[4].set_yticks([])
        axs[4].invert_yaxis()
        axs[4].legend(loc='upper right', fontsize=10)
        
        fig.tight_layout()
        plt.show()
    
class RockCompressiveStrength:
    def __init__(self, depth, ecd, pore_pressure_grad, delta_tc, porosity, equation, variable):
        self.depth = depth
        self.ecd = ecd                                      
        self.pore_pressure_grad = pore_pressure_grad        
        self.delta_tc = delta_tc
        self.porosity = porosity
        self.equation = equation
        self.variable = variable

        self.calcule_dp()
        self.calcule_ucs()
        self.calcule_friction_angle()
        self.calcule_ccs()  

    def calcule_dp(self):
        self.dp = (self.ecd - self.pore_pressure_grad) * self.depth * 119.8 * 9.81 * 10 ** (-6)     # ppg to MPa
    
    def calcule_ucs(self):
        self.ucs = self.equation(self.delta_tc) if self.variable == Data.DELTA_TC else self.equation(self.porosity)
    
    def calcule_friction_angle(self):
        phi = sym.Symbol('phi')
        tau = -0.41713 + 0.28907 * self.ucs - 0.00051878 * (self.ucs ** 2)
        eq = (self.ucs / tau) - (2 * sym.cos(phi)) / (1 - sym.sin(phi))
        self.angle = math.degrees(sym.solve(eq, phi)[0])    
    
    def calcule_ccs(self):
        self.ccs = self.ucs + self.dp + 2 * self.dp * \
            math.sin(math.radians(self.angle)) / (1 - math.sin(math.radians(self.angle)))
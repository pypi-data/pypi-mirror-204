from pdengine.Model import Model
import control
import numbers

class WoodBerryModel(Model):
    def __init__(self):
        name = "Wood-Berry Distillation"

        # make explicit which inputs are MVs and which ones are FFs
        inputs  = {'MV': ['R', 'S'], 
                   'FF': ['F']}
        outputs = ['x_D', 'x_B']
                
        SS_vals = {'R': 1.95,
                   'S': 1.71, 
                   'F': 2.45, 
                   'x_D': 96.25,
                   'x_B': 0.50} # R, S, F in lb/min, x_D, x_B in mol %
        
        typ_movs = {'R': 0.01,
                    'S': 0.01,
                    'F': 0.01}
        
        validity_lims = {'R': (0.5,3), 
                         'S': (0.5,3), 
                         'F': (0.5,3), 
                         'x_D': (0, 100),
                         'x_B': (0, 100)} # R, S, F in lb/min, x_D, x_B in mol %        
        
        noise_lvls = {'R': 0.05, 'S': 0.05, 'F': 0, 'x_D': 0.25, 'x_B': 0.25}
        
        # Wood-Berry
        g_tf = control.tf([12.8], [16.7,1])
        (num_pade, den_pade) = control.pade(1,1)
        g_delay = control.tf(num_pade, den_pade)
        g11 = g_tf*g_delay

        g_tf = control.tf([-18.9], [21.0,1])
        (num_pade, den_pade) = control.pade(3,1)
        g_delay = control.tf(num_pade, den_pade)
        g12 = g_tf*g_delay

        g_tf = control.tf([6.6], [10.9,1])
        (num_pade, den_pade) = control.pade(7,1)
        g_delay = control.tf(num_pade, den_pade)
        g21 = g_tf*g_delay

        g_tf = control.tf([-19.4], [14.4,1])
        (num_pade, den_pade) = control.pade(3,1)
        g_delay = control.tf(num_pade, den_pade)
        g22 = g_tf*g_delay

        g_tf = control.tf([3.8], [14.9,1])
        (num_pade, den_pade) = control.pade(8,1)
        g_delay = control.tf(num_pade, den_pade)
        g1f = g_tf*g_delay

        g_tf = control.tf([4.9], [13.2,1])
        (num_pade, den_pade) = control.pade(3,1)
        g_delay = control.tf(num_pade, den_pade)
        g2f = g_tf*g_delay

        row_1_num = [x[0][0] for x in (g11.num, g12.num, g1f.num)]
        row_2_num = [x[0][0] for x in (g21.num, g22.num, g2f.num)]

        row_1_den = [x[0][0] for x in (g11.den, g12.den, g1f.den)]
        row_2_den = [x[0][0] for x in (g21.den, g22.den, g2f.den)]

        sys = control.tf(
                    [row_1_num,row_2_num],
                    [row_1_den,row_2_den])
        
        super().__init__(name, inputs, outputs, sys, SS_vals, typ_movs, validity_lims, noise_lvls)
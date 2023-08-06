from pdengine.Model import Model
import control
import numbers

class ValveModel(Model):
    # Simple Valve Model
    # Input = %CO, Output = Flow in GPM
    # K = Gain in gpm/%CO, tau = time constant of valve actuator in s
    # Assumes dP across valve is constant or just a function of flow. 
    # See Smith and Corripio Textbook Figure 5-2.8.

    def __init__(self):
        name = "Simple Control Valve"

        # make explicit which inputs are MVs and which ones are FFs
        inputs  = {'MV': ['CO'], 
                   'FF': []}
        outputs = ['F']
                
        SS_vals = {'CO': 0.5,
                   'F': 5} # CO in %CO, F flow in GPM
        
        typ_movs = {'CO': 0.01}
        
        validity_lims = {'CO': (0,1), 
                         'F': (0,10)
                         }
        
        noise_lvls = {'CO': 0.001, 'F': 0.1}
        
        # Wood-Berry
        g_tf = control.tf([-10], [7,1])
        (num_pade, den_pade) = control.pade(5,1)
        g_delay = control.tf(num_pade, den_pade)
        g11 = g_tf*g_delay
        sys = control.tf(g11)
        
        super().__init__(name, inputs, outputs, sys, SS_vals, typ_movs, validity_lims, noise_lvls)

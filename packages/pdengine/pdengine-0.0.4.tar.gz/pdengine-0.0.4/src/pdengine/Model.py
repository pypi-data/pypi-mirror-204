import control
import numpy as np
import numbers
from abc import ABC, abstractmethod
from noise import pnoise1
from random import uniform

class Model(ABC):
    # A PDEngine Model parent class that all child classes will inherit from to define a model
    # A model must be of type control.TransferFunction
    
    @abstractmethod
    def __init__(self, name: str, inputs: dict, outputs, sys, SS_vals, typ_movs, validity_lims, noise_lvls):
        self.name = name
        self.inputs = inputs
        self.outputs = outputs

        # check for input/output validity
        self.nMVs = len(inputs['MV'])
        self.nFFs = len(inputs['FF'])
        self.ninputs = self.nMVs + self.nFFs
        self.noutputs = len(outputs)

        N = self.ninputs + self.noutputs
        
        if (N != len(SS_vals)):
            raise ValueError(f"Dict of steady-state values must have {N} signals but given {len(SS_vals)}.")
            
        if (N != len(validity_lims)):
            raise ValueError(f"Dict of validity limits must have {N} signals but given {len(validity_lims)}.")            

        if (self.ninputs != len(typ_movs)):
            raise ValueError(f"Dict of typical move values must have {self.ninputs} signals but given {len(typ_movs)}.")
            
        self.system = sys
        self.SS_vals = SS_vals
        self.typ_movs = typ_movs
        self.validity_lims = validity_lims

        # noise settings
        self.noise_lvls = noise_lvls

        # initial values calculated based on span
        self.initial_COs = {}
        for key in inputs['MV']:
            self.initial_COs[key] = self.get_percentspan(key, self.SS_vals[key])

    def get_percentspan(self, key, pv):
        """
        Calculate the change in PV in terms of % based on
        the validity limits
        """
        ll = self.validity_lims[key][0]
        ul = self.validity_lims[key][1]
        span = ul-ll
        pspan = (pv-ll)/span # percent span
        return pspan
        
    def create_system(self, dt=0.02):
        # https://python-patterns.guide/gang-of-four/abstract-factory/
        # I find a function name easier to read when it tells me what the 
        # function does instead of telling me what kind of function it is
        g = self._init_generator(dt=dt)
        g.send(None)
        
        print(f"=============================================\nSystem Created: {self.name}\n=============================================")
        print(self.system)
        
        return g
                
    def _init_generator(self, dt):
        """
        Returns a Python generator function for control.LinearIOSystem()

        Parameters
        ----------
        sys: A LinearIOSystem() system
        dt:  The time step for stepping the system. Must be small enough to be stable.

        Outputs
        ----------             
        A Python generator for the IOSystem that takes in a set of system
        inputs, U and responds with system outputs, Y
        """

        # must use IOSystem for input_output_response()
        sys = control.LinearIOSystem(self.system, 
                name = self.name, 
                inputs = self.inputs['MV'] + self.inputs['FF'], 
                outputs = self.outputs)

        # time step grid size?
        T_start = 0
        T_end   = dt
        N       = 2 # 2 time steps: this step and next step

        # initialize time, states and inputs to 0
        X = np.zeros(sys.nstates)
        U = np.zeros([sys.ninputs, N])
        T = np.linspace(T_start, T_end, N)

        # for storing results
        resp = {}
        U_new = np.zeros(sys.ninputs)

        # store noise index for each val (for noise simulation)
        noise_index = dict.fromkeys(self.noise_lvls, 0)

        # infinite loop, yield and wait for next input U(t)
        while True:
            
            # TODO, make sure U is within validity limits

            # Do one step of the simulation
            T_out, Y_out, X_out = control.input_output_response(sys, T, U, X0=X, return_x=True)
            
            Y_out = np.atleast_2d(Y_out) # handles the case of 1D outputs
            X_out = np.atleast_2d(X_out) # handles the case of 1D inputs
            
            # Store inputs and outputs in response dictionary
            for key in sys.output_index:
                noise_index[key] += (uniform(-0.001,0.001)*self.noise_lvls[key])                
                resp[key] = self.SS_vals[key] + Y_out[:,-1][sys.output_index[key]] + pnoise1(noise_index[key], octaves=4, persistence=5, repeat=256)/2

            for key in sys.input_index:
                noise_index[key] += (uniform(-0.001,0.001)*self.noise_lvls[key])                
                resp[key] = self.SS_vals[key] + U[:,-1][sys.input_index[key]] + pnoise1(noise_index[key], octaves=4, persistence=0.5, repeat=64)/2
            
            U_input = yield resp # yield response dict and store new input dict U

            if not isinstance(U_input, dict): # Check for correct input type of dictionary
                raise TypeError("Input U must be a dictionary")

            if (len(U_input) != self.nMVs): # Check for correct number of inputs
                raise ValueError(f"Input U must have exactly {self.nMVs} manipulated variables. Do not include feed-forwards.")

            # flatten input into a list
            for key in U_input:
                if not isinstance(U_input[key], numbers.Number): # Check for valid numbers as inputs
                    raise ValueError(f"Input U must contain numeric values")
                U_new[sys.find_input(key)] = self.initial_COs[key] - U_input[key] # adjust to take delta between initial CO and current CO

            # handle noise for FFs (modeled as input noise before going into TF)
            for key in self.inputs['FF']:
                noise_index[key] += (uniform(-0.01,0.01)*self.noise_lvls[key])                
                U_new[sys.find_input(key)] = pnoise1(noise_index[key], octaves=2, persistence=2)

            # Update T, X and U
            T = np.add(T, dt)  # step forward one time unit, dt
            X = X_out[:, -1]   # get the latest state, X

            # march forward one time step in the U input vector
            U[:,0] = U[:,1]
            U[:,1] = U_new
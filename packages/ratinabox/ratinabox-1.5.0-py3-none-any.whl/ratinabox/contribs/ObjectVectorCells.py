from ratinabox.Environment import Environment
from ratinabox.Agent import Agent
from ratinabox.Neurons import *
from ratinabox.utils import *

class ObjectVectorCells(Neurons):
    """

    """
    def __init__(self, Agent, params={}):
        """Initialise PhasePrecessingPlaceCell(), takes as input a parameter dictionary. Any values not provided by the params dictionary are taken from a default dictionary below.

        Args:
            params (dict, optional). Defaults to {}."""

        default_params = {
            "n": 10,
            "min_fr": 0,
            "max_fr": 1,
            "name": "ObjectVectorCell",
            "walls_occlude":True, 
            "field_of_view":False,
            "object_locations":None, #otherwise random across Env, the length of this will overwrite "n" 
            "angle_spread_degrees":15, #can be an array, one for each object 
            "pref_object_dist":0.25, #can be an array, one for each object, otherwise randomly drawn from a Rayleigh with this sigma
            "xi": 0.08,
            "beta": 12,
        }
        self.Agent = Agent
        default_params.update(params)
        self.params = default_params
        super().__init__(Agent, self.params)

        assert (self.Agent.Environment.dimensionality == "2D"), "object vector cells only possible in 2D"
        
        if self.object_locations is None: 
            self.object_locations = self.Agent.Environment.sample_positions(self.n)
            print(f"No object locations passed so {self.n} object locations have been randomly sampled across the environment")
        
        #preferred distance and angle to objects and their tuning widths (set these yourself if needed)
        self.tuning_angles = np.random.uniform(0, 2 * np.pi, size=self.n)
        self.tuning_distances = np.random.rayleigh(scale=self.pref_object_dist, size=self.n)
        self.sigma_distances = self.tuning_distances / self.beta + self.xi
        self.sigma_angles = np.array([(self.angle_spread_degrees / 360) * 2 * np.pi] * self.n)

        # normalises activity over the environment 
        locs = self.Agent.Environment.discretise_environment(dx=0.04)
        locs = locs.reshape(-1, locs.shape[-1])
        self.cell_fr_norm = np.ones(self.n)
        self.cell_fr_norm = np.max(self.get_state(evaluate_at=None, pos=locs), axis=1)

        print("HELLLLO")

        if self.walls_occlude == True: 
            self.wall_geometry = 'line_of_sight'
        else: 
            self.wall_geometry = 'euclidean'
        print(self.wall_geometry)

        if verbose is True:
            print(
                "ObjectVectorCells (OVCs) successfully initialised. You can also manually set their orientation preferences (OVCs.tuning_angles, OVCs.sigma_angles), distance preferences (OVCs.tuning_distances, OVCs.sigma_distances)."
            )
        return

    def get_state(self, evaluate_at="agent", **kwargs):
        """Returns the firing rate of the ObjectVectorCells.

        The way we do this is a little complex. We will describe how it works from a single position to a single OVC (but remember this can be called in a vectorised manner from an array of positons in parallel and there are in principle multiple OVCs)
            1. A vector from the position to the OVC is calculated. 
            2. The bearing of this vector is calculated and its length. Note if self.field_of_view == True then the bearing is relative to the heading direction of the agent (along its current velocity), not true-north.
            3. Since the distance to the OVC is calculated taking the environment into account if there is a wall occluding the agent from the obvject this object will not fire. 
            4. It is now simple to calculate the firing rate of the cell. Each OVC has a preferred distance and angle away from it which cause it to fire. Its a multiple of a gaussian (distance) and von mises (for angle) which creates teh eventual firing rate. 

        By default position is taken from the Agent and used to calculate firing rates. This can also by passed directly (evaluate_at=None, pos=pass_array_of_positions) or you can use all the positions in the environment (evaluate_at="all").

        Returns:
            firingrates: an array of firing rates
        """
        if evaluate_at == "agent":
            pos = self.Agent.pos
        elif evaluate_at == "all":
            pos = self.Agent.Environment.flattened_discrete_coords
        else:
            pos = kwargs["pos"]
        pos = np.array(pos)
        pos = pos.reshape(-1, pos.shape[-1]) #(N_pos, 2)
        N_pos = pos.shape[0]
        N_cells = self.n

        (distances_to_OVCs, vectors_to_OVCs) = self.Agent.Environment.get_distances_between___accounting_for_environment(pos,self.object_locations,return_vectors=True,wall_geometry=self.wall_geometry,) #(N_pos, N_cells) (N_pos, N_cells, 2)
        flattened_vectors_to_OVCs = vectors_to_OVCs.reshape(-1,2) #(N_pos x N_cells, 2)
        bearings_to_OVCs = utils.get_angle(flattened_vectors_to_OVCs,is_array=True).reshape(N_pos,N_cells) #(N_pos,N_cells)
        if self.field_of_view == True: 
            if evaluate_at == "agent":
                vel = self.Agent.velocity
            elif 'vel' in kwargs.keys():
                vel = kwargs["vel"]
            else:
                vel = np.array([1,0])
                print("Field of view OVCs require a velocity vector but none was passed. Using [1,0]")
            head_bearing = utils.get_angle(vel)
            bearings_to_OVCs -= head_bearing
        
        g = utils.gaussian(
            distances_to_OVCs, self.tuning_distances, self.sigma_distances, norm=1
        ) * utils.von_mises(
            bearings_to_OVCs, self.tuning_angles, self.sigma_angles, norm=1
        ) #(N_pos, N_cell)
        firingrate = g.T #(N_cell, N_pos)
        firingrate = firingrate / np.expand_dims(self.cell_fr_norm, axis=-1)
        firingrate = (
            firingrate * (self.max_fr - self.min_fr) + self.min_fr
        )  # scales from being between [0,1] to [min_fr, max_fr]

        return firingrate


if __name__ == "__main__":
    """Example of use
    """

    Env = Environment()
    Ag = Agent(Env)
    OVCs = ObjectVectorCells(
        Ag,
    )

    while Ag.t < 10:
        Ag.update()
        OVCs.update()

    Ag.plot_trajectory()
    OVCs.plot_rate_map()
    fig, ax = OVCs.plot_rate_timeseries()
    fig.show()

#Create a class to define internal nodes
#Where x-rays will be absorbed and heat transfer will occur through conduction only
class InternalElement:
    """This class is used by the Section class (via composition design pattern) and represents an internal,
    solid element of material. These elements absorb cold x-rays and transmit heat via conduction only."""
    
    #Class constructor
    def __init__(self,  
                 t_conductivity,
                 spec_heat,
                 cs_area, 
                 ic_temp, 
                 element_length,
                 ablation_temp,
                 rad_abs_coefficient,
                 density,
                 emissivity):
        """InternalElement Class Constructor
        This function is used to enter the material properties and initial conditions for each element.
        Inputs:
            t_conductivity <float>: Thermal conductivity of the element's material
            spec_heat <float>: Specific heat of the element's material
            cs_area <float>: The cross-sectional area of the element
            ic_temp <float>: The initial condition for temperature of the element
            element_length <float>: The length of the element (colinear w/ x-ray direction)
            ablation_temp <float>: The temperature at which the material ablates
            rad_abs_coefficient <float>: The mass attenuation factor of the material
            density <float>: The density of the material
        Outputs:
            None"""
        
        #Initialize instance state
        self.absorbed_energy = 0
        self.rem_energy_flux = 0
        self.temp = ic_temp
        self.t_conductivity = t_conductivity
        self.spec_heat = spec_heat
        self.cs_area = cs_area
        self.nm1_temp = 0
        self.nm0_temp = 0
        self.is_ablated = False
        self.element_length = element_length
        self.ablation_temp = ablation_temp
        self.rad_abs_coefficient = rad_abs_coefficient
        self.density = density
        self.emissivity = emissivity
        
    #Function to set the initial conditions for the element
    def set_ics(self, initial_temp):
        """This function is used to set the temperature initial condition of the element.
        Inputs:
            initial_temp <float>: The initial condition for temperature of the element
        Outputs:
            None"""
        
        self.nm1_temp = initial_temp
        
#Create a class to define the entire section of material
#The computation will be performed here
class Section:
    """This class is used to represent a cross-section of one or more materials which will absorb x-rays and undergo
    thermal changes."""
    
    eV_to_Joule = 1.602e-19
    
    #Class constructor
    def __init__(self):
        self.elements_list = []
        self.rem_elements = []
        self.has_run_rad = False
        self.has_run_ablation = False
        self.has_run_temp = False
    """InternalElement Class Constructor
        This function is used to initialize variables for a Section class instance. No inputs are required by the user
        at this step.
        Inputs:
            None
        Outputs:
            None"""
        
    #Function to add a material layer to the section
    #Materials added from foreward (x-ray incoming direction) and populates back
    def add_matl(self,
                 quantity,
                 t_conductivity,
                 spec_heat,
                 cs_area,
                 ic_temp,
                 element_length,
                 ablation_temp,
                 rad_abs_coefficient,
                 density,
                 emissivity):
        """add_matl function
        This function is used to add a new thickness of material. Call this function multiple times to add additional
        material layers. Subsequent calls will add material to the back (away from initial x-ray impingment surface)
        Inputs:
            quantity <int>: Number of elements in the section of material
            t_conductivity <float>: The material's thermal conductivity
            spec_heat <float>: The material's specific heat
            cs_area <float>: The cross sectional area for the 1D material section (normal to x-rays)
            ic_temp <float>: Initial temperature of the material
            element_length <float>: The length of each element in the material layer
            ablation_temp <float>: The temperature at which the material will ablate
            rad_abs_coefficient <float>: The mass attenuation factor of the material
            density <float>: The density of the material
            emissivity <float>: The emissivity of the material
        Outputs:
            None"""
        
        for i in range(0, quantity):
            new_element = InternalElement(t_conductivity,
                                          spec_heat,
                                          cs_area,
                                          ic_temp,
                                          element_length,
                                          ablation_temp,
                                          rad_abs_coefficient,
                                          density,
                                          emissivity)
            self.elements_list.append(new_element)
        
    #Function to propagate x-rays through material
    def prop_xray_energy(self, tot_x_ray_energy):
        """prop_xray_energy function
        After all the layers of materials have been added, call this function to pass x-ray energy through
        the material section to calculate how much each element absorbs and the accompanying temperature change
        Inputs:
            tot_x_ray_energy <float>: Energy of all the x-rays to pass through the material's section [eV]
        Outputs:
            None"""
    
        tsprt_flux = tot_x_ray_energy
        for element in self.elements_list:
            delta_tsprt_flux = tsprt_flux * element.rad_abs_coefficient * element.density * element.element_length
            element.absorbed_energy = delta_tsprt_flux * Section.eV_to_Joule
            element.rem_energy_flux = tsprt_flux
            tsprt_flux = tsprt_flux - delta_tsprt_flux
            
        for element in self.elements_list:
            volume = element.cs_area * element.element_length
            element.temp = element.absorbed_energy / (volume*element.density*element.spec_heat) + element.temp
    
    #Function to get the total absorbed x-ray energy for each element
    def get_absorbed_energy(self):
        """get_absorbed_energy function
        After passing the x-ray energy through the material, use this function to get a list
        of the energy absorbed by each element.
        Inputs:
            None
        Outputs:
            Absorbed energy of each element <List of floats>"""
        
        absorbed_energy_list = []
        for element in self.elements_list:
            if isinstance(element, InternalElement):
                absorbed_energy_list.append(element.absorbed_energy)
        
        return absorbed_energy_list
    
    #Function to get the remaining x-ray flux through each element
    def get_rem_energy(self):
        """get_rem_energy function
        After passing the x-ray energy through the material, use this function to get a list
        of the energy that passes through each element.
        Inputs:
            None
        Outputs:
            Remaining energy passing through each element <List of floats>"""
        
        rem_flux_list = []
        for element in self.elements_list:
            if isinstance(element, InternalElement):
                rem_flux_list.append(element.rem_energy_flux)
                
        return rem_flux_list
    
    #Function to get the temperature distribution for each element
    def get_temperatures(self):
        """get_temperatures function
        After passing the x-ray energy through the material, use this function to get a list
        of the temperature for each element
        Inputs:
            None
        Outputs:
            Temperature of each element <List of floats>"""
        temp_list = []
        for element in self.elements_list:
            if isinstance(element, InternalElement):
                temp_list.append(element.temp)
                
        return temp_list
    
    #Function to get a list of the distances of each node from the outermost surface
    def get_node_depths(self):
        """get_node_distances function
        After configuring the material section, use this function to return a list of the depth for each element.
        This is useful when plotting performance and parameters of the section as a function of distance.
        Inputs:
            None
        Outputs:
            Depth of each element <List of floats>"""
        
        dist_list = []
        dist = 0
        for element in self.elements_list:
            if isinstance(element, InternalElement):
                dist_list.append(dist)
                dist += element.element_length
                
        return dist_list
    
    #Function to get a list of mass attenuation factors for each element
    def get_macs(self):
        """get_macs function
        After configuring the material section, use this function to return a list of the mass attenuation coefficient
        for each element.
        Inputs:
            None
        Outputs:
            Mass attenuation coefficient of each element <List of floats>"""
        
        mac_list = []
        for element in self.elements_list:
            if isinstance(element, InternalElement):
                mac_list.append(element.rad_abs_coefficient)
                
        return mac_list
    
    #Function to get a list of densities for each element
    def get_densities(self):
        """get_densities function
        After configuring the material section, use this function to return a list of the density for each element.
        Inputs:
            None
        Outputs:
            Density of each element <List of floats>"""
        
        density_list = []
        for element in self.elements_list:
            if isinstance(element, InternalElement):
                density_list.append(element.density)
                
        return density_list
    
    #Function to evaluate ablation
    def eval_ablation(self):
        ablated_element_list = []
        for element in self.elements_list:
            if (element.temp > element.ablation_temp):
                element.is_ablated = True
                ablated_element_list.append(0)
            else:
                element.is_ablated = False
                ablated_element_list.append(1)
        return ablated_element_list
    
    
     #Function to iterate through time for transient thermal analyses for the nomainal condition before cold x-ray exposure.

    def transient_thermal_analysis(self, L, T0, Tinf, rho, c, k, dx, dt, t_max, emissivity, solar_flux):
        
        # Calculate the number of spatial and temporal steps
        n_x = int(L/dx) + 1
        n_t = int(t_max/dt) + 1

        # Initialize the temperature array
        T = np.zeros((n_t, n_x))

        # Set the initial temperature
        T[0,:] = T0

        # Set the boundary conditions
        T[:,0] = 303.15 #temp of space craft in kelvin
        T[:,-1] = T[:,-2] + solar_flux*dx/k - emissivity*5.67e-8*(T[:,-2]**4 - Tinf**4)*dx/k

        # Calculate the coefficients
        alpha = k*dt/(rho*c*dx**2)
        beta = 1 - 2*alpha

        # Iterate over time
        for i in range(1, n_t):
            for j in range(1, n_x-1):
                T[i,j] = alpha*(T[i-1,j+1] + T[i-1,j-1]) + beta*T[i-1,j]

            # Update the boundary conditions
            T[i,0] = 303.15 #temperature of space craft in kelvin
            T[i,-1] = T[i,-2] + solar_flux*dx/k - emissivity*5.67e-8*(T[i,-2]**4 - Tinf**4)*dx/k

        # Plot the temperature vs time at a specific point in the plate
        t = np.linspace(0, t_max, n_t)
        plt.plot(t, T[:,int(n_x/2)])
        plt.xlabel('Time (s)')
        plt.ylabel('Temperature (K)')
        plt.title('Temperature vs Time at x = L/2')
        plt.show()

        #Function to iterate through time for transient thermal analyses for the plate post cold-xray
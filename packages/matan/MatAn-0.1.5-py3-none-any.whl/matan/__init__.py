import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "src"))

import numpy as np
import matplotlib.pyplot as plt

import glob
from typing import Union
import properties
# from sklearn.linear_model import LinearRegression


"""

1. move real and eng values to other files
2. create instance in sample
3. inherit logic to both eng and real values from another class
SOURCES:

https://professorkazarinoff.github.io/Engineering-Materials-Programming/07-Mechanical-Properties/mechanical-properties-from-stress-strain-curves.html

According to ISO 527-1: https://cdn.standards.iteh.ai/samples/75824/61c480ef4bf0494aa6966bd4c2244c2e/ISO-527-1-2019.pdf
"""

"""c
    class to menage files
    methods are types of techniques used to manufacture material
    """

class files:
    def __init__(self,path, extension:str, methods=None):
        """This class can manage the files as well as it's parameters

        This class helps managing he files, find their names/paths, extract the method of manufacturing or other
        parameters

        Parameters
        ----------
        path : str
            This variable is used to put path to your files
        extension : str
            Extention is the extention of your files. If your file is .csv put csv in there, be aware and do not put the dot before your extention
        methods : str
            Descripe the technique of manufacturing there, or find it using find_method in that class

        Examples
        --------
        FIXME: Add docs.

        """

        if extension.startswith("."):
            extension=extension[1:]
        
        self.files=glob.glob(os.path.join(path, f"*.{extension}"))
        
        try:
            splitted = [os.path.split(file)[1] for file in self.files if any(method in file for method in methods)] #split to extract names
            self.paths = [file for file in self.files if any(method in file for method in methods)]
        except TypeError:
            splitted = [os.path.split(file)[1] for file in self.files]
            self.paths = [file for file in self.files]
        self.names = [name.split("_")[0] for name  in splitted]
        self.methods = [self.find_method(name) for name in self.names ] #thats for 
    def find_method(self,path, delimiter='-'):
        """Find the technique how the material was created

        Find the method how the material was created, what methods were used to modify it, etc. To do so it is using
        first letters of filename, so for extruded parts you can use EXT, for annealed extruded parts you can use aEXT
        etc.

        Parameters
        ----------
        path : str
            path for your file
        delimiter : str
            what sign you wanna use to finish your method string. By default it is -

        Examples
        --------
        FIXME: Add docs.

        """

        method = path.split(delimiter)[0]
        return method

class sample:
    """
    Class to menage material, material properities, converting to engineerin stress etc.
    """
    def __init__(self,name: str,
                 thickness:float = None,
                 width:float = None,
                 elongation_array: Union[list, np.array] =None,
                 force_array: Union[list, np.array] =None,
                 stress_array: Union[list, np.array] =None,
                 strain_array: Union[list, np.array] =None,
                 force_units: str="N",
                 lenght_units: str="mm"):

        self.name=name
        self.thickness, self.width= thickness,width
        self.eng_values=engineering_values(name=name,
                                           force_units=force_units,
                                           lenght_units=lenght_units,
                                           thickness=thickness,
                                           width=width
                                           )
        self.real_values=real_values_class(name=name,
                                           thickness=thickness,
                                           width=width,
                                           force_units=force_units,
                                           lenght_units=lenght_units,)
        
        if stress_array is None and strain_array is None:
            if elongation_array is None and force_array is None:
                raise ValueError("None of elongation/force or stress/strain arrays are defined!")
            elif thickness is None:
                raise ValueError("Thickness is not defined!")
            elif width is None:
                raise ValueError(" Width is not defined!")
            else:
                self.eng_values.calculate(thickness=self.thickness,
                                          width=self.width,
                                          elongation_array=elongation_array,
                                          force_array=force_array)
                self.real_values.calculate(self.eng_values.stress,
                                           self.eng_values.strain)
        else:
            self.eng_values.set(stress_array, strain_array)



                
        
    def composition_from_name(delimiter: str, percent_sign="p"):
        """
        TODODO baby shark
        method to obtain material ingridiens from name, as I usually name files extracted from machine with code allowing me to get that information from filename
    Finds the proportional range of a stress-strain curve by searching for a derivative.
    
    Parameters:
        strain (array-like): An array of strain values.
        stress (array-like): An array of corresponding stress values.
        n: An count of chunks to divide stress/strain array
    
    Returns:n
            Sets start and end of proportional range points
    """
        pass
    
class engineering_values:
        def __init__(self,
                     thickness,
                     width,
                     name=None,
                     force_units="N",
                      lenght_units="mm"
            ):
            """initializer of engineering values class

            This class is used to menage the properties of engineering values

            Parameters
            ----------
            name : str
                name for your sample

            Examples
            --------
            FIXME: Add docs.

            """
            
            self.name=name
            self.force_units = force_units
            self.lenght_units=lenght_units
            self.thickness=thickness,
            self.width=width
            self.stress, self.strain=None,None
        def calculate(self,
                      thickness:float,
                      width:float,
                      elongation_array,
                      force_array,
                      ):
            """Calculates the engineering stress and strain

            This method is used to calculate engineering stress and strain from height

            Parameters
            ----------
            thickness : float
                smaller initial dimension of the rectangular cross-section in the central part of test specimen
            width : float
                larger initial dimension of the rectangular cross-section in the central part of the test specimen
            elongation_array : list
                list of the sample elongation
            force_array : list
                list of the forces from the machinge
            force_units : str
                Units used as force units. Newtons [N] by default. Use shorten strings, as it is used in output
            lenght_units : str
                Units used for lenght, mm by default. Use short strings, as they are used in output. If you wanna use percent, just use % sign or percent
            """
            

            if self.lenght_units=="%" or self.lenght_units=="percent":
                self.percent_strain=True
            else:
                self.percent_strain=False


            if  self.stress is  None and self.strain is None:
                initial_area=thickness*width
                self.stress=[force/initial_area for force in force_array]
                if self.percent_strain:
                    self.strain=[strain for strain in elongation_array]
                else:
                    self.strain=[strain*0.01 for strain in elongation_array]

            self.strength=self.calculate_strength(self.stress,
                                                  self.strain)
            
            self.at_break=self.calculate_at_break(self.strain,
                                                  self.stress)
            
            self.yield_strength=self.calculate_yield_strength(self.stress,
                                                              self.strain)
            self.tensile_modulus=self.calculate_tensile_modulus()

        class calculate_strength:
            def __init__(self,strain: np.array,stress:np.array):
                """Strenght is according to ISO-527-1 first maximum local value

                Parameters
                ----------
                strain : np.array
                    strain array
                stress : np.array
                    stress array

                Examples
                --------
                FIXME: Add docs.

                """
                
                strength = properties.strenght(strain,stress)
                self.value=strength.value
                self.strain=strength.strain

        class calculate_yield_strength:
            def __init__(self, stress: np.array, strain: np.array):
                """Yield strenght  is according to ISO-527-1 strain increase without stress increase. 

                Parameters
                ----------
                stress : np.array
                    stress numpy array
                strain : np.array
                    strain numpy array

                Examples
                --------
                FIXME: Add docs.

                """
                yield_strenght=properties.yield_strenght(stress, strain)
                self.value, self.strain=yield_strenght.value,yield_strenght.strain
        class calculate_at_break:
            """
            This class calculates values at the brain according to ISO 527-1
            """
            def __init__(self,stress, strain):
                at_break=properties.at_break(stress, strain)
                self.stress=at_break.stress
                self.strain=at_break.strain


        def calculate_tensile_modulus(self,
                                    plot=True,
                                    r2=True,
                                    output=True,
                                    lower_limit=0.05,
                                    upper_limit=0.25
                                    ):
            """            Tensile, or Young's modulus is the slope of strain/stress curve, between strains equals to 0.05 and 0.25 percent according to DIN ISO 527-1

            Parameters
            ----------
            plot : bool
                Put True for use pyplot on the tensile modulus part
            r2 : Put coeffitient 	of determination into pyplot label
                Put coeffitient of determination into pyplot label
            output : bool
                Print the output of this method
            lower_limit : float
                lower limit of the measurement boundary
            upper_limit : float
                upper limit of the measurement boundary

            Examples
            --------
            FIXME: Add docs.

            """

            E=properties.tensile_modulus(self.stress,
                                       self.strain,
                                       percent_strain=self.percent_strain
                                       )
            if plot:
                label=rf"Young's modulus {int(E.tensile_modulus)} $\left[\frac{{{self.force_units}}}{{{self.lenght_units}^2}}\right]$"
                if r2:
                    label+="\n"+rf"$R^{{{2}}}={E.r2}$"
                plt.plot(E.module_strain,
                         E.module_stress,
                         label=label
                         )
            if output:
                print(f"Tensile modulus is equal to {int(E.tensile_modulus)} [{self.force_units}/{self.lenght_units}^2]")
                return   E.tensile_modulus

                
        def set(self,
                engineering_stress: Union[list, np.array] =None,
                engineering_strain:Union[list, np.array] =None,
                # TODO: gives TypeError: only size-1 arrays can be converted to Python scalars while using numpy array
                # TODO: gives KeyKerrr None
                # TODO: in general this method does not work yet!
                ):
            """Method to set engineering stress and engineering strain

            Parameters
            ----------
            engineering_stress : list
                array of engineering stress
            engineering_strain : list
                array of engineering strain

            Examples
            --------
            FIXME: Add docs.

            """
            
            self.stress, self.strain=engineering_stress, engineering_strain
            self.calculate(thickness=self.thickness,
                                      width=self.width,
                                      elongation_array=None,
                                      force_array=None)
            

        def plot(self, show=False):
            """Method for plotting the results

            This method can be used to plot your engineering stress-strain curve. If you wanna show it instantly use
            parameter show as True

            Parameters
            ----------
            show : bool
                It it equal to matplotlib.pyplot function show

            Examples
            --------
            FIXME: Add docs.

            """
            plt.plot(self.strain,self.stress, label=self.name)
            plt.title(self.name)
            plt.ylabel(rf"Stress $\left[\frac{{{self.force_units}}}{{{self.lenght_units}^2}}\right]$")
            plt.xlabel(f"Strain [{self.lenght_units}]")
            plt.legend()
            if show:
                plt.show()

class real_values_class(engineering_values):

        def __init__(self, name,
                     thickness,
                     width,
                     force_units,
                     lenght_units,
                     ):
            self.force_units=force_units
            self.lenght_units=lenght_units
            if lenght_units=="%" or lenght_units=="percent":
                self.percent_strain=True
            else:
                self.percent_strain=False

    
            engineering_values.__init__(self,
                                        name=name,
                                        thickness=thickness,
                                        width=width
                                        )
            self.name=name + " [real]"
            width=self.width
            super().__init__(self,
                             width=width,
                             name=self.name
                             )

        def calculate(self, stress, strain):
            """
                Calculates the true stress and strain, from engineering values.
                Read more there:
                        https://courses.ansys.com/index.php/courses/topics-in-metal-plasticity/lessons/how-to-define-a-multilinear-hardening-plasticity-model-lesson-1/
    
                Parameters:
                        strain (array-like): An array of strain values.
                        stress (array-like): An array of corresponding stress values.
                        n: An count of chunks to divide stress/strain array
    
                Returns:
                    A tuple (start_strain, end_strain) representing the proportional range of the stress-strain curve.
            """
            self.stress=[stress_val*(1+strain_val) for stress_val, strain_val in zip(stress, strain)]
            self.strain=[np.log(1+strain_val) for strain_val in strain]

            self.strength=self.calculate_strength(self.stress,
                                                  self.strain)
            
            self.at_break=self.calculate_at_break(self.strain,
                                                  self.stress)
            
            self.yield_strength=self.calculate_yield_strength(self.stress,
                                                              self.strain)
            self.tensile_modulus=self.calculate_tensile_modulus()            



        # def plot(self, show: bool=False):
        #     plt.plot(self.strain,self.stress, label=self.name)
        #     plt.title("real")
            
        #     plt.legend()
        #     if show:
        #         plt.show()


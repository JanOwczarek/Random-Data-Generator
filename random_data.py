import pandas as pd
import random

class RandomData(pd.DataFrame):
    types_spec = ["con", "cat", "interval", "binary"]
    _metadata = ['rd_dict', 'rd_size', 'rd_seed']

    def __init__(self, data=None, *args, rd_dict=None, rd_size=None, rd_seed=None, **kwargs): # The *args and **kwargs seems necessary
        super().__init__(data, *args, **kwargs)
        if (rd_dict!=None) & (type(rd_dict) is dict):
            """Processing -size-"""
            try:
                self.rd_size = int(rd_size)
            except ValueError:
                raise Exception("-size- parameter needs to be an integer or convertible to an integer.")

            """Process -seed-"""
            # Will be used in the methods which are part of .process_variables()
            self.rd_seed = self.__process_seed(rd_seed)

            """Checking -rd_dict-"""
            try: 
                assert type(rd_dict) is dict
            except AssertionError:
                raise Exception("-data_def- parameter needs to be a dictionary.")
            
            # The first item of the dictionary key's value needs to be a recognized variable type
            for val in rd_dict.values():
                if val[0] not in RandomData.types_spec:
                    raise Exception("Some of the variables types specified are not recognized by class. The options are: 'cat', 'con', 'interval', 'binary'")
                else:
                    continue

            """Create rd_data dictionary (as the data= argument needed for pd.DataFrame)"""
            data = self.process_variables(def_dict=rd_dict)

            """Create variable to show that this data has been created by the random methods"""
            self.random_data = True
            pass

        else:
            self.random_data = False
        
        # Here we need to instantiate the parent's methods and attributes again because we possibly changed the -data- argument above.
        super().__init__(data, *args, **kwargs)
            
    
    @property
    def _constructor(self):
        """Constructor needed for subclassing"""
        def _c(*args, **kwargs):
            return RandomData(*args, **kwargs)
        return _c
    

    """DATA CREATING METHODS BELOW"""
    # Instead of creating the pd.DataFrame, simply create the components for the data argument (see __init__) in each of these __create_..() methods.

    def process_variables(self, def_dict):
        """Method that creates the provided variables, called in create_data and add_variables methods"""
        # Locate all types of var entries ("cat", "con", "interval", "binary"), assert that it is in the first position of the list after entry
        con_keys = [key for key, val in def_dict.items() if val[0]=="con"]
        cat_keys = [key for key, val in def_dict.items() if val[0]=="cat"]
        intv_keys = [key for key, val in def_dict.items() if val[0]=="interval"]
        bin_keys = [key for key, val in def_dict.items() if val[0]=="binary"]

        data_dict = {}

        # Iterate over the items in the data dictionary and create data variable by variable
        for var_name, spec in def_dict.items():
            """Methods referenced below need to check if the specs are compatible."""
            if var_name in con_keys:
                ## Process continuous variable
                name, var = self.__create_con(name=var_name, spec_detail=spec)
                # Add to dict
                data_dict[name] = var

            elif var_name in cat_keys:
                ## Process categorical variable
                name, var = self.__create_cat(name=var_name, spec_detail=spec)
                # Add to dict
                data_dict[name] = var

            elif var_name in intv_keys:
                ## Process interval variable
                name, var = self.__create_interval(name=var_name, spec_detail=spec)
                ## Add to dict
                data_dict[name] = var

            elif var_name in bin_keys:
                ## Process binary variable
                name, var = self.__create_binary(name=var_name, spec_detail=spec)
                # Add to dict
                data_dict[name] = var


        # Return the data dictionary
        return data_dict


    def __create_cat(self, name, spec_detail):
        """Method appending the dictionary that will inform the data argument in the __init__ statement!"""

        """Check if spec_detail is in the correct format."""
        try:
            assert ((len(spec_detail)==2) & (type(spec_detail[1]) is list))
        except AssertionError:
            raise Exception("Specification for categorical data is not in the correct format. It needs to have two items where the second argument is a list specifying the categories.")

        """Create categorical variable"""
        # Generate a list of random integers within the range of the categories, the second item within the list should be a list, also set seed
        random.seed(self.rd_seed)
        rand_ints = [random.randint(0, len(spec_detail[1])-1) for num in range(self.rd_size)]
        
        # Populate the rand_ints with the categories using indexing and delete rand_ints
        cat_var = [spec_detail[1][i] for i in rand_ints]
        del rand_ints

         # Send confirmation message
        print("Categorical variable "+"'"+name+"'"+" created.")

        # Return variable in list form and the name of the variable
        return name, cat_var


    def __create_con(self, name, spec_detail):
        """Check if spec_detail is in correct format"""
        try:
            assert (type(spec_detail[1]) is list)
        except AssertionError:
            raise Exception("Specification for continuous data is not in correct format. Second item in list needs to be a list.")
        
        try:
            for item in spec_detail[1]:
                assert type(item) is int
        except AssertionError:
            raise Exception("Continuous specification: not all items in the second item of spec (list) are integers.")

        """Create continuous variable"""
        # Generate list of values
        resolution = spec_detail[1][2]
        random.seed(self.rd_seed)
        rand_con = [round(random.uniform(spec_detail[1][0],spec_detail[1][1]), resolution) for num in range(self.rd_size)]
        
        # Return variable in list form and the name of the variable
        return name, rand_con


    def __create_binary(self, name, spec_detail):
        """Check if spec_detail is in correct format"""
        try:
            assert ((len(spec_detail)==2) & (type(spec_detail[1]) is list) & (len(spec_detail[1])==2))
        except AssertionError:
            raise Exception("Specification for binary data is not in the correct format. It needs to have two items where the second argument is a list specifying the categories.")
        
        """Create binary variable"""
        # Generate a list of random integers within the range of the binary categories, the second item within the list should be a list, also set seed
        random.seed(self.rd_seed)
        rand_ints = [random.randint(0, len(spec_detail[1])-1) for num in range(self.rd_size)]
        
        # Populate the rand_ints with the categories using indexing and delete rand_ints
        bin_var = [spec_detail[1][i] for i in rand_ints]
        del rand_ints

        # Send confirmation message
        print("Binary variable "+"'"+name+"'"+" created.")

        # Return variable in list form and the name of the variable
        return name, bin_var


    def __create_interval(self, name, spec_detail):
        """Check if spec_detail is in correct format"""
        try:
            assert ((len(spec_detail)==2) & (type(spec_detail[1]) is list) & (len(spec_detail[1])==2))
        except AssertionError:
            raise Exception("Specification for interval data is not in the correct format. It needs to have two items where the second argument is a list specifying the interval range.")
        
        try:
            assert (spec_detail[1][0]<=spec_detail[1][1])
        except AssertionError:
            raise Exception("The interval range "+str(spec_detail[1])+" is incorrect. The first item needs to represent the lower end of the range.")

        """Create interval variable"""
        # Generate list of values
        random.seed(self.rd_seed)
        rand_int = [random.randint(spec_detail[1][0],spec_detail[1][1]) for num in range(self.rd_size)]

        # Send confirmation message
        print("Interval variable "+"'"+name+"'"+" created.")
        
        # Generate variable
        return name, rand_int


    @staticmethod
    def __process_seed(seed):
        """Seed needs to be an integer or string to start with."""
        try:
            assert (type(seed) in [int, str])
        except AssertionError:
            raise Exception("-seed- parameter needs to be a string or an integer.")
        
        """If seed is a string it needs to be either 'standard', 'random' or convertible to an integer (not a float)"""
        try:
            assert ((type(seed) is str) & ((seed in ["random","standard"]) | (seed.isdigit()==True)))
        except AssertionError:
            raise Exception("Specified string type -seed- needs to be 'standard' OR 'random' OR integer convertible string. 'random' specifies no control over seed and 'standard' defaults to 42.")
        
        """Convert seed to appropriate value."""
        if (type(seed) is int) | (seed.isdigit()==True):
            print("Seed is integer type or a integer convertible string. Specific seed specified.")
            processed_seed = int(seed)
            return processed_seed

        elif (type(seed) is str) & (seed.lower()=="random"):
            print("Random seed will be used to generate data.")
            processed_seed = None
            return processed_seed

        elif (type(seed) is str) & (seed.lower()=="standard"):
            print("The standard seed 42 will be used.")
            processed_seed = 42
            return processed_seed
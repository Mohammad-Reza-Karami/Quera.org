########################### Classes and Functions ###############################
Lands = []
class Land:
    def __init__(self, Allowed_Plant_Types: set) -> None:
        self.Allowed_Plant_Types = Allowed_Plant_Types
        self.Plant = None
        self.Plant_Age = 0
        self.Fertilizers = []
    def Plant_This (self, Plant_Name: str):
        This_Plant = Search_for_Object_by_Name (Plant_Name, Plants)
        # Checking if there is a live plant on this land and if we are allowed to plant this type on this land:
        if self.Plant_Age == 0 and This_Plant.Type in self.Allowed_Plant_Types:
            self.Plant = This_Plant
            self.Plant_Age = 1
            return "done"
        return "failed"
    def Fertilize (self, Fertilizer_Name):
        # Checking if we have this fertilizer on our fertilizers:
        if Search_for_Object_by_Name (Fertilizer_Name, Fertilizers):
            This_Fertilzer = Search_for_Object_by_Name (Fertilizer_Name, Fertilizers)
            if This_Fertilzer.Stock > 0:
                This_Fertilzer.Stock -= 1
                # Adding tis fertilizer to this land and setting its age to 1:
                self.Fertilizers.append ([This_Fertilzer, 1])
                return "done"
            return "failed"
        return "failed"
    @property
    def Harvest (self):
        if self.Plant:
            Yield = self.Plant.Growth_Rate
            if self.Fertilizers:
                # Yield will be multiplied by summation of active fertilizers's incremental coefficient:
                Yield *= sum ([Item [0].Incremental_Coefficient for Item in self.Fertilizers])
            Storage [self.Plant.Name] += Yield
            self.Plant_Age += 1
            # Getting ride of dead plant:
            if self.Plant_Age == 6: self.Plant, self.Plant_Age = None, 0
        for Item in self.Fertilizers: Item [1] += 1
        # Getting ride of non-active fertilizers:
        self.Fertilizers = [[F, A] for F, A in self.Fertilizers if A <= F.Durability]
        
Plants = set () 
class Plant:
    def __init__(self, Name: str, Type: str, Basic_Price: float, Growth_Rate: float) -> None:
        self.Name = Name
        self.Type = Type
        self.Basic_Price = Basic_Price
        self.Growth_Rate = Growth_Rate

Fertilizers = set ()
class Fertilizer:
    def __init__(self, Name: str, Incremental_Coefficient: float, Durability: int) -> None:
        self.Name = Name
        self.Incremental_Coefficient = Incremental_Coefficient
        self.Durability = Durability
        self.Stock = 0

Costumers = set ()
class Costumer:
    def __init__(self, Name: str) -> None:
        self.Name = Name
        self.Reputation = 0
        self.Total_Purchase = 0

Days = []
class Day:
    def __init__ (self, Jobs: list, Orders: list) -> None:
        self.Jobs = Jobs
        self.Orders = Orders
        self.Responses = []
    @property
    def Do_Jobs (self):
        for Job in self.Jobs:
            Job = Job.split ()
            if Job [0] == "bekar":
                Land_Index, Plant_Name = int (Job [1]) - 1, Job [2]
                self.Responses.append (Lands [Land_Index].Plant_This (Plant_Name))
            elif Job [0] == "kooddehi":
                Land_Index, Fertilizer_Name = int (Job [1]) - 1, Job [2]
                self.Responses.append (Lands [Land_Index].Fertilize (Fertilizer_Name))
            elif Job [0] == "koodgiri":
                Fertilizer_Name, Unit_Value = Job [1], int (Job [2])
                Search_for_Object_by_Name (Fertilizer_Name, Fertilizers).Stock += Unit_Value
                self.Responses.append ("done")
    @property
    def Store_Products (self):
        for Object in Lands: Object.Harvest
    @property
    def Do_Orders (self):
        for Order in self.Orders:
            Costumer_Name, Requested_Plant_Name, Requested_Value = Order.split () [0], Order.split () [1], float (Order.split () [2])
            # Adding this costumer to our costumers if it's new:
            if not Search_for_Object_by_Name (Costumer_Name, Costumers): Costumers.add (Costumer (Costumer_Name))
            This_Costumer = Search_for_Object_by_Name (Costumer_Name, Costumers)
            # Checking if we have this plant in our storage:
            if Requested_Plant_Name in Storage:
                # Checking if we have requested amount of this plant in storage:
                if Requested_Value <= Storage [Requested_Plant_Name]:
                    This_Plant = Search_for_Object_by_Name (Requested_Plant_Name, Plants)
                    Storage [Requested_Plant_Name] -= Requested_Value
                    Purchase_Amount = Requested_Value * (This_Costumer.Reputation + This_Plant.Basic_Price)
                    This_Costumer.Total_Purchase += Purchase_Amount
                    This_Costumer.Reputation += 1
                    self.Responses.append (str (Purchase_Amount)) if int (Purchase_Amount) != Purchase_Amount else self.Responses.append (int (Purchase_Amount))
                else:
                    This_Costumer.Reputation -= 1
                    self.Responses.append ("-1")
            else: 
                    This_Costumer.Reputation -= 1
                    self.Responses.append ("-1")
    @property
    def Make_Top_5 (self):
        if Costumers:
            # Making a list of (CostumerName, Total_Purchase) tuples:
            Costumers_Name_Purchase = []
            for Object in Costumers: Costumers_Name_Purchase.append ((Object.Name, Object.Total_Purchase))
            Costumers_Name_Purchase = sorted (Costumers_Name_Purchase, key = lambda Item: (-Item [1], Item [0]))
            # If we have less than 5 resaults, return all of them:
            try: self.Responses.append (" ".join ([Item [0] for Item in Costumers_Name_Purchase] [0: 5]))
            except IndexError: self.Responses.append (" ".join ([Item [0] for Item in Costumers_Name_Purchase]))

def Search_for_Object_by_Name (Name: str, Collection):
    for Object in Collection:
        if Object.Name == Name: return Object
    return False

############################### Input Handling ###################################
# n Lands:
for i in range (n := int (input ())):
    Allowed_Plant_Types = set ()
    This_Land = input ().split ()
    if This_Land [0] == "1": Allowed_Plant_Types.add ("derakht")
    if This_Land [1] == "1": Allowed_Plant_Types.add ("buteh")
    if This_Land [2] == "1": Allowed_Plant_Types.add ("risheh")
    Lands.append (Land (Allowed_Plant_Types))
# m Plants:
for i in range (m := int (input ())):
    Name, Type, Basic_Price, Growth_Rate = input ().split ()
    Plants.add (Plant (Name, Type, float (Basic_Price), float (Growth_Rate)))
# k Fertilizers:
for i in range (k := int (input ())):
    Name, Incremental_Coefficient, Durability = input ().split ()
    Fertilizers.add (Fertilizer (Name, float (Incremental_Coefficient), int (Durability)))
# d Days:
for i in range (d := int (input ())):
    Jobs, Orders = [], []
    # q1 Jobs:
    for j in range (q1 := int (input ())): Jobs.append (input ())
    # q2 Orders:
    for j in range (q2 := int (input ())): Orders.append (input ())
    Days.append (Day (Jobs, Orders))
# Initializing the storage:
Storage = {Object.Name: 0 for Object in Plants}

################################### Output ######################################
for Object in Days:
    Object.Do_Jobs
    Object.Store_Products
    Object.Do_Orders
    Object.Make_Top_5
    for Response in Object.Responses: print (Response)
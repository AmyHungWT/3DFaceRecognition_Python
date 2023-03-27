''' 23702699.py
CITS1401 Project 2
by: Amy HUNG'''

def main(csvfile, SubjIDs):
    # Checking if the SubjIDs in the list of input SubjIDs are string type
    for subj in SubjIDs:
        if type(subj) is not str:
            print("Please double check the format of the individual input SubjIDs (it should be string).")
            return [None, None, None, None]
        
    # Checking if the input file name is string type
    if type(csvfile) is not str:
        print("Please double check the format of the input filename (it should be string).")
        return [None, None, None, None]    
      
    # Checking if the list of input SubjIDs containing 2 SubjID
    if len(SubjIDs) < 2:
        print("Please double check the number of input SubjIDs (it should be 2).")
        return [None, None, None, None]
    
    # Checking if the input SubjIDs is in list format
    if type(SubjIDs) is not list:
        print("Please double check the format of the input SubjIDs (it should be a list).")
        return [None, None, None, None]
        
    SubjIDs = [each_SubjID.upper() for each_SubjID in SubjIDs]      # Changing all the input of SubjIDs to uppercase
    
    try:
        with open(csvfile) as IDdata:                               # Openning the input data file and save as new file (IDdata)
            ID_dict, landmark_dict, xyzlocation_dict = create_dictionary(IDdata)
            OP2_list = OP2R(ID_dict, xyzlocation_dict, SubjIDs)
            return [OP1R(ID_dict, landmark_dict, xyzlocation_dict, SubjIDs), OP2R(ID_dict, xyzlocation_dict, SubjIDs), OP3R(ID_dict, landmark_dict,xyzlocation_dict, SubjIDs), OP4R(ID_dict, xyzlocation_dict, SubjIDs, OP2_list)]

    # Checking if the input subjID is included in the data file
    except KeyError:
        print("Please double check the input SubjIDs (it is not included in the data file).")
        return [None, None, None, None] 

    # Checking any errors in openning/finding the file input
    except FileNotFoundError:
        print("File cannot be found. Please double check the input file.")
        return [None, None, None, None]
    
    except PermissionError:
        print("No permission to assess the file. Please double check the input file.")
        return [None, None, None, None]    
    
    except IsADirectoryError:
        print("The input filename is a directory. Please double check.")
        return [None, None, None, None]

    except UnicodeDecodeError:
        print("Please double check the format of input file.")
        return [None, None, None, None]

    except TypeError:                                                   
        print("There is a type error in the input. Please double check.")
        return [None, None, None, None]
    
    except NameError:
        print("There is a name error in the input. Please double check.")
        return [None, None, None, None]
    
def read_title(IDdata):                 # Reading the title of the input data file
    title = IDdata.readline()           # Reading the first row of the file (title)
    title = title.lower()               # Changing all the titles to lowercase
    title = title.strip().split(",")    # Spliting the title
    return title

# Creating dictionaries for input data file
def create_dictionary(IDdata):          

    title = read_title(IDdata)          # Extracting the title of file from function read_title(IDdata)
    
    ID_dict_value = ()
    ID_dict = {}
    
    for line in IDdata:                 # Reading the lines in the new data file (IDdata)
        line = line.strip().split(",")  # Spliting all the lines' content
        line[title.index("landmark")] = line[title.index("landmark")].upper() # Changing all the letters in landmark to uppercases
        line[title.index("subjid")] = line[title.index("subjid")].upper()     # Changing all the letters in subjid to uppercases
        
        # Checking if there is missing data in the file
        if (len(line[title.index("ox")])!= 0
            and len(line[title.index("oy")])!= 0
            and len(line[title.index("oz")])!= 0
            and len(line[title.index("mx")])!= 0
            and len(line[title.index("my")])!= 0
            and len(line[title.index("mz")])!= 0):
        
            # Creating a dictionary (xyzlocation_dict) for {3D coordinate name: 3D location values}
            xyzlocation_dict = {"ox":float(line[title.index("ox")]),
                                "oy":float(line[title.index("oy")]),
                                "oz":float(line[title.index("oz")]),
                                "mx":float(line[title.index("mx")]),
                                "my":float(line[title.index("my")]),
                                "mz":float(line[title.index("mz")])}
            
            # Creating a dictionary (landmark_dict) for {landmark:xyzlocaton_dict}
            landmark_dict = {line[title.index("landmark")]:xyzlocation_dict}
            
            # Creating a dictionary (ID_dict) for {subjID:landmark_dict}
            subjID_key = line[title.index("subjid")]
            
            if subjID_key not in ID_dict:
                ID_dict[subjID_key] = landmark_dict
            else:
                landmark_dict = ID_dict[subjID_key]
                landmark_dict[line[title.index("landmark")]] = xyzlocation_dict
    
    return ID_dict, landmark_dict, xyzlocation_dict

# Validating the input SubjID and data in data file
def data_validate(ID_dict, xyzlocation_dict, subj):
    subjID_key_list = list(ID_dict.keys())
    landmark_key_list = ["FT","EX","EN","AL","SBAL","CH","PRN"]
    location_key_list = list(xyzlocation_dict.keys())
    
    landmark_dict = ID_dict[subj]
    
    for landmark in landmark_key_list:                     # Checking if any landmark record is missing
        if landmark not in landmark_dict.keys():
            return None

    for landmark in landmark_key_list:   
        for location in location_key_list:
            coordinate = ID_dict[subj][landmark][location]
            if coordinate == "":                           # Checking if any 3D location value is missing
                return None
            elif coordinate < -200 or coordinate > 200:    # Checking if any 3D location value is out of bound
                return None
            else:
                continue
    
    # Checking if any facial asymmetry at nose tip is not zero
    if (landmark_dict["PRN"]["mx"] - landmark_dict["PRN"]["ox"] == 0
    and landmark_dict["PRN"]["my"] - landmark_dict["PRN"]["oy"] == 0
    and landmark_dict["PRN"]["mz"] - landmark_dict["PRN"]["oz"] == 0):
        return True
    else:
        return None  

# Calculating the output for OP1
def OP1R(ID_dict, landmark_dict, xyzlocation_dict, SubjIDs):

    OP1_list = []
    landmark_list = ["FT","EX","EN","AL","SBAL","CH"]    
    
    for subj in SubjIDs:
        OP1_dict = {}
        
        # Ensuring the input data passes the validation
        result = data_validate(ID_dict, xyzlocation_dict, subj)
        # Returning None if data doesn't pass the validation
        if result is None:
            OP1_list.append(None)                      # Appending the result into OP1_list
              
        else:
            # Calculating the facial asymmetry values between original and mirrored face if data passes the validation
            for landmark in landmark_list:                 
                ox = ID_dict[subj][landmark]["ox"]
                oy = ID_dict[subj][landmark]["oy"]
                oz = ID_dict[subj][landmark]["oz"]
                mx = ID_dict[subj][landmark]["mx"]
                my = ID_dict[subj][landmark]["my"]
                mz = ID_dict[subj][landmark]["mz"]
            
                asymmetry = round((((mx-ox)**2 + (my-oy)**2 + (mz-oz)**2)**0.5),4)
            
                OP1_dict[landmark] = asymmetry          # Creating a dictionary (OP1_dict) for {landmark:facial asymmetry values}
            OP1_list.append(OP1_dict)                   # Appending the result into OP1_list
    
    return OP1_list

# Calculating the output for OP2
def OP2R(ID_dict, xyzlocation_dict, SubjIDs):
    
    OP2_list = []
    location_list = ["ox","oy","oz"]
    
    for subj in SubjIDs:
        OP2_dict = {}
        EXEN_list = []
        ENAL_list = []
        ALEX_list = []
        FTSBAL_list = []
        SBALCH_list = []
        CHFT_list = []
        
        # Ensuring the input data passes the validation
        result = data_validate(ID_dict, xyzlocation_dict, subj)
        # Returning None if data doesn't pass the validation
        if result is None:
            OP2_list.append(None)     # Appending the result into OP2_list
        else:
            # Calculating the facial distances on original face if data passes the validation
            for location in location_list:
                EXEN = (ID_dict[subj]["EX"][location] - ID_dict[subj]["EN"][location])**2
                ENAL = (ID_dict[subj]["EN"][location] - ID_dict[subj]["AL"][location])**2
                ALEX = (ID_dict[subj]["AL"][location] - ID_dict[subj]["EX"][location])**2
                FTSBAL = (ID_dict[subj]["FT"][location] - ID_dict[subj]["SBAL"][location])**2
                SBALCH = (ID_dict[subj]["SBAL"][location] - ID_dict[subj]["CH"][location])**2
                CHFT = (ID_dict[subj]["CH"][location] - ID_dict[subj]["FT"][location])**2
                
                EXEN_list.append(EXEN)
                ENAL_list.append(ENAL)
                ALEX_list.append(ALEX)
                FTSBAL_list.append(FTSBAL)
                SBALCH_list.append(SBALCH)
                CHFT_list.append(CHFT)
                
            EXEN_diff = round((sum(EXEN_list))**0.5,4)
            ENAL_diff = round((sum(ENAL_list))**0.5,4)
            ALEX_diff = round((sum(ALEX_list))**0.5,4)
            FTSBAL_diff = round((sum(FTSBAL_list))**0.5,4)
            SBALCH_diff = round((sum(SBALCH_list))**0.5,4)
            CHFT_diff = round((sum(CHFT_list))**0.5,4)
            
            # Creating a dictionary (OP2_dict) for {Facial distance: Facial distance values}
            OP2_dict.update({"EXEN":EXEN_diff,"ENAL":ENAL_diff, "ALEX":ALEX_diff, "FTSBAL":FTSBAL_diff, "SBALCH":SBALCH_diff, "CHFT":CHFT_diff})    
            OP2_list.append(OP2_dict)       # Appending the result into OP2_list
    
    return OP2_list

# Calculating the output for OP3
def OP3R(ID_dict, landmark_dict ,xyzlocation_dict, SubjIDs):
    OP3_list = []
    OP3_dict = {}
    
    landmark_list = ["FT","EX","EN","AL","SBAL","CH"]
    
    for subj in ID_dict.keys():

        asymmetry_list = []
        # Ensuring the input data passes the validation
        result = data_validate(ID_dict, xyzlocation_dict, subj)
        # Skipping the subjID if data doesn't pass the validation
        if result is None:
            continue
        else:
            # Calculating the total facial asymmetry if data passes the validation
            for landmark in landmark_list:
                ox = ID_dict[subj][landmark]["ox"]
                oy = ID_dict[subj][landmark]["oy"]
                oz = ID_dict[subj][landmark]["oz"]
                mx = ID_dict[subj][landmark]["mx"]
                my = ID_dict[subj][landmark]["my"]
                mz = ID_dict[subj][landmark]["mz"]
            
                asymmetry = (((mx-ox)**2 + (my-oy)**2 + (mz-oz)**2)**0.5)
                asymmetry_list.append(asymmetry)
            
            total_asymmetry = round(sum(asymmetry_list),4)
            OP3_dict[subj] = total_asymmetry     # Creating a dictionary(OP3_dict) for {SubjID:Total facial asymmetry}
    
    
    OP3_dict = dict(sorted(OP3_dict.items(), key = lambda item:item[1]))  # Sorting OP3_dict in increasing order of total facial asymmetry
    OP3_pairs = {k: OP3_dict[k] for k in list(OP3_dict)[:5]}   # Extracting the lowest 5 pairs of (SubjID, Total facial asymmetry)
    OP3_list = list(OP3_pairs.items())           # Appending the result into a list

    return OP3_list

# Calculating the output for OP4
def OP4R(ID_dict, xyzlocation_dict, SubjIDs, OP2_list):
    distance_list = ["EXEN","ENAL","ALEX","FTSBAL","SBALCH","CHFT"]
    cossim_numerator_list = []
    cossim_denominator_f1_list = []
    cossim_denominator_f2_list = []
    
    # Checking if any of the OP2 result is None
    for value in OP2_list:     
        if (value is None):
            return None        # Returning None if there is None found in OP2 result
    
    else:
        # Calculating the cosine similarity score for f1 and f2 using OP2 result
        try:
            for distance in distance_list:
                cossim_numerator = OP2_list[0][distance] * OP2_list[1][distance]
                cossim_numerator_list.append(cossim_numerator)
                
                cossim_denominator_f1 = OP2_list[0][distance]**2
                cossim_denominator_f1_list.append(cossim_denominator_f1)
                cossim_denominator_f2 = OP2_list[1][distance]**2
                cossim_denominator_f2_list.append(cossim_denominator_f2)
        
            OP4_numerator = sum(cossim_numerator_list)
            OP4_denominator = ((sum(cossim_denominator_f1_list)**0.5) * (sum(cossim_denominator_f2_list)**0.5))
            
            cossim = round(OP4_numerator/OP4_denominator,4)

            return cossim
        
        # Checking if any zero division error in the cosine similarity score calculation
        except ZeroDivisionError:
            return None

''' 23702699.py
CITS1401 Project 1
by: Amy HUNG'''

def main(csvfile, adultID, Option):
    Option = Option.lower()           # Changing all the input of Option to lowercase
    
    with open(csvfile) as indivdata:  # Open the input file and do thing in a new data file (indivdata)
        if Option == "stats":
            return OP1(indivdata, adultID), OP2(indivdata, adultID), OP3(indivdata, adultID), OP4(indivdata, adultID)
        else:
            return cossim_max(indivdata, adultID)
        
def read_title(indivdata):              # To read the title of the input data file
    title = indivdata.readline()        # Reading the first row of the file (title)
    title = title.lower()               # Changing all the titles to lowercase
    title = title.strip().split(",")    # Spliting the title
    return title
    
def create_dictionary(indivdata):       # To create a dictionary
    indivdata.seek(0)                   # Going back to the first row of the file when processing this function

    title = read_title(indivdata)       # Extracting the title of file from function read_title(indivdata)
    unique_key_list = []
    indiv_dict = dict()
    
    for line in indivdata:              # Reading the lines in the new data file (indivdata)
        line = line.strip().split(",")  # Spliting all the lines' content
        line[title.index("expression")] = line[title.index("expression")].lower() # Changing all the letters in Expression to lowercases

        # Creating unique key for the dictionary by joining audltID, distance and expression columns
        unique_key = line[title.index("id")]+"&"+line[title.index("distance")]+"&"+line[title.index("expression")]
        unique_key_list.append(unique_key)
        # Finding the corresponing Gdis and Ldis as values in dictionary
        values = [float(line[title.index("gdis")]), float(line[title.index("ldis")])]
        # Creating a dictionary
        indiv_dict[unique_key] = values 

    return indiv_dict, unique_key_list

def adultkey(indivdata, adultID):       # To find the input adultID key for the dictionary 
    
    adult_key_list = []
    adultID = adultID
    expressionList = ["neutral", "angry", "disgust", "happy"]
    distanceList = ["1","2","3","4","5","6","7","8"]
    
    # Combining adultID, distance and expression to create adultID key
    for distance in distanceList:
        ID_distance = adultID + "&" + distance

        for expression in expressionList:
            adult_key = ID_distance + "&" + expression
            adult_key_list.append(adult_key)
    
    return adult_key_list

def extract_data(indivdata, adultID):   # To extract Gdis and Ldis from dictionary for (i)input adultID and (ii)remaining adultID in data file
    indiv_dict, unique_key_list = create_dictionary(indivdata)
    adult_key_list = adultkey(indivdata, adultID)
    indiv_dict_key_list = list(indiv_dict.keys())
    data_list = []
    other_ID_data_list = []
    other_ID_key_list = []
    
    for adult_key in adult_key_list:
        if adult_key in indiv_dict_key_list:
            data = indiv_dict[adult_key]
            
            # If Gdis or Ldis are negative or 0, replace with 50.0 (as floats format)
            if data[0] <= 0:
                data[0] = 50.0
            if data[1] <= 0:
                data[1] = 50.0

            data_list.append(data)                 # A list contains all the Gdis and Ldis for the input adultID
            
    Gdis_list = [Gdis[0] for Gdis in data_list]    # A list contains all the Gdis for the input adultID
    Ldis_list = [Ldis[1] for Ldis in data_list]    # A list contains all the Ldis for the input adultID
    
    for key in unique_key_list:           # Finding all the remaining adultID in data file except for input adultID
        if key not in adult_key_list:
            other_ID_key = key
            other_ID_data = indiv_dict[key]
            
            # If Gdis or Ldis are negative or 0, replace with 50.0 (as floats format)
            if other_ID_data[0] <= 0:
                other_ID_data[0] = 50.0
            if other_ID_data[1] <= 0:
                other_ID_data[1] = 50.0

            other_ID_data_list.append(other_ID_data) # A list contains all the Gdis and Ldis for other adultID (except input adultID)
            other_ID_key_list.append(other_ID_key)   # A list contains all the adultID in data file, except input adultID

    other_ID_Gdis_list = [Other_Gdis[0] for Other_Gdis in other_ID_data_list]  # A list contains all the Gdis for the other adultID
    
    return data_list, Gdis_list, Ldis_list, other_ID_Gdis_list, other_ID_key_list

def OP1(indivdata, adultID):     # To calculate the result for OP1
    data_list, Gdis_list, Ldis_list, other_ID_Gdis_list, other_ID_key_list = extract_data(indivdata, adultID)
 
    OP1_result = []
    
    # To extract the max and min Gdis and Ldis 
    for i in range (8):          # Looping in the 8 locations
        lowerindex = 4 * i
        upperindex = 4 * (1+i)
        
        # Finding max & min Gdis and Ldis from 4 expression in every location
        Gdis_min = round(min(Gdis_list[lowerindex:upperindex]),4)   
        Gdis_max = round(max(Gdis_list[lowerindex:upperindex]),4)   
        Ldis_min = round(min(Ldis_list[lowerindex:upperindex]),4)   
        Ldis_max = round(max(Ldis_list[lowerindex:upperindex]),4)   
        
        OP1_result.append([Gdis_min, Gdis_max, Ldis_min, Ldis_max])
        
    return OP1_result

def OP2(indivdata, adultID):       # To calculate the result for OP2
    data_list, Gdis_list, Ldis_list, other_ID_Gdis_list, other_ID_key_list = extract_data(indivdata, adultID)
    
    OP2_result = []
      
    for i in range (4):       # Looping in 4 expressions
        Dis1 = i
        Dis2 = Dis1 + 4
        Dis3 = Dis2 + 4
        Dis4 = Dis3 + 4
        Dis5 = Dis4 + 4
        Dis6 = Dis5 + 4
        Dis7 = Dis6 + 4
        Dis8 = Dis7 + 4
        
        # Calculate the difference in Gdis and Ldis from 8 location in each expression
        Dis1_diff = round(Gdis_list[Dis1] - Ldis_list[Dis1],4)   
        Dis2_diff = round(Gdis_list[Dis2] - Ldis_list[Dis2],4)
        Dis3_diff = round(Gdis_list[Dis3] - Ldis_list[Dis3],4)
        Dis4_diff = round(Gdis_list[Dis4] - Ldis_list[Dis4],4)
        Dis5_diff = round(Gdis_list[Dis5] - Ldis_list[Dis5],4)
        Dis6_diff = round(Gdis_list[Dis6] - Ldis_list[Dis6],4)
        Dis7_diff = round(Gdis_list[Dis7] - Ldis_list[Dis7],4)
        Dis8_diff = round(Gdis_list[Dis8] - Ldis_list[Dis8],4)
        
        OP2_result.append([Dis1_diff, Dis2_diff, Dis3_diff, Dis4_diff, Dis5_diff, Dis6_diff, Dis7_diff, Dis8_diff])
   
    return OP2_result

def OP3(indivdata, adultID):        # To calculate the result for OP3
    data_list, Gdis_list, Ldis_list, other_ID_Gdis_list, other_ID_key_list = extract_data(indivdata, adultID)
    
    OP3_result = []
    
    for i in range (8):          # Looping in the 8 locations
        lowerindex = 4 * i
        upperindex = 4 * (1+i)
        
        # Calculating average Gdis across 4 expression in every location
        Dis_avg = round(sum(Gdis_list[lowerindex:upperindex])/4,4)
        
        OP3_result.append(Dis_avg)
    
    return OP3_result

def OP4(indivdata, adultID):        # To calculate the result for OP4
    data_list, Gdis_list, Ldis_list, other_ID_Gdis_list, other_ID_key_list = extract_data(indivdata, adultID)
    
    OP4_result = []
    
    for i in range (8):             # Looping in the 8 locations
        lowerindex = 4 * i
        upperindex = 4 * (1 + i)
        Dis_sd_numerator = 0
        
        # Calculating the numerator in SD formula
        for n in range (4):         # Looping in 4 expressions
            Dis_sd_numerator = (Ldis_list[n + 4 * i] - (sum(Ldis_list[lowerindex:upperindex])/4)) ** 2 + Dis_sd_numerator

        Dis_sd = round((Dis_sd_numerator/4) ** 0.5,4)  # Calculating the SD
        OP4_result.append(Dis_sd)
    
    return OP4_result

def cossim_sameID(indivdata, adultID):    # To calculate max cossim among different expression in input adultID
    data_list, Gdis_list, Ldis_list, other_ID_Gdis_list, other_ID_key_list = extract_data(indivdata, adultID)
    same_id_netural_Gdis_list = []
    same_id_angry_Gdis_list = []
    same_id_disgust_Gdis_list = []
    same_id_happy_Gdis_list = []
    
    for i in range (8):            # Looping in 8 locations
        netural_index = 4 * i
        same_id_netural_Gdis = Gdis_list[netural_index]
        same_id_netural_Gdis_list.append(same_id_netural_Gdis)  #  A list contains Gdis in Netural for input adultID
    
        angry_index = 4 * i + 1
        same_id_angry_Gdis = Gdis_list[angry_index]
        same_id_angry_Gdis_list.append(same_id_angry_Gdis)      #  A list contains Gdis in Angry for input adultID

        disgust_index = 4 * i + 2
        same_id_disgust_Gdis = Gdis_list[disgust_index]
        same_id_disgust_Gdis_list.append(same_id_disgust_Gdis)  #  A list contains Gdis in Disgust for input adultID
    
        happy_index = 4 * i + 3
        same_id_happy_Gdis = Gdis_list[happy_index]
        same_id_happy_Gdis_list.append(same_id_happy_Gdis)      #  A list contains Gdis in Happy for input adultID

    cosine_NA_numerator = 0
    cosine_ND_numerator = 0
    cosine_NH_numerator = 0
    cosine_N_denominator = 0
    cosine_A_denominator = 0
    cosine_D_denominator = 0
    cosine_H_denominator = 0
    
    # Calculating the cossim on Gdis between Netural and other expression for input adultID
    for n in range (8):   # Looping in 8 locations
        cosine_NA_numerator = same_id_netural_Gdis_list[n] * same_id_angry_Gdis_list[n] + cosine_NA_numerator
        cosine_ND_numerator = same_id_netural_Gdis_list[n] * same_id_disgust_Gdis_list[n] + cosine_ND_numerator
        cosine_NH_numerator = same_id_netural_Gdis_list[n] * same_id_happy_Gdis_list[n] + cosine_NH_numerator
        cosine_N_denominator = same_id_netural_Gdis_list[n] ** 2 + cosine_N_denominator
        cosine_A_denominator = same_id_angry_Gdis_list[n] ** 2 + cosine_A_denominator
        cosine_D_denominator = same_id_disgust_Gdis_list[n] ** 2 + cosine_D_denominator
        cosine_H_denominator = same_id_happy_Gdis_list[n] ** 2 + cosine_H_denominator
        
    cosine_NA_denominator = (cosine_N_denominator ** 0.5) * (cosine_A_denominator ** 0.5)
    cosine_ND_denominator = (cosine_N_denominator ** 0.5) * (cosine_D_denominator ** 0.5)
    cosine_NH_denominator = (cosine_N_denominator ** 0.5) * (cosine_H_denominator ** 0.5)
    
    # Rounding the cossim values calculated to 4 d.p.
    cosine_NA = round(cosine_NA_numerator / cosine_NA_denominator,4)
    cosine_ND = round(cosine_ND_numerator / cosine_ND_denominator,4)
    cosine_NH = round(cosine_NH_numerator / cosine_NH_denominator,4)
    
    # Find the max cossim from the cossim calculated between Netural and other expression for input adultID
    max_cossim_sameID = max(cosine_NA, cosine_ND, cosine_NH)
    
    return max_cossim_sameID, same_id_netural_Gdis_list

def cossim_max(indivdata, adultID):      # To calculate cossim on Netural expression between input adultID to other adultID, search for max cossim and corresponding adultID
    data_list, Gdis_list, Ldis_list, other_ID_Gdis_list, other_ID_key_list = extract_data(indivdata, adultID)
    max_cossim_sameID, same_id_netural_Gdis_list = cossim_sameID(indivdata, adultID)
    
    otherID_netural_number = int(len(other_ID_Gdis_list)/32)  # Calculating the number of other adultID in data file (except input adultID)
    otherID_netural_Gdis_list = []

    for i in range(otherID_netural_number):  # Looping in every other adultID
        lowerindex = 32 * i
        upperindex = lowerindex + 8
        
        otherID_netural_Gdis = other_ID_Gdis_list[lowerindex:upperindex]
        otherID_netural_Gdis_list.append(otherID_netural_Gdis)    # A list contains Gdis in Netural for all other adultID
    
    cosine_N_diffID_numerator = 0
    cosine_N_denominator = 0
    cosine_N_otherID_denominator = 0
    cosine_N_diffID_numerator_list = []
    cosine_N_denominator_list = []
    cosine_N_otherID_denominator_list = []
    cosine_N_diffID_list = []
    
    # Calculating the cossim on Netural expression between input adultID to other adultID
    for i in range (otherID_netural_number):  # Looping in every other adultID
        otherID_netural_Gdis_list_extract = otherID_netural_Gdis_list[i][0:8]
        cosine_N_diffID_numerator = 0
        cosine_N_denominator = 0
        cosine_N_otherID_denominator = 0
        for n in range (8):   # Looping in every location
            cosine_N_diffID_numerator = same_id_netural_Gdis_list[n] * otherID_netural_Gdis_list_extract[n] + cosine_N_diffID_numerator
            cosine_N_denominator = same_id_netural_Gdis_list[n] ** 2 + cosine_N_denominator
            cosine_N_otherID_denominator = otherID_netural_Gdis_list_extract[n] ** 2 + cosine_N_otherID_denominator 
          
        cosine_N_diffID_numerator_list.append(cosine_N_diffID_numerator)
        cosine_N_denominator_list.append(cosine_N_denominator)
        cosine_N_otherID_denominator_list.append(cosine_N_otherID_denominator)
    
    for i in range (otherID_netural_number):  # Looping in every other adultID
        cosine_N_diffID_denominator = (cosine_N_denominator_list[i] ** 0.5) * (cosine_N_otherID_denominator_list[i] ** 0.5)
        cosine_N_diffID = round(cosine_N_diffID_numerator_list[i] / cosine_N_diffID_denominator,4)
        cosine_N_diffID_list.append(cosine_N_diffID)

    # Finding the max cossim from all cossim calculated on Netural expression between input adultID to other adultID
    max_cossim_diffID = max(cosine_N_diffID_list)

    # Finding the max cossim between max cossim in same adultID comparision and diff adultID comparision
    max_cossim = max(max_cossim_diffID, max_cossim_sameID)
    
    # Finding the reference ID for max cossim
    if max_cossim == max_cossim_sameID:
        ref_adultID = adultID
    else:
        max_cosine_index = cosine_N_diffID_list.index(max_cossim_diffID)
        max_adultID_index = (max_cosine_index + 1) * 32
        ref_adultID_key = other_ID_key_list[max_adultID_index-1]
        ref_adultID_key_list = ref_adultID_key.split("&")
        ref_adultID = ref_adultID_key_list[0]
    
    return ref_adultID, max_cossim

# End of the program
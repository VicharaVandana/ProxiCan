#inputs for security access
#input 1 : The subfunction for request seed (subfunction for validate key will be +1)
#input 2 : Length of seed and key for security level
#input 3 : logic of computing key from seed

def getKey4mSeed_SecuLvl_01(seed):
    #Update the code between start and end section only
    ################# START ########################
    #Logic: Key is 2's complement of the seed 
    ones_complement = ~seed
    twos_complement = ones_complement + 1
    key = 0xFFFF & twos_complement
    ################## END #########################
    return(key)

def getKey4mSeed_SecuLvl_31(seed):
    #Update the code between start and end section only
    ################# START ########################
    #Logic: Key is ORed operation of the seed high bite and low byte
    oredval = (seed >> 8) | (seed & 0xFF)
    key = 0xFF & oredval
    ################## END #########################
    return(key)
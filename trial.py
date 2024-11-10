import json

# Retrieve the code from QTextEdit
function_code2 = """
def getKey4mSeed_SecuLvl_01(seed):
    # Logic: Key is 2's complement of the seed 
    ones_complement = ~seed
    twos_complement = ones_complement + 1
    key = 0xFFFF & twos_complement
    return key
"""

function_code = """def SecurityFunction(seed):
    # Logic to compute key from seed in python
    # START OF LOGIC 
    #Enter your python code here
    key = seed  #to be replaced with actual logic
    # END OF LOGIC
    return key
"""

# Serialize the code to JSON
function_json = json.dumps({"SecurityFunctionDefinition": function_code})

# Save to JSON file (optional)
with open('function_data.json', 'w') as f:
    f.write(function_json)

# Load and execute the function from JSON
with open('function_data.json', 'r') as f:
    function_data = json.load(f)

exec(function_data["SecurityFunctionDefinition"])

# Test the function
result = SecurityFunction(0x1234)
print("Result:", result)

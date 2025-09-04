import os   
import pandas as pd
def find_number_in_file(file_name, number_to_find):
    try:
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(script_dir, file_name)
        with open(file_path, 'r') as file:
            for line in file:
                columns = line.split() 
                if columns and columns[0] == str(number_to_find):
                    print(f"Found {number_to_find} in file {file_name}: {line.strip()}")
                    
                    return line
        return None
    except FileNotFoundError:
        return f"Error: File {file_name} not found."  
    except Exception as e:
        return f"An error occurred: {e}"
    
def ORB_EL_printer(mount,ast):
    number_to_find=ast
    ans=mount
    if ans=='10Micron':
        file_name='mpcorb_df.pkl'
        num=number_to_find
        for i in range(5-len(number_to_find)):
            num='0'+num
        print(num,type(num))
        file_name =  "mpcorb_df.pkl"
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(script_dir, file_name)
        local_asteroids_df = pd.read_pickle(file_path)
            
        match = local_asteroids_df[local_asteroids_df['designation_packed'] == num]
        
               
        print(type(match))
        print(match)
        if not match.empty:
                row = match.iloc[0]
                result_line = ' '.join([str(val) for val in row.values])
                print(f"Found {number_to_find} in file {file_name}")
                return f"Orbital Elements: {result_line}"
        else:
                return f"Number {number_to_find} not found in MPCORB database." 
    elif ans=='PlaneWave4':
        file_name='astorb.dat'
        num=number_to_find
        result=find_number_in_file(file_name, num)

    if result:
        return f"Orbital Elements:{result}"
    else:
       return f"Number {number_to_find} not found in the first column of the file."
   
   
if __name__== "__main__" :
    mount="PlaneWave4"
    mount ="10Micron"
    ast ="39796"
    result = ORB_EL_printer(mount,ast)
    print(result)

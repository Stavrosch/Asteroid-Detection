import os   

def find_number_in_file(file_name, number_to_find):
    try:
        # Get the directory of the current script and save file in the current script.
        script_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(script_dir, file_name)

        with open(file_path, 'r') as file:
            for line in file:
                columns = line.split() # Adding a collumn split.
                if columns and columns[0] == str(number_to_find):
                    return line
        return None
    except FileNotFoundError:
        return f"Error: File {file_name} not found."  
    except Exception as e:
        return f"An error occurred: {e}"
    
def TLE_printer(mount,ast):
    number_to_find=ast
    ans=mount
    if ans=='10Micron':
        file_name='MPCORB.dat'
        num=number_to_find
        for i in range(5-len(number_to_find)):
            num='0'+num
        result=find_number_in_file(file_name, num)
    elif ans=='PlaneWave4':
        file_name='astorb.dat'
        num=number_to_find
        result=find_number_in_file(file_name, num)

    if result:
        return f"Line found:{result}"
    else:
       return f"Number {number_to_find} not found in the first column of the file."
   
   
if __name__== "__main__" :
    mount="PlaneWave4"
    mount1 ="10Micron"
    ast ="39796"
    result = TLE_printer(mount,ast)
    print(result)

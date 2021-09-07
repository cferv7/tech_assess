import pandas as pd
import os
import json
import yaml
import csv


def file_converter(file, o_type):
    """
    Description: This function takes a file with extension of CSV, JSON, YML and converts it
    into anyone of those file types (json, csv, yaml, yml)
    if the input file exension and output type is the same, will write to file anwyway
    NOTE: The file in question has to be in the same directory as this program

    Arguments:
        file: the name of file with ext 
        o_type: 'json', 'csv', 'yaml', 'yml'
    
    Return: print stmt of job status and based on input, a file written to current directory
    """

    # takes filepath breaks to filename and file ext
    split_tup = os.path.splitext(file)
    file_name = split_tup[0]
    file_extension = split_tup[1]
    
    file_extension = file_extension.lower().rstrip()
    o_type = o_type.lower().rstrip()

    # input checks
    if file_extension not in ['.csv', '.json', '.yml', '.yaml']:
        print("Sorry, file extension not supported.")
    
    elif o_type not in ['csv','json', 'yml', 'yaml']:
        print("Sorry, output file not supported.")
    
    else:
        if file_extension == '.csv':
            if o_type == 'json':
                df = pd.read_csv(file)
                df.to_json('{}.json'.format(file_name), orient='records')

            elif o_type == 'csv':
                df = pd.read_csv(file)
                df.to_csv('{}_1.csv'.format(file_name), index=False)
                
            elif o_type == 'yml' or 'yaml':
                with open(file) as f_csv:       
                    csvFile = csv.reader(f_csv)        
                    header = next(csvFile) # obtain columns
                    rest = list(csvFile) # convert the rest of data into a list

                row_length = len(rest)
                
                # turn the csv into a list_of_dict format to match yml format
                full_text = []
                for row in range(row_length):
                    # perform dict_comprehension while converting numeric values from string to int
                    res = { header[i]: 
                           (int(rest[row][i]) if rest[row][i].isnumeric() else rest[row][i]) 
                               for i in range(len(header)) }
                    full_text.append(res)
                
                # then writes to a yml file
                with open('{}.yml'.format(file_name), 'w') as f:
                    yaml.dump(full_text, f, sort_keys=False) # disable sort
    
        elif file_extension == '.json': 
            if o_type == 'csv':
                df = pd.read_json(file)
                df.to_csv('{}.csv'.format(file_name), index=False)

            elif o_type == 'json':
                with open(file) as json_file:
                    data = json.load(json_file)
                df = pd.DataFrame.from_dict(data)
                df.to_json('{}_1.json'.format(file_name), orient='records')
                
            elif o_type == 'yml' or 'yaml':
                with open(file) as json_file:
                    data = json.load(json_file)
                with open('{}.yml'.format(file_name), 'w') as f:
                    yaml.dump(data, f, sort_keys=False) # disable sort
        
        elif file_extension == '.yml' or '.yaml':
            if o_type == 'json':
                # open yaml file, turn into json string, then write to json file 
                with open(file) as f_yaml:
                    json_storage = json.dumps(yaml.load(f_yaml, Loader=yaml.FullLoader))
                with open('{}.json'.format(file_name), 'w') as f_json:
                    f_json.write(json_storage)
            
            elif o_type == 'csv':  
                
                with open(file) as f_yml:
                    lines = yaml.full_load(f_yml)
                
                fields = [] # stores header
                data = [] # store rows
                
                # taking csv data formatting into yaml (list of dicts)
                for line in lines: 
                    row = []
                    for key, value in line.items():
                        if key not in fields:
                            fields.append(key)
                        row.append(value)
                    data.append(row)
                
                with open('{}.csv'.format(file_name), 'w', newline='') as f_csv:
                    csvwriter = csv.writer(f_csv) # creates a csv writer object 
                    csvwriter.writerow(fields) # writes the fields                     
                    csvwriter.writerows(data) # writes the data rows 
            
            elif o_type == 'yml' or o_type == 'yaml':
                with open(file) as f_yaml:
                    data = yaml.load(f_yaml, Loader=yaml.FullLoader)
    
                with open('{}_1.yml'.format(file_name), 'w') as f:
                    yaml.dump(data, f, sort_keys=False) # disable sort

        print("Task Completed.")    


if __name__ == "__main__":
    # asks user to input filename and output type via terminal
    filename = input("Please enter the filename: ")
    output_type = input("Please pick a format to write the file to: csv, json, yaml? ")

    file_converter(filename, output_type)

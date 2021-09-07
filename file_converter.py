import pandas as pd
import os
import json
import csv


def file_converter(file, o_type):
    """
    Description: This function takes a CSV file and converts it into a JSON file and vice-versa,
    if the input file exension and output type is the same, will write to file anwyway
    NOTE: The file in question has to be in the same directory as this program

    Arguments:
        file: the name of file with ext 
        o_type: 'json' or 'csv'
    
    Return: print stmt of job status and based on input, a file written to current directory
    """

    # takes filepath breaks to filename and file ext
    split_tup = os.path.splitext(file)
    file_name = split_tup[0]
    file_extension = split_tup[1]

    file_extension = file_extension.lower().rstrip()
    o_type = o_type.lower().rstrip()
    
    # input checks
    if file_extension not in ['.csv', '.json']:
        print("Sorry, file extension not supported.")
    
    elif o_type not in ['csv','json']:
        print("Sorry, output file not supported.")
    
    else:
        if file_extension == '.csv':
            if o_type == 'json':
                df = pd.read_csv(file)
                df.to_json('{}.json'.format(file_name), orient='records')

            elif o_type == 'csv':
                df = pd.read_csv(file)
                df.to_csv('{}_1.csv'.format(file_name), index=False)
    
        elif file_extension == '.json': 
            if o_type == 'csv':
                df = pd.read_json(file)
                df.to_csv('{}.csv'.format(file_name), index=False)

            elif o_type == 'json':
                with open(file) as json_file:
                    data = json.load(json_file)
                df = pd.DataFrame.from_dict(data)
                df.to_json('{}_1.json'.format(file_name), orient='records')    

        print("Task Completed.")    


if __name__ == "__main__":
    # asks user to input filename and output type via terminal
    filename = input("Please enter the filename: ")
    output_type = input("Please pick a format to write the file to: csv or json? ")

    file_converter(filename, output_type)

import csv
import os
from collections import Counter # to remove duplicates
from tabulate import tabulate # formatting purposes


# Parameters to modify
station_X = "SST114"
model = "SST02"

# Parameters that might need modification if needed
csv_path = "csv_folder"
csvfile_name_X = "csv_" + station_X + ".csv"
csvfile_name_model = "csv_" + model + ".csv"
txt_name = f"results model {model} with {station_X}.txt"
delimiter_ = ";"

# Initialization of lists
dwg_no_X = []
dwg_no_model = []

def read_csv (csv_path, csvfile_name, dwg_no):
    """
    Reads DWG. No. from a CSV file and appends them to a list.
    
    Args:
        csv_path (str): Path to the folder containing the CSV file.
        csvfile_name (str): Name of the CSV file to read.
        dwg_no (list): List to append DWG. No. to.

    Returns:
        list: Updated list containing DWG. No.
    """    
    with open(os.path.join(csv_path, csvfile_name)) as file:
        reader = csv.DictReader(file, delimiter=delimiter_)
        for row in reader:
            dwg_no.append(row['DWG. No.'])
    return dwg_no


def get_duplicates(dwg_no):
    """
    Identifies duplicate DWG. No. in the provided list.
    
    Args:
        dwg_no (list): List of DWG. No. to check for duplicates.

    Returns:
        dict: A dictionary where keys are duplicate DWG. No. and values are counts of occurrences.
    """
    duplicates_count = Counter(dwg_no)
    duplicates = {item: count for item, count in duplicates_count.items() if count > 1}
    return duplicates


def get_data(dwg_no, station):
    """
    Extracts sector numbers and project numbers from DWG. No. and returns them.
    
    Args:
        dwg_no (list): List of DWG. No. to extract data from.
        station (str): Station identifier for logging.

    Returns:
        tuple: A tuple containing two lists - sector numbers and project numbers.
    """
    sector_no = []
    project_no = []
    for dwg in dwg_no:
        sector_no.append(dwg[6:])
        project_no.append(dwg[:6])
    project_no = list(set(project_no))
    if len(project_no) < 2:
        project_no = project_no[0]
    else:
        print(f"There are different project numbers in station {station}: {project_no}" )
    return sector_no, project_no


def compare(sector_no_model, sector_no_X):
    """
    Compares sector numbers between the model and station X, identifying differences and commonalities.
    
    Args:
        sector_no_model (list): Sector numbers from the model.
        sector_no_X (list): Sector numbers from station X.

    Returns:
        tuple: Three lists - sector numbers not found in station X, not found in model, and common to both.
    """
        # Find elements in model but not in station X
    sector_not_found_in_X = list(set(sector_no_model) - set(sector_no_X))
        # Find elements in station X but not in model
    sector_not_found_in_model = list(set(sector_no_X) - set(sector_no_model))
        # Find elements in both model and station X
    sector_common = list(set(sector_no_X) & set(sector_no_model))
    return sector_not_found_in_X, sector_not_found_in_model, sector_common


def recuperate_dwg_no(sector_not_found, project_no):
    """
    Constructs DWG. No. for sectors not found based on project numbers.
    
    Args:
        sector_not_found (list): List of sector numbers not found.
        project_no (list): List of project numbers.

    Returns:
        list: A list of DWG. No. that were not found.
    """
    dwg_not_found = []
    for sector in sector_not_found:
        dwg_not_found.append(project_no + sector)
    return dwg_not_found
    

def get_description(csvfile_name, dwg_not_found):
    """
    Retrieves drawing descriptions for specified DWG. No. from a CSV file.

    Args:
        csvfile_name (str): Name of the CSV file to read.
        dwg_not_found (list): List of DWG. No. for which descriptions are required.

    Returns:
        dict: A dictionary where the keys are DWG. No. and the values are their corresponding drawing descriptions.
    """
    drawings = {}
    with open(os.path.join(csv_path, csvfile_name), encoding='utf-8-sig',newline='') as file:
        reader = csv.DictReader(file, delimiter=delimiter_)
        for row in reader:
            
            if row['DWG. No.'] in dwg_not_found:
                drawings[row['DWG. No.']] = row['DRAWING DESCRIPTION']

   
    return drawings


def output(station_X, model, duplicates, sector_not_found_in_X,sector_not_found_in_model, sector_common,drawings_model,drawings_X):
    """
    Writes the comparison results to a text file.
    
    Args:
        station_X (str): Station identifier.
        model (str): Model identifier.
        duplicates (dict): Dictionary of duplicate DWG. No. and their counts.
        sector_not_found_in_X (list): Sector numbers in the model but not in station X.
        sector_not_found_in_model (list): Sector numbers in station X but not in the model.
        sector_common (list): Sector numbers common to both station X and the model.
        drawings_model (dict): Drawing descriptions from the model for DWG. No. not found in station X.
        drawings_X (dict): Drawing descriptions from station X for DWG. No. not found in the model.
    """
    with open (txt_name, "w") as txtfile:
        txtfile.write(f"These are the DWG.No. that are duplicated in station {station_X}:\n\n")
        txtfile.write(tabulate(duplicates.items(), headers=["DWG. No.", "Occurences"], stralign='center'))
        txtfile.write("\n\n")
        txtfile.write('Sector Results:\n\n')
        txtfile.write(tabulate({
        f"Not found in station {station_X}":sorted(sector_not_found_in_X), 
        f"Not found in model {model}":sorted(sector_not_found_in_model),
        f"Common in both station {station_X} and model {model}": sorted(sector_common)
        }, headers='keys',stralign='center'))

        txtfile.write(f"\n\nDrawings not found in station {station_X} but are in model {model}:\n\n")
        txtfile.write(tabulate(sorted(drawings_model.items()), headers=["DWG. No.", "DRAWING DESCRIPTION"], stralign='center'))

        txtfile.write(f"\n\nDrawings not found in model {station_X} but are in station {station_X}:\n\n")
        txtfile.write(tabulate(sorted(drawings_X.items()), headers=["DWG. No.", "DRAWING DESCRIPTION"], stralign='center'))



def main():
    """
    Main function to orchestrate the reading, processing, comparison, and output of drawing data.
    """
    global dwg_no_model, dwg_no_X
    dwg_no_X = read_csv(csv_path, csvfile_name_X, dwg_no_X)
    dwg_no_model = read_csv(csv_path, csvfile_name_model, dwg_no_model)
    duplicates = get_duplicates(dwg_no_X)
    sector_no_X, project_no_X = get_data(dwg_no_X, station_X)
    sector_no_model, project_no_model = get_data(dwg_no_model, model)
    sector_not_found_in_X, sector_not_found_in_model, sector_common = compare(sector_no_model, sector_no_X)
    dwg_not_found_in_X = recuperate_dwg_no(sector_not_found_in_X, project_no_model)
    dwg_not_found_in_model = recuperate_dwg_no(sector_not_found_in_model, project_no_X)
    drawings_X = get_description(csvfile_name_X, dwg_not_found_in_model)
    drawings_model = get_description(csvfile_name_model, dwg_not_found_in_X)
    output(station_X, model, duplicates, sector_not_found_in_X,sector_not_found_in_model, sector_common,drawings_model,drawings_X)
    
    

if __name__ == "__main__":
  main()





    

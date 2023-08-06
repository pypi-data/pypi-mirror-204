from PIL import Image
import os
import numpy as np
import traceback
from .utils import *


def imagesToThermals(input_dir:str,output_dir:str=None,iterate_recursive:bool=False,sep:str=','):
    """
    Docstring:
    Read images from input directory path and save it into output path.

    Parameters
    ----------
    input_dir : str, path object or file-like object
        Any valid string path is acceptable.
        It should contain radiometric files in the directory
        
    output_dir : str, path object or file-like object
        Any valid string path is acceptable.
        If directory not present it will be created
        output_dir=None then ouput will be generated in the input_dir it self.
        
    iterate_recursive : boolean, True or Flase
        True: recursively iterate through input_dir and search for image files in sub directory
        False: retrive files from current directory only
        
    sep : str, default ','
        Delimiter to use. It will be used as seperate in csv file.
        e.g. , | # ;


    Returns
    -------
    numpy nd array object
        A numpy array object is returned as two-dimensional data structure.

    Examples
    --------
    >>> import hitthermal as ht
    >>> ht.imagesToThermals(input_dir='/user/image/',output_dir=None,iterate_recursive=False,sep:str=',')
    Type:      function

    """

    file_extension = 'csv'
    var_supported_file_extension = [".jpg",".jpeg"]

    if output_dir == None:
        output_dir = input_dir
    
    all_files = []
    # Iterate using folder name
    source_path=input_dir
    # print('\nwalk_dir (absolute) = ' + os.path.abspath(source_path))
    if iterate_recursive:
        for root, subdirs, files in os.walk(source_path):
            for filename in files:
                if any(filename.lower().endswith(x) for x in var_supported_file_extension):
                    file_path = os.path.join(root, filename)
                    all_files.append(file_path)
    else:
        for filename in os.listdir(source_path):
            if any(filename.lower().endswith(x) for x in var_supported_file_extension):
                    file_path = os.path.join(source_path, filename)
                    all_files.append(file_path)

    
    var_total_file_count = len(all_files)
    
    rejected_file_count=0
    for i,rjpeg_image_path in enumerate(all_files):
        try:
            output_file_save_dir = None
            if input_dir == output_dir:
                output_file_save_dir = os.path.normpath(os.path.dirname(rjpeg_image_path))
            else:
                recursive_directory_part = os.path.normpath(os.path.dirname(rjpeg_image_path)).replace(os.path.normpath(input_dir),'')
                recursive_directory_part = trimForwardBackwardSlashFromStartOfDir(recursive_directory_part)
                output_file_save_dir = os.path.join(output_dir,recursive_directory_part)

            splitted_file_name = os.path.basename(rjpeg_image_path).split('.')
            splitted_file_name[-1]=file_extension            
            temperature_file_name = '.'.join(splitted_file_name)
            temperature_file_path = os.path.join(output_file_save_dir,temperature_file_name)
            checkIfDirExistElseCreate(temperature_file_path)

            tempArray = convertRjpegToTemperature(rjpeg_image_path)
            _=np.savetxt(temperature_file_path, tempArray, delimiter=sep, fmt='%.2f')

            var_processed_file_count = i+1-rejected_file_count

        except Exception as ex:
            #TODO: display rejected  
            print("Error Update:")
            rejected_file_count+=1
            traceback.print_exc()

def convertRjpegToTemperature(file_path:str) -> np.array:
    img = Image.open(file_path)
    
    raw_file = None
    with open(file_path, "rb") as image:
        raw_file = image.read()
    
    step_size = 1
    ImageWidth= img.size[0]
    ImageHeight= img.size[1]
    value_sep=","
    
    # decode byte stream
    decoded_file = []
    for i in range(0,len(raw_file),1):
        decoded_file.append(bytes_to_uint(raw_file[i:i+1]))

    # raw_file
    start_sequence = [255,217,240,0]
    end_sequence = [240,0,64,1]
    
    check_upto_bytes = 4
    
    start_end_index=[]
    
    # find temperature data start and end index
    for i in range(0,len(decoded_file),1):
        if decoded_file[i:i+check_upto_bytes] == start_sequence:
            #print('start:',i+check_upto_bytes)
            start_end_index.append(i+check_upto_bytes)
        if decoded_file[i:i+check_upto_bytes] == end_sequence:
            #print('end:',i-1)
            start_end_index.append(i-1)
    
    start_index=None
    end_index=None
    found_match=False
    
    temperature_data = []
    # save temperature data to sperate file
    # check condition if multiple match of start and end sequence found and if the range is same as for the size of the image * 2 as decimal are stored seperately
    if len(start_end_index)==2 and ((start_end_index[-1]-start_end_index[0]-1)==ImageWidth*ImageHeight*2):
        #print("Start and End index")
        start_index = start_end_index[0]
        end_index = start_end_index[-1]
        found_match=True
    # if found multiple pattern but the start index and end index matches with the size of the image required then proceed
    elif len(start_end_index)>2 and ((start_end_index[-1]-start_end_index[0]-1)==ImageWidth*ImageHeight*2):
        #print("Multiple start and end index found and processing with first and last instance")
        start_index = start_end_index[0]
        end_index = start_end_index[-1]
        found_match=True
    # fall back check with four index
    else:
        raise Exception("Unable to convert file")
    
    if found_match:
        for i in range(start_index,end_index-1,2):
            temperature_data.append(float(str(decoded_file[i])+'.'+str(decoded_file[i+1])))

    temperature_array= np.array(temperature_data).reshape(ImageHeight,ImageWidth)
    
    assert temperature_array.shape[1] == img.size[0] and temperature_array.shape[0] == img.size[1]

    return temperature_array
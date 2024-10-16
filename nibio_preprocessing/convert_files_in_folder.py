import os
import argparse
from joblib import Parallel, delayed
from matplotlib import use
from tqdm import tqdm

# usie logging to print out the progress
import logging
logging.basicConfig(level=logging.INFO)


class ConvertFilesInFolder(object):
    def __init__(self, input_folder, output_folder, out_file_type, in_place=False, verbose=False):
        """
        There are following available file types:
        - las
        - laz
        - ply
        """
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.out_file_type = out_file_type
        self.in_place = in_place
        self.verbose = verbose

    def convert_file(self, file_path):
        """
        Convert a single file to the specified output file type.
        """
        # if the output folder doesn't exist, create it
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        # get the file name
        file_name = os.path.basename(file_path)
        # get the file name without extension
        file_name_no_ext = os.path.splitext(file_name)[0]
        # define the output file path
        output_file_path = os.path.join(self.output_folder, file_name_no_ext + "." + self.out_file_type)
        # define the command
        if output_file_path.split('.')[1] == "ply":
            command = "pdal translate -i {} -o {} --writers.ply.storage_mode='little endian'".format(file_path, output_file_path)
        else:
            command = "pdal translate -i {} -o {} --writers.las.forward=all".format(file_path, output_file_path)
        # command = 'pdal translate {} {} --writers.ply.storage_mode="little endian"'.format("/mnt/z/tobias/data_point2tree/docker/2_norm.laz", "/mnt/z/tobias/data_point2tree/docker/2_norm.ply")
        # run the command
        os.system(command)

        # use logging to print out the progress
        if self.verbose:
            logging.info("Converted {} to {}".format(file_path, output_file_path))


    # convert all files in the input folder
    def convert_files(self):
        """
        Convert all files in the input folder to the specified output file type.
        """
        # print if in_place is True
        if self.in_place:
            logging.info("Converting files in place.")

        # get paths to all files in the input folder and subfolders
        if self.verbose:
            print("Searching for files in the input folder...")

        file_paths = []
        for root, dirs, files in os.walk(self.input_folder):
            for file in files:
                file_paths.append(os.path.join(root, file))
        if self.verbose:
            # use logging to print out the progress
            logging.info("Found {} files.".format(len(file_paths)))

        # skip all the files that are not las or laz or ply
        file_paths = [f for f in file_paths if f.endswith(".las") or f.endswith(".laz") or f.endswith(".ply")]

        # skip all the files which are of type self.out_file_type
        file_paths = [f for f in file_paths if not f.endswith(self.out_file_type)]

        if self.verbose:
            # use logging to print out the progress
            logging.info("Found {} files that can be converted.".format(len(file_paths)))

        # iterate over all files and convert them

        for file_path in tqdm(file_paths):
            self.convert_file(file_path)

        # use joblib to speed up the process
        # Parallel(n_jobs=1)(delayed(self.convert_file)(file_path) for file_path in tqdm(file_paths))
        
        # print out the progress
        if self.verbose:
            # use logging to print out how many files were converted
            logging.info("Converted {} files.".format(len(file_paths)))

        # if in_place is True, delete all the original files
        if self.in_place:
            for file_path in tqdm(file_paths):
                os.remove(file_path)
            if self.verbose:
                # use logging to print out how many files were deleted
                logging.info("Deleted {} files.".format(len(file_paths)))
   

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_folder", help="Path to the folder with the files to convert.")
    parser.add_argument("--output_folder", help="Path to the folder where the converted files will be saved.")
    parser.add_argument(
        "--out_file_type", 
        default='ply', 
        help="The file type of the output files.There are following available file types: las, laz, ply"
        )
    parser.add_argument("--in_place", action="store_true", help="If set, the original files will be deleted.")
    parser.add_argument("--verbose", help="Print more information.", action="store_true")
    args = parser.parse_args()
    # create an instance of the class
    converter = ConvertFilesInFolder(
        args.input_folder, 
        args.output_folder, 
        args.out_file_type, 
        args.in_place,
        args.verbose
        )
    # convert all files in the input folder
    converter.convert_files()
    
      

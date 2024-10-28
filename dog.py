import os
import re
import subprocess

def merge_ts_files(input_folder, output_folder, min_file_size):
    # Get a list of all .ts files in the input folder
    ts_files = [f for f in os.listdir(input_folder) if f.endswith('.ts')]

    # Sort the .ts files in alphabetical order
    ts_files.sort()

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Delete files smaller than the minimum file size
    for ts_file in ts_files:
        ts_file_path = os.path.join(input_folder, ts_file)
        file_size = os.path.getsize(ts_file_path)
        
        if file_size < min_file_size:
            os.remove(ts_file_path)
            print(f"Deleted file '{ts_file}' due to small size.")

    # Update the list of .ts files after deleting small files
    ts_files = [f for f in os.listdir(input_folder) if f.endswith('.ts')]

    # Create a temporary file to store the list of valid .ts files
    temp_file = 'temp_file_list.txt'
    with open(temp_file, 'w') as file:
        for ts_file in ts_files:
            ts_file_path = os.path.join(input_folder, ts_file)
            file.write(f"file '{ts_file_path}'\n")

    # Get the base filename without numbers from the first .ts file
    base_filename = re.sub(r'\d+\.ts$', '', ts_files[0]).rstrip('-')
    output_filename = f"{base_filename}.mp4"

    # Use FFmpeg to merge the valid .ts files into a single video file
    output_path = os.path.join(output_folder, output_filename)
    subprocess.call(['ffmpeg', '-f', 'concat', '-safe', '0', '-i', temp_file, '-c', 'copy', output_path])

    # Remove the temporary file
    os.remove(temp_file)

    # Check if the merged video file exists
    if os.path.exists(output_path):
        print(f"Merged video file saved as: {output_path}")
        
        # Delete the valid .ts files
        for ts_file in ts_files:
            ts_file_path = os.path.join(input_folder, ts_file)
            os.remove(ts_file_path)
        
        print("Original valid .ts files deleted.")
    else:
        print("Merging failed. Merged video file not found.")

input_folder = 'raw'
output_folder = 'output'
min_file_size = 1024  # Minimum file size in bytes (1KB)
merge_ts_files(input_folder, output_folder, min_file_size)
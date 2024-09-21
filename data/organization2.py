import os
import shutil
import random

def split_dataset(dataset_dir, train_dir, test_dir, split_ratio=0.8):
    # Create train and test directories if they do not exist
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    # Iterate over each class folder
    for class_name in os.listdir(dataset_dir):
        class_dir = os.path.join(dataset_dir, class_name)
        if os.path.isdir(class_dir):
            # Create class subdirectories in train and test directories
            train_class_dir = os.path.join(train_dir, class_name)
            test_class_dir = os.path.join(test_dir, class_name)
            if not os.path.exists(train_class_dir):
                os.makedirs(train_class_dir)
            if not os.path.exists(test_class_dir):
                os.makedirs(test_class_dir)
            
            # List all files in the class directory
            files = os.listdir(class_dir)
            random.shuffle(files)
            
            # Split the files into train and test sets
            split_point = int(len(files) * split_ratio)
            train_files = files[:split_point]
            test_files = files[split_point:]
            
            # Copy files to train and test directories
            for file in train_files:
                src_file = os.path.join(class_dir, file)
                dest_file = os.path.join(train_class_dir, file)
                shutil.copy2(src_file, dest_file)
            
            for file in test_files:
                src_file = os.path.join(class_dir, file)
                dest_file = os.path.join(test_class_dir, file)
                shutil.copy2(src_file, dest_file)
    
    print("Dataset split completed.")

# Example usage
dataset_dir = r'C:\Users\ayabe\vs projects\data_teeth_brushing'
train_dir = r'C:\Users\ayabe\vs projects\new_data\train'
test_dir = r'C:\Users\ayabe\vs projects\new_data\test'
split_ratio = 0.8

split_dataset(dataset_dir, train_dir, test_dir, split_ratio)

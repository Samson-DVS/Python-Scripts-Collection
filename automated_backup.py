#Author: Visahl Samson David Selvam

import os
import shutil
import boto3
from datetime import datetime
from botocore.exceptions import NoCredentialsError

# AWS S3 Configuration
S3_BUCKET = 'your-s3-bucket-name'
S3_BACKUP_FOLDER = 'backups/'  # Folder in S3 where backups will be stored

# Local Directory Configuration
SOURCE_DIR = '/path/to/your/directory'  # Directory you want to backup
BACKUP_DIR = '/path/to/your/backup/folder'  # Temporary local backup storage

# Function to create a zipped backup
def create_backup(source_dir, backup_dir):
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    backup_file = os.path.join(backup_dir, f'backup_{timestamp}.zip')
    
    shutil.make_archive(backup_file.replace('.zip', ''), 'zip', source_dir)
    print(f"Backup created: {backup_file}")
    return backup_file

# Function to upload the backup to AWS S3
def upload_to_s3(file_name, bucket, s3_folder):
    s3 = boto3.client('s3')
    
    try:
        s3.upload_file(file_name, bucket, s3_folder + os.path.basename(file_name))
        print(f"Backup uploaded to S3: s3://{bucket}/{s3_folder}{os.path.basename(file_name)}")
    except FileNotFoundError:
        print("The file was not found.")
    except NoCredentialsError:
        print("Credentials not available.")

# Main function to execute backup and upload
def main():
    print("Starting backup process...")
    
    # Step 1: Create a backup of the specified directory
    backup_file = create_backup(SOURCE_DIR, BACKUP_DIR)
    
    # Step 2: Upload the backup to AWS S3
    upload_to_s3(backup_file, S3_BUCKET, S3_BACKUP_FOLDER)

if __name__ == '__main__':
    main()

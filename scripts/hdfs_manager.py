"""
HDFS file management utilities
"""
import subprocess
import argparse
from pathlib import Path


class HDFSManager:
    """Manager for HDFS operations"""
    
    def __init__(self):
        """Initialize HDFS manager"""
        self.hdfs_cmd = 'hdfs dfs'
    
    def run_command(self, command):
        """Execute HDFS command"""
        try:
            result = subprocess.run(
                f"{self.hdfs_cmd} {command}",
                shell=True,
                capture_output=True,
                text=True
            )
            
            return result.returncode == 0, result.stdout, result.stderr
            
        except Exception as e:
            return False, '', str(e)
    
    def upload_file(self, local_path, hdfs_path):
        """Upload file to HDFS"""
        print(f"📤 Uploading {local_path} to {hdfs_path}")
        
        success, stdout, stderr = self.run_command(
            f"-put {local_path} {hdfs_path}"
        )
        
        if success:
            print(f"✓ Upload successful")
        else:
            print(f"✗ Upload failed: {stderr}")
        
        return success
    
    def download_file(self, hdfs_path, local_path):
        """Download file from HDFS"""
        print(f"📥 Downloading {hdfs_path} to {local_path}")
        
        success, stdout, stderr = self.run_command(
            f"-get {hdfs_path} {local_path}"
        )
        
        if success:
            print(f"✓ Download successful")
        else:
            print(f"✗ Download failed: {stderr}")
        
        return success
    
    def list_directory(self, hdfs_path):
        """List HDFS directory contents"""
        success, stdout, stderr = self.run_command(f"-ls {hdfs_path}")
        
        if success:
            return stdout
        else:
            return None
    
    def create_directory(self, hdfs_path):
        """Create HDFS directory"""
        print(f"📁 Creating directory {hdfs_path}")
        
        success, stdout, stderr = self.run_command(
            f"-mkdir -p {hdfs_path}"
        )
        
        if success:
            print(f"✓ Directory created")
        else:
            print(f"✗ Failed to create directory: {stderr}")
        
        return success
    
    def delete_path(self, hdfs_path, recursive=False):
        """Delete HDFS path"""
        flag = "-r" if recursive else ""
        print(f"🗑️  Deleting {hdfs_path}")
        
        success, stdout, stderr = self.run_command(
            f"-rm {flag} {hdfs_path}"
        )
        
        if success:
            print(f"✓ Deleted successfully")
        else:
            print(f"✗ Delete failed: {stderr}")
        
        return success


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(
        description='HDFS File Manager'
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Upload command
    upload_parser = subparsers.add_parser('upload', help='Upload file')
    upload_parser.add_argument('local_path', help='Local file path')
    upload_parser.add_argument('hdfs_path', help='HDFS destination')
    
    # Download command
    download_parser = subparsers.add_parser('download', help='Download file')
    download_parser.add_argument('hdfs_path', help='HDFS file path')
    download_parser.add_argument('local_path', help='Local destination')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List directory')
    list_parser.add_argument('hdfs_path', help='HDFS directory path')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete path')
    delete_parser.add_argument('hdfs_path', help='HDFS path to delete')
    delete_parser.add_argument('--recursive', action='store_true')
    
    args = parser.parse_args()
    manager = HDFSManager()
    
    if args.command == 'upload':
        manager.upload_file(args.local_path, args.hdfs_path)
    elif args.command == 'download':
        manager.download_file(args.hdfs_path, args.local_path)
    elif args.command == 'list':
        result = manager.list_directory(args.hdfs_path)
        if result:
            print(result)
    elif args.command == 'delete':
        manager.delete_path(args.hdfs_path, args.recursive)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

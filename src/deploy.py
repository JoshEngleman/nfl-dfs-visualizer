#!/usr/bin/env python3
"""
Automated deployment script for NFL DFS Visualization website.
Uploads files to GoDaddy via FTP.
"""

import os
import sys
from pathlib import Path
from ftplib import FTP
from dotenv import load_dotenv

# Load environment variables from .env file
project_root = Path(__file__).parent.parent
env_path = project_root / '.env'

if not env_path.exists():
    print("❌ ERROR: .env file not found!")
    print(f"   Expected location: {env_path}")
    print()
    print("   Setup instructions:")
    print("   1. Copy .env.example to .env")
    print("   2. Edit .env and add your GoDaddy FTP credentials")
    print("   3. Run this script again")
    sys.exit(1)

load_dotenv(env_path)

# FTP Configuration
FTP_HOST = os.getenv('FTP_HOST')
FTP_USER = os.getenv('FTP_USER')
FTP_PASS = os.getenv('FTP_PASS')
FTP_PORT = int(os.getenv('FTP_PORT', '21'))
REMOTE_BASE_PATH = os.getenv('REMOTE_BASE_PATH', '/public_html/nfl-dfs')
REMOTE_HEADSHOTS_PATH = os.getenv('REMOTE_HEADSHOTS_PATH', '/public_html/nfl-dfs/headshots')

# Validate credentials
if not all([FTP_HOST, FTP_USER, FTP_PASS]):
    print("❌ ERROR: Missing FTP credentials in .env file!")
    print("   Required: FTP_HOST, FTP_USER, FTP_PASS")
    sys.exit(1)

class DeploymentManager:
    def __init__(self):
        self.ftp = None
        self.project_root = project_root

    def connect(self):
        """Connect to FTP server."""
        print(f"🔌 Connecting to {FTP_HOST}...")
        try:
            self.ftp = FTP()
            self.ftp.connect(FTP_HOST, FTP_PORT)
            self.ftp.login(FTP_USER, FTP_PASS)
            print(f"✅ Connected as {FTP_USER}")
            print(f"   Server: {self.ftp.getwelcome()}")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False

    def disconnect(self):
        """Disconnect from FTP server."""
        if self.ftp:
            try:
                self.ftp.quit()
                print("👋 Disconnected from FTP server")
            except:
                pass

    def upload_file(self, local_path, remote_path):
        """Upload a single file to FTP server."""
        try:
            with open(local_path, 'rb') as file:
                self.ftp.storbinary(f'STOR {remote_path}', file)
            file_size = os.path.getsize(local_path)
            print(f"   ✅ Uploaded {local_path.name} ({file_size:,} bytes)")
            return True
        except Exception as e:
            print(f"   ❌ Failed to upload {local_path.name}: {e}")
            return False

    def ensure_directory(self, remote_dir):
        """Create directory if it doesn't exist."""
        try:
            self.ftp.cwd(remote_dir)
        except:
            try:
                # Create directory
                self.ftp.mkd(remote_dir)
                print(f"   📁 Created directory: {remote_dir}")
            except Exception as e:
                print(f"   ⚠️  Could not create directory {remote_dir}: {e}")

    def deploy_website(self):
        """Upload index.html to server."""
        print("\n🌐 Deploying website...")

        index_file = self.project_root / 'public' / 'index.html'
        if not index_file.exists():
            print(f"   ❌ File not found: {index_file}")
            return False

        # Ensure base directory exists
        self.ensure_directory(REMOTE_BASE_PATH)

        # Upload index.html
        remote_path = f"{REMOTE_BASE_PATH}/index.html"
        return self.upload_file(index_file, remote_path)

    def deploy_headshots(self):
        """Upload all headshots to server."""
        print("\n📸 Deploying headshots...")

        headshots_dir = self.project_root / 'cache' / 'headshot_cache_compressed'
        if not headshots_dir.exists():
            print(f"   ❌ Directory not found: {headshots_dir}")
            return False

        # Get list of PNG files
        png_files = list(headshots_dir.glob('*.png'))
        if not png_files:
            print(f"   ❌ No PNG files found in {headshots_dir}")
            return False

        print(f"   Found {len(png_files)} headshots to upload")

        # Ensure headshots directory exists
        self.ensure_directory(REMOTE_HEADSHOTS_PATH)
        self.ftp.cwd(REMOTE_HEADSHOTS_PATH)

        # Upload each file
        uploaded = 0
        failed = 0
        for png_file in png_files:
            if self.upload_file(png_file, png_file.name):
                uploaded += 1
            else:
                failed += 1

        print(f"\n   📊 Results: {uploaded} uploaded, {failed} failed")
        return failed == 0

    def deploy_all(self):
        """Deploy both website and headshots."""
        if not self.connect():
            return False

        try:
            website_ok = self.deploy_website()
            headshots_ok = self.deploy_headshots()

            if website_ok and headshots_ok:
                print("\n✅ Deployment complete!")
                print(f"   Visit: https://joshengleman.com/nfl-dfs/")
            else:
                print("\n⚠️  Deployment completed with errors")

            return website_ok and headshots_ok
        finally:
            self.disconnect()


def main():
    print("=" * 60)
    print("NFL DFS Visualization - Deployment Tool")
    print("=" * 60)

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
    else:
        print("\nUsage:")
        print("  python3 src/deploy.py all         # Deploy everything")
        print("  python3 src/deploy.py website     # Deploy index.html only")
        print("  python3 src/deploy.py headshots   # Deploy headshots only")
        print()
        command = input("What would you like to deploy? (all/website/headshots): ").lower()

    deployer = DeploymentManager()

    if command == 'all':
        deployer.deploy_all()
    elif command == 'website':
        if deployer.connect():
            try:
                deployer.deploy_website()
            finally:
                deployer.disconnect()
    elif command == 'headshots':
        if deployer.connect():
            try:
                deployer.deploy_headshots()
            finally:
                deployer.disconnect()
    else:
        print(f"❌ Unknown command: {command}")
        print("   Valid options: all, website, headshots")
        sys.exit(1)


if __name__ == '__main__':
    main()

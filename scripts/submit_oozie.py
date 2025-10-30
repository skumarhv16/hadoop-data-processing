"""
Submit Oozie workflow for execution
"""
import requests
import argparse
import json
import sys
from pathlib import Path


class OozieClient:
    """Client for interacting with Oozie API"""
    
    def __init__(self, oozie_url):
        """
        Initialize Oozie client
        
        Args:
            oozie_url (str): Oozie server URL
        """
        self.base_url = oozie_url.rstrip('/')
        self.api_version = 'v2'
    
    def submit_workflow(self, workflow_path, properties):
        """
        Submit workflow to Oozie
        
        Args:
            workflow_path (str): Path to workflow.xml
            properties (dict): Job properties
            
        Returns:
            str: Job ID
        """
        endpoint = f"{self.base_url}/{self.api_version}/jobs"
        
        # Prepare configuration
        config = {
            'user.name': properties.get('user.name', 'sandeep'),
            'oozie.wf.application.path': workflow_path,
            **properties
        }
        
        headers = {'Content-Type': 'application/xml'}
        
        # Convert config to XML format
        config_xml = self._dict_to_xml(config)
        
        try:
            response = requests.post(
                endpoint,
                data=config_xml,
                headers=headers
            )
            
            if response.status_code == 201:
                result = response.json()
                job_id = result.get('id')
                print(f"✓ Workflow submitted successfully")
                print(f"  Job ID: {job_id}")
                return job_id
            else:
                print(f"✗ Failed to submit workflow")
                print(f"  Status: {response.status_code}")
                print(f"  Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"✗ Error submitting workflow: {e}")
            return None
    
    def get_job_status(self, job_id):
        """
        Get job status
        
        Args:
            job_id (str): Oozie job ID
            
        Returns:
            dict: Job information
        """
        endpoint = f"{self.base_url}/{self.api_version}/job/{job_id}"
        
        try:
            response = requests.get(endpoint)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to get job status: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error getting job status: {e}")
            return None
    
    def _dict_to_xml(self, config):
        """Convert config dict to XML format"""
        xml_parts = ['<configuration>']
        
        for key, value in config.items():
            xml_parts.append(f'  <property>')
            xml_parts.append(f'    <name>{key}</name>')
            xml_parts.append(f'    <value>{value}</value>')
            xml_parts.append(f'  </property>')
        
        xml_parts.append('</configuration>')
        
        return '\n'.join(xml_parts)


def load_properties(properties_file):
    """Load properties from file"""
    properties = {}
    
    with open(properties_file, 'r') as f:
        for line in f:
            line = line.strip()
            
            if not line or line.startswith('#'):
                continue
            
            if '=' in line:
                key, value = line.split('=', 1)
                properties[key.strip()] = value.strip()
    
    return properties


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(
        description='Submit Oozie workflow'
    )
    parser.add_argument(
        '--workflow',
        required=True,
        help='Path to workflow XML'
    )
    parser.add_argument(
        '--properties',
        required=True,
        help='Path to job properties file'
    )
    parser.add_argument(
        '--oozie-url',
        default='http://localhost:11000/oozie',
        help='Oozie server URL'
    )
    
    args = parser.parse_args()
    
    # Load properties
    print("📋 Loading job properties...")
    properties = load_properties(args.properties)
    
    # Submit workflow
    print("🚀 Submitting workflow...")
    client = OozieClient(args.oozie_url)
    job_id = client.submit_workflow(args.workflow, properties)
    
    if job_id:
        print("\n📊 Job submitted successfully!")
        print(f"   Track at: {args.oozie_url}/?job={job_id}")
    else:
        print("\n❌ Failed to submit workflow")
        sys.exit(1)


if __name__ == '__main__':
    main()

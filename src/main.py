import re
import ipaddress
import os
import logging
from typing import Set, Tuple, List
from concurrent.futures import ProcessPoolExecutor, as_completed
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import time

class IPExtractor:
    """Efficient and robust IP address extraction from log files with MongoDB storage."""
    
    # Comprehensive private network ranges
    PRIVATE_NETWORKS = [
        ipaddress.ip_network('10.0.0.0/8'),
        ipaddress.ip_network('172.16.0.0/12'),
        ipaddress.ip_network('192.168.0.0/16')
    ]
    
    # Advanced IP matching regex
    IP_PATTERN = re.compile(
        rb'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
        rb'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    )
    
    @classmethod
    def validate_ip(cls, ip: str) -> bool:
        """Validate and check IP address."""
        try:
            ip_obj = ipaddress.ip_address(ip)
            return not (
                ip_obj.is_unspecified or 
                ip_obj.is_reserved or 
                ip_obj.is_multicast
            ) and any(ip_obj in network for network in cls.PRIVATE_NETWORKS)
        except ValueError:
            return False
    
    @classmethod
    def extract_ips_from_file(
        cls,
        file_path: str,
        chunk_size: int = 1024 * 1024
    ) -> Tuple[List[str], List[str]]:
        """Extract IPs from log file."""
        # Validate file
        if not os.path.isfile(file_path) or os.path.getsize(file_path) == 0:
            logging.error(f"Invalid file: {file_path}")
            return [], []
        
        private_ips, public_ips = set(), set()
        
        try:
            with open(file_path, 'rb') as file:
                with ProcessPoolExecutor() as executor:
                    # Process file in chunks
                    futures = []
                    while True:
                        chunk = file.read(chunk_size)
                        if not chunk:
                            break
                        
                        futures.append(executor.submit(cls._process_chunk, chunk))
                    
                    # Collect results
                    for future in as_completed(futures):
                        chunk_private, chunk_public = future.result()
                        private_ips.update(chunk_private)
                        public_ips.update(chunk_public)
        except Exception as e:
            logging.error(f"Processing error: {e}")
            return [], []
        
        return sorted(list(private_ips)), sorted(list(public_ips))
    
    @classmethod
    def _process_chunk(cls, chunk: bytes) -> Tuple[Set[str], Set[str]]:
        """
        Process a chunk of log file data.
        
        Args:
            chunk (bytes): File chunk to process
        
        Returns:
            Tuple of private and public IP sets
        """
        private_ips, public_ips = set(), set()
        
        # Extract unique IPs
        ips = set(ip.decode('utf-8', errors='ignore')
                  for ip in cls.IP_PATTERN.findall(chunk))
        
        # Classify IPs
        for ip in ips:
            (private_ips if cls.validate_ip(ip) else public_ips).add(ip)
        
        return private_ips, public_ips

def connect_to_mongodb(uri: str, database: str = 'ip_extraction', 
                       private_collection: str = 'private_ips', 
                       public_collection: str = 'public_ips'):
    """
    Establish a connection to MongoDB and return client and collections.
    
    Args:
        uri (str): MongoDB connection URI
        database (str): Database name
        private_collection (str): Collection name for private IPs
        public_collection (str): Collection name for public IPs
    
    Returns:
        Tuple of (MongoClient, private collection, public collection)
    """
    try:
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))
        
        # Verify the connection
        client.admin.command('ping')
        logging.info("Successfully connected to MongoDB!")
        
        # Get or create database and collections
        db = client[database]
        private_coll = db[private_collection]
        public_coll = db[public_collection]
        
        return client, private_coll, public_coll
    
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {e}")
        return None, None, None

def main(log_file):
    """Main execution for IP extraction and MongoDB storage."""
    try:
        # Configure logging
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s: %(message)s'
        )
        
        # MongoDB connection URI (replace with your actual connection string)
        mongodb_uri = "mongodb://mongodb:27017"
        
        # Connect to MongoDB
        client, private_coll, public_coll = connect_to_mongodb(mongodb_uri)
        
        if not client:
            logging.error("MongoDB connection failed. Exiting.")
            return
        
        # Extract IPs from log file
        private_ips, public_ips = IPExtractor.extract_ips_from_file(log_file)
        
        # Clear previous entries and insert new IPs
        private_coll.delete_many({})
        public_coll.delete_many({})
        
        # Insert IPs as documents
        if private_ips:
            private_coll.insert_many([{'ip': ip} for ip in private_ips])
        if public_ips:
            public_coll.insert_many([{'ip': ip} for ip in public_ips])
        
        # Display results
        print(f"Private IPs: {len(private_ips)}")
        print(f"Public IPs: {len(public_ips)}")

        
        # Close MongoDB connection
        client.close()
    
    except Exception as e:
        logging.error(f"Execution error: {e}")

if __name__ == "__main__":
    while(True):
        log_file = 'data/access.log'
        print("Calling Main Function")
        main(log_file=log_file)
        print("Sleeping for 10 seconds")
        time.sleep(10)
# IP Extractor

## Overview

The **IP Extractor** is a Python application designed to efficiently extract and classify IP addresses from log files. The tool identifies and separates private and public IPs, storing them in MongoDB for further analysis. This project leverages concurrent processing for faster extraction and uses advanced IP matching techniques.

## Features

- Extracts IPv4 addresses from log files.
- Classifies IP addresses into private and public categories.
- Stores classified IPs in MongoDB.
- Utilizes concurrent processing for efficient log file parsing.
- Configurable log file and extraction intervals.

## Project Structure

```
ip_extractor/
│
├── config/
│   ├── __init__.py
│   └── settings.py            # Configuration settings for the application
│
├── core/
│   ├── __init__.py
│   ├── ip_validator.py        # Validates and categorizes IP addresses
│   └── ip_extractor.py        # Extracts and classifies IP addresses from log files
│
├── database/
│   ├── __init__.py
│   └── mongodb_manager.py     # Handles MongoDB operations for storing IPs
│
├── utils/
│   ├── __init__.py
│   └── logging_config.py      # Configures application-wide logging
│
└── main.py                    # Main entry point for continuous IP extraction
```

## Requirements

- Python 3.6 or higher.
- MongoDB (local or remote server).

### Install Dependencies

First, install the required Python libraries by running the following command:

```bash
pip install -r requirements.txt
```

### MongoDB Setup

Ensure that MongoDB is running on your local or remote server. Update the connection URI in `main.py` to reflect the correct MongoDB address.

## Configuration

All the key configuration settings are stored in `config/settings.py`. You can modify the following settings:

- **PRIVATE_NETWORKS**: List of private IP address ranges.
- **MONGODB_URI**: MongoDB connection URI.
- **DATABASE_NAME**: The name of the database in MongoDB.
- **PRIVATE_IPS_COLLECTION**: Collection name for storing private IPs.
- **PUBLIC_IPS_COLLECTION**: Collection name for storing public IPs.
- **LOG_FILE_PATH**: Path to the log file that will be scanned for IP addresses.
- **CHUNK_SIZE**: Size of each chunk for reading the log file.
- **EXTRACTION_INTERVAL**: Interval in seconds between extractions.

## Running the Project

To start the IP extraction process, simply run the `main.py` script:

```bash
python main.py
```

### What Happens:
1. The script connects to the MongoDB server.
2. It extracts IP addresses from the specified log file (`access.log`).
3. It classifies IPs into private and public categories.
4. It stores the extracted IPs in the `private_ips` and `public_ips` collections in MongoDB.
5. The process runs continuously every 10 seconds (configurable).

## Logging

Logging is configured using Python's built-in logging module. By default, the logging level is set to `INFO`, but you can modify the level in `logging_config.py` to `DEBUG` or `ERROR` depending on your needs.

### Example Log Output:

```
2025-03-27 10:15:00 - INFO: Successfully connected to MongoDB!
2025-03-27 10:15:05 - INFO: Extracted 10 private IPs
2025-03-27 10:15:05 - INFO: Extracted 5 public IPs
2025-03-27 10:15:10 - INFO: Stored 10 private and 5 public IPs
```

## MongoDB Storage

The extracted IP addresses are stored in MongoDB under the following collections:
- **private_ips**: Stores private IP addresses.
- **public_ips**: Stores public IP addresses.

Each IP address is stored as a document in its respective collection.

## Next Steps & Enhancements

Here are some suggested improvements:
- **Unit Testing**: Add unit tests for the key modules like IP extraction, validation, and MongoDB storage.
- **Docker Support**: Create a Docker container to easily deploy the application.
- **Error Handling**: Implement retries and error handling for MongoDB connectivity issues.
- **Configuration Management**: Implement environment-specific configurations to handle different setups for development, staging, and production.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
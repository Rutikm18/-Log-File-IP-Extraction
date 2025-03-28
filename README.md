# IP Extractor: Dynamic Log File IP Processing

## Overview

The **IP Extractor** is a sophisticated Python application designed to dynamically extract and classify IP addresses from log files. The tool provides real-time IP address identification, classification, and MongoDB storage with continuous monitoring and processing capabilities.

## Key Features

- 🔍 Dynamic log file processing
- 🌐 Automatic IP address extraction
- 🏗️ IP classification (private vs. public)
- 📦 MongoDB storage integration
- 🚀 Concurrent processing for efficiency
- ♻️ Continuous monitoring and extraction

## How It Works

The application continuously monitors a specified log file and performs the following tasks:

1. **Dynamic File Scanning**: 
   - Automatically processes the designated log file
   - Supports real-time updates and file changes
   - Configurable scanning interval (default: 10 seconds)

2. **IP Address Extraction**:
   - Uses advanced regex for comprehensive IP detection
   - Supports IPv4 address extraction
   - Filters out unspecified, reserved, and multicast addresses

3. **IP Classification**:
   - Categorizes IPs into private and public networks
   - Identifies IPs within standard private network ranges:
     - 10.0.0.0/8
     - 172.16.0.0/12
     - 192.168.0.0/16

4. **MongoDB Integration**:
   - Stores extracted IPs in separate collections
   - Supports easy configuration of MongoDB connection
   - Provides clear logging of extraction process

## Project Structure

```
ip_extractor/
│
├── src/
│   └── main.py             # Core extraction logic
├── data/
│   └── access.log          # Log file to be processed
├── Dockerfile              # Docker containerization
└── docker-compose.yml      # Docker composition
```

## Configuration

### Log File Configuration

- **Default Location**: `data/access.log`
- **Customization**: Easily change log file path in `main.py`
- **Supports**: Any text-based log file with IPv4 addresses

### MongoDB Configuration

- **Connection URI**: Configurable in `main.py`
- **Default URI**: `mongodb://mongodb:27017`
- **Collections**:
  - `private_ips`: Stores private IP addresses
  - `public_ips`: Stores public IP addresses

## Docker Deployment

### Prerequisites
- Docker
- Docker Compose

### Deployment Steps

1. Clone the repository
2. Add your log file under data with name access.log
3. Run deployment:
   ```bash
   docker-compose up --build
   ```


## Performance Considerations

- Uses `ProcessPoolExecutor` for concurrent processing
- Chunk-based file reading for memory efficiency
- Minimal resource consumption

## Logging

Comprehensive logging provides insights into:
- MongoDB connection status
- IP extraction details
- Error tracking

**Log Format**: 
```
2024-03-28 10:15:00 - INFO: Successfully connected to MongoDB!
2024-03-28 10:15:05 - INFO: Extracted 10 private IPs
2024-03-28 10:15:05 - INFO: Extracted 5 public IPs
```

## Extensibility

Future enhancements can include:
- Advanced IP reputation checking
- Support for IPv6
- Enhanced error handling
- More granular IP classification

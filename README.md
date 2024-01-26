# Simple File Store Application

This repository contains a simple file store application with a client-server architecture. Follow the instructions below to set up and run the application.

## Instructions

### Prerequisites

- `kubectl` installed on your machine.
- A locally running Kubernetes cluster or a local Kubernetes environment like Docker Desktop.

### Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/sauravchandra/simple-file-store.git
   ```

2. **Deploy the Server:**

   ```bash
   cd simple-file-store/deploy
   chmod +x run.sh
   ./run.sh
   ```

3. **Install the Client:**

   ```bash
   cd ..
   pip3 install .
   ```

5. **Access the Client:**

   ```bash
   store --help
   ```

   The client supports the following commands:

   * `add`: Add files
   * `ls`: List files
   * `rm`: Remove files
   * `update`: Update file
   * `wc`: Get word count
   * `freq-words`: Get frequent words

   Example:
   ```bash
   store add file1.txt file2.txt
   ```

   For more details on each command, use:
   ```bash
   store <command> --help
   ```

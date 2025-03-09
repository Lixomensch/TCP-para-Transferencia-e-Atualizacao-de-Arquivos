# Project Overview

This project implements a Python-based server-client architecture, with tools managed via a Makefile to simplify common tasks such as running the server, sending requests, and updating data.

## Prerequisites

Ensure that the following dependencies are installed before using this project:

- Python 3.x (preferably 3.7 or above)
- Make (for running the Makefile commands)

Additionally, you’ll need to have a `.env` file configured with the necessary environment variables for your project.

## Usage

### Running the Server

To start the server, execute the following command:

```sh
make server
```

This will run the `server.py` file located in the `src` folder.

### Sending a Request

To send a request to the server, use the following command:

```sh
make request
```

This will trigger the `client.py` script with the `request` argument to initiate a request to the server.

### Updating Data

To update data via the client, run:

```sh
make update
```

This will run the `client.py` script with the `update` argument to trigger a data update.

## License

This project is licensed under the [MIT License](LICENSE).

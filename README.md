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

### Send a new data file

To send a new data file via the client, run the following command:

```sh
make new
```

This will run the `client.py` script with the `new` argument, sending the new data file.

### Send a new PDF file

To send a new PDF file via the client, run the following command:

```sh
make newpdf
```

This will run the `client.py` script with the `new rafael.pdf` argument, sending the new PDF file.

### Additional Client Operations

Beyond the standard `make` commands, you can also manually specify a filename for different operations:

- **Request a specific file:**

  ```sh
  python src/client.py request <filename>
  ```

  If no filename is provided, the default is `test.txt`.

- **Update a specific file:**

  ```sh
  python src/client.py update <filename>
  ```

  If no filename is provided, the default is `test.txt`.

- **Send a new file:**

  ```sh
  python src/client.py new <filename>
  ```

  If no filename is provided, the default is `test_new.txt`.

These options provide greater flexibility in specifying which file to process.

## License

This project is licensed under the [MIT License](LICENSE).

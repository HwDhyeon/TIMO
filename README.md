# TIMO

<p align="center">
  <img src="https://user-images.githubusercontent.com/37629503/88120645-5ff14300-cbfe-11ea-98e0-c42b00f524c6.png" />
</p>

![rate](https://img.shields.io/github/languages/top/hwdhyeon/timo)  
![reposize](https://img.shields.io/github/repo-size/hwdhyeon/timo)  
![lastcommit](https://img.shields.io/github/last-commit/hwdhyeon/timo)  
![coverage](https://img.shields.io/badge/coverage-69%25-yellowgreen)  
![markdownlint](https://img.shields.io/badge/markdown%20lint-pass-brightgreen)

_`TIMO` stands for `Test integration management tool` and is a tool that performs various tests and collects the results into one result._

## Installation

**Requirements**

- Python3.8+

### Common

Clone this repository using Git.

```bash
> git clone https://github.com/HwDhyeon/TIMO.git
```

Then go into the TIMO folder.

```bash
> cd TIMO
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install required packages.

```bash
> pip install -r requirements.txt
```

### Windows

Run setup_env.bat

```cmd
.\setup_env.bat
```

### Unix(Linux, MacOS, ...)

Run setup_env.sh

```bash
./setup-env.sh
```

### Docker

Build the image

```bash
> docker build -f Dockerfile -t timo:latest --compress --no-cache .
```

Run container

```bash
> docker run -itd --name TIMO -w /root timo:latest
```

Enter the container

```bash
> docker exec -it TIMO bash
```

Create a data folder and create a conf file in it.

```bash
> mkdir data
> touch conf.yaml
```

## Usage

First, help TIMO recognize your conf file.

```bash
> timo setting <conf file extension>
```

And check your project information.

```bash
> timo get name
Project name: TIMO

> timo get version
Project version: v1.0.0
TIMO version: v0.0.1
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

**[MIT License](https://choosealicense.com/licenses/mit/)**

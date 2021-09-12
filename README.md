<p align="center">
    <img width="200" src="../assets/images/logo.png?raw=true">
</p>

<h1 align="center">Hybrid Rocket Design</h1>

<div align="center">
Tool to assist in hybrid rocket motor design.
</div>

<br/>

<p align="center">
    <img width = "800" src="../assets/images/app_overwiew.png?raw=true">
</p>

# Table of Contents

1. [About the project](#about-the-project)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
5. [License](#license)

# About the project

This project consists of a tool developed to assist researchers and students during the design of hybrid rocket engines.
This tool can solve the rocket problem using the [CEA NASA](https://www1.grc.nasa.gov/research-and-engineering/ceaweb/) (McBride) program,
perform a propellant analysis by varying the mixing ratio value, as well as carry out a simulation of the burning for a single perforation tubular grain, providing as output the motor dimensions.

This software can be used during early development to validate the propellant viability, as well as the motor geometry. See [Usage](#usage) for more information about everything this tool can do. 

# Prerequisites

## Linux

* Python 3.3+
* pip
* WineHQ

If you don't have WineHQ installed, you can install it with the following commands.

```shell
$ sudo dpkg --add-architecture i386
$ wget -nc https://dl.winehq.org/wine-builds/winehq.key
$ sudo apt-key add winehq.key
$ sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ xenial main'
$ sudo apt-get update
$ sudo apt-get install --install-recommends winehq-stable
```

## Windows

* Python 3.3+
* pip

# Installation

## Linux

You can install this tool with the following commands.

```shell
$ git clone https://github.com/lrischioni/hybrid-rocket-design.git
$ cd hybrid-rocket-design
$ pip install .
```

If you want to install this package in a virtual enviroment, just follow the commands below.

```shell
$ git clone https://github.com/lrischioni/hybrid-rocket-design.git
$ cd hybrid-rocket-design
$ python3 -m venv myenv
$ source ./myenv/bin/activate
$ pip install .
```

If using conda, you can just follow the instructions below.

```shell
$ git clone https://github.com/lrischioni/hybrid-rocket-design.git
$ cd hybrid-rocket-design
$ conda activate
$ conda create --name myenv
$ conda install -n myenv pip
$ conda activate myenv
$ pip install .
```

## Windows

Download this repository and extract the files on the desired location. Then, open the command prompt and navigate to the chosen location and enter the commands below.

```shell
python3 -m venv myenv
.\myenv\scripts\activate
pip install .
```

# Usage

Just type `hybridrd` on the terminal to launch the GUI after installing.

After importing a CEA .inp file, the information is displayed on the interface.

<p align="left">
    <img width = "800" src="../assets/images/app_usage1.png?raw=true">
</p>

Then, you can run the CEA program and the output with the results is shown.

<p align="left">
    <img width = "800" src="../assets/images/app_usage2.png?raw=true">
</p>

After that, on the 'Propellant Analysis' tab, you can vary the misture ratio value and check its influence on the propulsive parameters, as shown below.

<p align="left">
    <img width = "800" src="../assets/images/app_usage3.png?raw=true">
</p>

After providing the required information on the 'Burn Simulation' tab, you can perform the simulation. The results are shown on the next tab.

<p align="left">
    <img width = "800" src="../assets/images/app_usage5.png?raw=true">
</p>

<p align="left">
    <img width = "800" src="../assets/images/app_usage6.png?raw=true">
</p>

# License

This project is licensed under the terms of the [GNU GPLv3 license](../master/LICENSE.txt).
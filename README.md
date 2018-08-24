# Music Signals Visualization


Web application to see features extracted by different algorithms from a track file in 2d dimensionality.

Current feature extractors supported:

- Marsyas (GTZAN)
- Random Projection
- Short-Time Fourier Transform

Current grouping algorithms supported:

- KMeans

Current visualization algorithms supported:

- Principal Component Analysis



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

- python-dev
- python-venv
- [Some Python libraries](https://github.com/vitorys/musicSignalsVisualization/blob/master/requirements.txt)

### Installing

A step by step series of examples that tell you how to get a development env running

Install Python dependencies:

```
pip install -r requirements.txt
```

#### Good Practices

We recommend installing dependencies in a virtual enviroment (virtualenv)

First, create a virtualenv named venv

```
virtualenv venv
```

Activate the virtual enviroment.

```
source venv/bin/activate
```

Now you can install the dependencies

```
pip install -r requirements
```

## Deployment

The deployment process is simple.
After installing the dependencies or activate the virtual enviroment, you must run the file ```run.py```.

```
python run.py
```

If everything goes right, you should see the following output:

![](https://i.imgur.com/2ApRQAh.png)

Now you can acess ```localhost:8080``` and use the application.

Note: You must leave the terminal open. If you want to execute the application in background, add ```&``` in the end of ```python run.py```

```
python run.py &
```

## Built With

* [Flask](http://flask.pocoo.org/) - The web framework used
* [Pyplot](https://plot.ly/) - Visualization Javascript API

## Authors

* **Vítor Y. Shinohara** - *Initial work* - [vitorys](https://github.com/vitorys)


* **Juliano H. Foleiss** - *Feature extractors algorithms* - [julianofoleiss](https://github.com/julianofoleiss)



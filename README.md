## Methodology
Recipes Economy Dashboard was developed in order to present a dynamic file where to experiment with distinct inputs that changes the amount of resources on gathering nodes and encounters. 
This is about aggregations per region name and materials family. Each section provides an explanation. We cover:
*  Amount of gathering nodes distributed by Regions and number of physical elements on that based on a global multiplier value.
*  Enemies Resources Drops that includes Spiritual Elements.
*  Time to complete a certain recipe based on those numbers.

## Output Dashboard
The final output can be found on:

*  [`streamlit dashboard`](https://mariaob1201-runiverse-sinkstaps-main-ls4sij.streamlit.app/).


## Prerequisities

Before you begin, ensure you have met the following requirements:

* You have a _Windows/Linux/Mac_ machine running [Python 3.6+](https://www.python.org/).
* You have installed the latest versions of [`pip`](https://pip.pypa.io/en/stable/installing/) and [`virtualenv`](https://virtualenv.pypa.io/en/stable/installation/) or `conda` ([Anaconda](https://www.anaconda.com/distribution/)).


## Setup

To install the dependencies, you can simply follow this steps.

Clone the project repository:
```bash
git clone https://github.com/bisonic-official/runiverse-economy.git
cd streamlit-example
```

To create and activate the virtual environment, follow these steps:

**Using `conda`**

```bash
$ conda create -n streamlit python=3.7

# Activate the virtual environment:
$ conda activate streamlit

# To deactivate (when you're done):
(streamlit)$ conda deactivate
```

**Using `virtualenv`**

```bash
# In this case I'm supposing that your latest python3 version is 3.7
$ virtualenv streamlit --python=python3

# Activate the virtual environment:
$ source streamlit/bin/activate

# To deactivate (when you're done):
(streamlit)$ deactivate
```

To install the requirements using `pip`, once the virtual environment is active:
```bash
(streamlit)$ pip install -r requirements.txt
```

#### Running the script

Finally, if you want to run the main script:
```bash
(streamlit)$ streamlit run main.py
```



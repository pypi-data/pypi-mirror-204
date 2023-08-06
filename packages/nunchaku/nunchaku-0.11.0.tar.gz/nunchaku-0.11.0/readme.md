# nunchaku: Dividing data into linear segments

`nunchaku` is a Python module for dividing data into linear segments.
It answers two questions:
1. how many linear segments best fit the data without overfitting (by Bayesian model comparison);
2. given the number of linear segments, where the boundaries between them are (by finding the posterior of the boundaries).

## Installation
For users, type in terminal
```
> pip install nunchaku
```

For developers, create a virtual environment and then install with Poetry: 
```
> git clone https://git.ecdf.ed.ac.uk/s1856140/nunchaku.git
> cd nunchaku 
> poetry install --with dev 
```

## Quickstart
Data `x` is a list or a 1D Numpy array, sorted ascendingly; the data `y` is a list or a Numpy array, with each row being one replicate of measurement.
```
>>> from nunchaku import Nunchaku, get_example_data
>>> x, y = get_example_data()
>>> nc = nunchaku(x, y, prior=[-5,5]) # load data and set prior of gradient
>>> # compare models with 1, 2, 3 and 4 linear segments
>>> numseg, evidences = nc.get_number(max_num=4)
>>> # get the mean and standard deviation of the boundary points
>>> bds, bds_std = nc.get_iboundaries(numseg)
>>> # get the information of all segments
>>> info_df = nc.get_info(bds)
>>> # plot the data and the segments
>>> nc.plot(info_df)
```

## Documentation
Detailed documentation is available on [Readthedocs](https://nunchaku.readthedocs.io/en/latest/).

## Citation
A preprint is coming soon.

# pyDataVizDay
*a python implementation for Data Viz Day*

![python](https://s3.amazonaws.com/files.dezyre.com/images/blog/Python+for+Data+Science+vs.+Python+for+Web+Development/Python+for+Data+Science+vs+Web+Devlopment.png)

----

# Agenda

1. Viz Walk (3 Views)
    1. Full Web App
    * Simple Web App
    * Exploritory Notebook
* Tools Used
* Other Considerations
* Pros/Cons

----

## About Me

![profile](/static/profile_photo_sm.jpg)

Waylon Walker

Product Engineering



----

# Open The Viz

[pydatavizday.herokuapp.com](pydatavizday.herokuapp.com)

---

**Seriously** Get out your devices

[pydatavizday.herokuapp.com](pydatavizday.herokuapp.com)

----

## Stack for this viz

* Python
      * pandas
      * flask
* javascript
      * C3
      * reveal
      * jquery
      * jqcloud
* HTML
      * Bootstrap


----

## Other Considerations

* Jupyter Notebooks
* Jupyter Dashboards
* DASH (just released in mid JUNE)

---

### Jupyter Notebooks

* My Adhoc analysis of choice
* Many plugins (including reveal)
* Data/viz/slides All in one place

![jupyter notebook](http://jupyter.org/assets/jupyterpreview.png)

---

### Jupyter Dashboards

* Dashboard plugin for Jupyter notebook

![jupyter dashboard](https://github.com/jupyter/dashboards/raw/master/docs/source/_static/dashboards_intro.png)

---

### DASH

* released in June

![dash](https://camo.githubusercontent.com/a1be75b74d4a47c50df7018e914d63a2e232e503/68747470733a2f2f63646e2d696d616765732d312e6d656469756d2e636f6d2f6d61782f3830302f312a44455441517136572d7079746c4e6f487a4c496144412e706e67)


----

## Pros of Python

* Fast High Level Data Science
* reusable
* Powerful Web stack
* Testing
* Documentation
* Profiling
* Free

---

### Fast High Level Data Science

python has a vast ecosysytem for data wrangling

``` python
import pandas as pd
import glob, os

path = "C:/reports"
files = glob.glob(path + os.sep + '*_report.csv*')

frames = []
for file in files:
    frames.append(pd.read_csv(file))

all_reports = (pd.concat(frames)
                 .dropna()
                 .query('DIVISION == ACCOUNTING')
                 )

```

---

### Reusability

Python libraries, and objects are very easily written and reused

```
import etl

data = etl.Data()
data.update()

```

---

### Testing

The ability to easily reuse code/datasets/plot gives us the ability to spend time making large projects more .


``` python
class Testdata(unittest.TestCase):
    """
    Test suite for my dataframe data
    """

    def test_cols(self):
        for col in important_cols:
            self.assertLess(len(data[data[col].isnull()]), 0, msg=f'column {col} has unexpected null values')
            self.assertIn(col, data.columns.tolist(), msg=f'column {col} is missing - check the /data/raw/shipments.csv file to ensure logistics has not changed the data format')

```

---

### Testing *(cont.)*

Alert us of an error before it becomes an issue

``` python
suite = unittest.TestLoader().loadTestsFromModule(Testdata())
results = unittest.TextTestRunner().run(suite)
if test_results.wasSuccessful():
    data.to_csv(settings.processed_data_dir + os.sep + 'processed_reports.csv')
else:
    print('test failed, not saving reports')
```

---

## Documentation

*The python community has a very strong focus on documentation*

---
* automated html docs
* free hosting for any pypi package
* docstrings

---

### Free

*enough said*

----

## Cons on python

* Code
* Interactivity
* Speed
* ML research

---

### No GUI (Drag and Drop Environment)
*Longer Learning Curve*

---

### Interactive plots are difficult

---

### Slow

*slow runtime compared to statically typed languages (c, java)*

---

### Latest ML aglorithms are typically developed in R

---


### I ♥ Code

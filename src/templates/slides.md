# pyDataVizDay
---
*a python implementation for Data Viz Day*

![python](https://s3.amazonaws.com/files.dezyre.com/images/blog/Python+for+Data+Science+vs.+Python+for+Web+Development/Python+for+Data+Science+vs+Web+Devlopment.png)

----

# Agenda
---
1. Viz Walk (2 Views)
    1. Full Web App
    * Exploritory Notebook
* Tools Used
* Other Considerations
* Pros/Cons

----

# About Me
---
![profile](/static/profile_photo_sm.jpg)

Waylon Walker

Product Engineering

----

# Open The Viz
---
[pydatavizday.herokuapp.com](pydatavizday.herokuapp.com)

---

**Seriously** Get out your devices

[pydatavizday.herokuapp.com](pydatavizday.herokuapp.com)

----

# External Resources

---

### Enthusiast
<div class='container'>
<div class='row' style='text-align:left; margin:50px'>
<div class='col-sm-4' style='margin:0px'>

<h4>Python</h4>
<ul>
    <li>pandas</li>
    <li>flask</li>
    <li>flask_restplus</li>
    <li>markdown</li>
</ul>
</div>
<div class='col-sm-4' style='margin:0px'>

<h4>javascript</h4>
<ul>
    <li>C3</li>
    <li>reveal</li>
    <li>jquery</li>
    <li>jqcloud</li>
</ul>
</div>
<div class='col-sm-4' style='margin:0px'>

<h4>HTML</h4>
<ul>
    <li>Bootstrap</li>
<ul>
</div>
</div>
</div>

---

### Exploritory

Python
  * jupyter
  * seaborn
  * numpy
  * pandas
  * sci-kit learn

----

## Other Considerations
---
* Jupyter Notebooks
* Jupyter Dashboards
* DASH (just released in mid JUNE)
* Bokeh
* Data shader

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
---
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

raw_example = pd.read_csv('example_data.csv')

example = (raw_example
  .groupby(['Date'])
  .sum()
  .resample('m')
  .fillna(0)
  )

example.plot()
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

Well written tests give us the confidence to push to production without manually spending our own time testing each feature of our end product.

``` python
import unittest
import etl

class Testdata(unittest.TestCase):
    """
    Test suite for my dataframe data
    """
    def setUp(self):
      self.data = etl.Data()
      important_cols = ['DATE', 'PRODUCT', 'QTY']

    def test_cols(self):
        for col in important_cols:
            self.assertIn(col, sdata.columns.tolist())

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
---
* Code
* Interactivity
* ML research

---

### No GUI (Drag and Drop Environment)
*Longer Learning Curve*

---

### Interactive plots are difficult

---

### Latest ML aglorithms are typically developed in R

---


### I ♥ Code

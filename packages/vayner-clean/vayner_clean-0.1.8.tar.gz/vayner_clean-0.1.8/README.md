# Getting Started 
This library has generic functions for cleaning advertising data such as standardising column
names between platforms and countries or extracting a Country like "France" from a string column

[Full Online Documentation](https://VaynerMedia-London.github.io/vaynerclean/)

## Library Installation
```
pip install vaynerclean
```
To upgrade the library after an update
```
pip install vayner-clean --upgrade
```

## Importing the Library
```
from vee_clean import cleaning_functions as clean
```

## Usage in code
In this example we will be using the cleaning library to clean and standardise column names in a dataframe 

```
fb_organic = clean.clean_column_names(fb_organic_temp)
```

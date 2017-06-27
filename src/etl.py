import os
import pandas as pd
import settings


class Data(object):
    """
    A data object for loading, updating, cleaning, and holding data.
    """

    def __init__(self, data=None):
        """
        loads data on creation if no data is provided
        """
        if data == None:
            self.load()

    def __str__(self):

        value = ''
        for key in self.__dict__.keys():
            if isinstance(self.__dict__[key], pd.DataFrame):
                value = value + f'item: {key},\ntype:{type(self.__dict__[key])},\nhead: {self.__dict__[key].head(1).T}\n\n'
            else:
                value = value + f'item: {key},\ntype:{type(self.__dict__[key])},\nvalue: {self.__dict__[key]}\n\n'

        return value

    def load(self):
        """
        loads/reloads data.  Can be called to update data without redefining a 
        new data object.
        """

        self.movie = pd.read_csv(os.path.join(settings.raw_data_dir, 'movie_metadata.csv'))

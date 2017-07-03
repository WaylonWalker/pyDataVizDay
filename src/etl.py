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

    def __repr__(self):
        return self.__str__()

    def load(self):
        """
        loads/reloads data.  Can be called to update data without redefining a 
        new data object.
        """

        self.movie = pd.read_pickle(os.path.join(settings.processed_data_dir, 'movie.pkl'))
        self.genre = pd.read_pickle(os.path.join(settings.processed_data_dir, 'genre.pkl'))
        self.keyword = pd.read_pickle(os.path.join(settings.processed_data_dir, 'keyword.pkl'))

    def update_data(self):
        """
        creates processed data sets from raw data sets
    
        This method only needs ran when the dataset gets updated
        """
        movie = pd.read_csv(os.path.join(settings.raw_data_dir, 'movie_metadata.csv'))
        movie['net'] = movie['gross'] - movie['budget']
        movie['profitable'] = 0
        movie.loc[movie['net']>0, 'profitable'] = 1
        movie.title_year = pd.to_datetime({'year':movie.title_year, 'month':1, 'day':1})
        movie.to_pickle(os.path.join(settings.processed_data_dir, 'movie.pkl'))

        genre = generate_genre(movie)
        genre.to_pickle(os.path.join(settings.processed_data_dir, 'genre.pkl'))

        keyword = generate_keyword(movie)
        keyword.to_pickle(os.path.join(settings.processed_data_dir, 'keyword.pkl'))


def generate_genre(movie):
    """
    splits genres into rows
    
    movie: DataFrame of movie Data
    returns: returns DataFrame of index and genre
    """
    genres = movie.reset_index()[['index', 'genres']]
    frames = list()
    for row in genres.iterrows():
        row_genres = row[1].genres.split('|')
        index = row[1]['index']
        frames.append(pd.DataFrame({'index':[index]*len(row_genres), 'genres': row_genres}))

    genre = pd.concat(frames).reset_index(drop=True)[['index', 'genres']]
    return genre



def generate_keyword(movie):
    """
    splits keywords into rows
    
    movie: DataFrame of movie Data
    returns: returns DataFrame of index and keyword
    """

    keywords = movie.reset_index()[['index', 'plot_keywords']].fillna('')
    frames = list()
    for row in keywords.iterrows():
        try:
            row_keywords = row[1].plot_keywords.split('|')
        except:
            print(row[1].plot_keywords)
        index = row[1]['index']
        frames.append(pd.DataFrame({'index':[index]*len(row_keywords), 'plot_keywords': row_keywords}))

    keyword = pd.concat(frames).reset_index(drop=True)[['index', 'plot_keywords']]
    return keyword


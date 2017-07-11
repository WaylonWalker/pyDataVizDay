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
        else:
            self.movie = data.movie
            self.genre = data.genre
            self.keyword = data.keyword

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

    def filter(self, start_year=None, end_year=None, 
                     genre=None, country=None, language=None, 
                     top=None, title=None, color=None):

            """
            Efficiently filters 

            """
            data = Data(self)

            if start_year:
                start_year_mask = data.movie.title_year > f'{str(int(start_year)-1)}-01-01'
            else:
                start_year_mask = True
            if end_year:
                end_year_mask = data.movie.title_year <= f'{str(end_year)}-01-01'
            else:
                end_year_mask = True
                
            if genre:
                genre_indexes = data.genre[data.genre.genres == genre]['index'].values
                genre_mask = data.movie.index.isin(genre_indexes)
            else:
                genre_mask = True

            if country:
                country_mask = data.movie.country == country
            else:
                country_mask = True

            if language:
                language_mask = data.movie.language == language
            else:
                language_mask = True

            if title:
                title_mask = data.movie.movie_title == title
            else: 
                title_mask = True

            if color:
                color_mask = data.movie.color == color
            else:
                color_mask = True
            masks = genre_mask & start_year_mask & end_year_mask & country_mask & language_mask & title_mask & color_mask

            try:
                len(masks)
            except TypeError: # object type 'bool' has no len() i.e. not a list
                masks = [True]*len(data.movie)

            data.movie = data.movie[masks].sort_values('imdb_score', ascending=False)
            if top:
                data.movie = data.movie.head(int(top))
            data.genre = data.genre[data.genre['index'].isin(data.movie.index.values.tolist())]
            data.keyword = data.keyword[data.keyword['index'].isin(data.movie.index.values.tolist())]

            return data


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


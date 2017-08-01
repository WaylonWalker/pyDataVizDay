from jinja2 import Template
from IPython.display import IFrame, HTML
import os
import json
from .base_plotter import IPlotter
import math


class C3Plotter(IPlotter):
    """
    Class for creating c3.js charts in ipython notebook
    """

    head = '''
        <!-- Load c3.css -->
        <link href='https://cdnjs.cloudflare.com/ajax/libs/c3/0.4.10/c3.min.css' rel='stylesheet' type='text/css'/>
        <!-- Load d3.js and c3.js -->
        <script src='http://d3js.org/d3.v3.min.js' charset='utf-8'></script>
        <script src='http://cdnjs.cloudflare.com/ajax/libs/c3/0.4.10/c3.min.js'></script>
        <style>{{custom_css}}</style>

    '''

    template = '''
        <h1>{{title}}</h1>
        <div id={{div_id}} style='width: 100%; height: 100%'></div>
        <script>
            var {{div_id}} = document.getElementById('{{div_id}}');
            var data = {{data}};
            data['axis']['y']['tick']['format'] = d3.format('{{y_axis_tick_format}}')
            data['axis']['y2']['tick']['format'] = d3.format('{{secondary_y_axis_tick_format}}')
            data['bindto']='#{{div_id}}'
            var {{div_id}} = c3.generate(data);
        </script>
    '''

    def __init__(self):
        super(C3Plotter, self).__init__()

    def render(self,
     data,
     div_id="chart",
               custom_css='',
               title="",
                head="",
               y_axis_tick_format='',
                secondary_y_axis_tick_format=''
               ,
                **kwargs):
        '''
        render the data in HTML template
        '''
        try:
            data = self.pandas_data(data, **kwargs)
        except AttributeError:
            pass

        if not self.is_valid_name(div_id):
            raise ValueError(
                "Name {} is invalid. Only letters, numbers, '_', and '-' are permitted ".format(
                    div_id))

        return Template(head + self.template).render(
            div_id=div_id.replace(" ", "_"),
            custom_css=custom_css,
            title=title,
            y_axis_tick_format=y_axis_tick_format,
            secondary_y_axis_tick_format=secondary_y_axis_tick_format,
            data=json.dumps(
                data, indent=4).replace("'", "\\'").replace('"', "'"))

    def plot_and_save(self,
                      data,
                      w=800,
                      h=430,
                      filename='chart',
                      subplots=False,
                      subplot_groups=False,
                      title=False,
                      overwrite=True):
        '''
        save the rendered html to a file and returns an IFrame to display the plot in the notebook
        '''
        self.save(data, filename, overwrite,)
        return IFrame(filename + '.html', w, h)

    def plot(self,
                 data,
                 w=800,
                 h=430,
                 div_id='chart',
                 subplots=False,
                 subplot_groups=False,
                 title=False,
                 **kwargs):
        '''
        output an iframe containing the plot in the notebook without saving
        '''

        if subplots:
            if title:
                if len(title) > 0:
                    title = title + '<br>'
            body = ''

            if not subplot_groups:
                subplot_groups = {col: [col] for col in data.columns}

            for group in subplot_groups:
                body = body + (self.render(data=data[subplot_groups[group]],
                                           div_id=str(div_id) + str(group),
                                           head=self.head,
                                           title=str(title) + str(group),
                                           **kwargs
                                           )
                               )
                title=''
        else:
            body = self.render(
                data=data,
                div_id=div_id,
                head=self.head,
                **kwargs)

        return HTML(self.iframe.format(source=body, w=w, h=h*len(subplot_groups)))

    def update():
        pass

    def save(self, data, filename='chart', overwrite=True):
        '''
        save the rendered html to a file in the same directory as the notebook
        '''
        try:
            data = self.pandas_data(data, **kwargs)
        except AttributeError:
            pass

        html = self.render(data=data, div_id=filename, head=self.head)
        if overwrite:
            with open(filename.replace(" ", "_") + '.html', 'w') as f:
                f.write(html)
        else:
            if not os.path.exists(filename.replace(" ", "_") + '.html'):
                with open(filename.replace(" ", "_") + '.html', 'w') as f:
                    f.write(html)
            else:
                raise IOError('File Already Exists!')

    def pandas_data(self, 
                    df, 
                    colors=False, 
                    data_label_formats=False,
                    data_labels=False, 
                    grid=False,
                    group=False, 
                    height=300, 
                    hue=False,
                    kind='line',
                    kinds=None, 
                    legend=True, 
                    mark_right=False, 
                    point=False,
                    secondary_y=list(), 
                    stacked=False,  
                    subchart=False, 
                    subplots=False,
                    tick_count=10, 
                    value=False,
                    value_labels=False,
                    x_axis_tick_culling=False,
                    x_axis_type='auto',
                    x_tick_values=False, 
                    xlabels=False, 
                    xlim=False, 
                    xregions=False, 
                    xy_rotated=False,
                    ylabels=False,
                    ylim=False,
                    yregions=False,
                    zoom=False,
                    ):
        '''
        create data dictionary from pandas DataFrame

        TODO:
        ## Pandas Features
        * proper docstring
        * subplots
        * layout
        * height -> figsize
        * use_index
        * legend
        * xlim (axis.x.min, axis.x.max or axis.x.extent)
        * ylim
        * colorbar
        * table
        * axis-rotation
        ## Seaborn-esque features
        * hue - ability to provide long form data
        ## C3 Features
        * interaction: {enabled: false}
        * transition: {duration: 500}
        * onrendered: function() {...}
        * onmouseover/out
        * data.empty.label.text
        * data.selection.enabled
        * data.selection.grouped
        * data.selection.multiple
        * data.selection.draggable
        * axis.x.tick.fit
        * axis.x.tick.values
        * axis.x.tick.rotate
        * axis.x.label
        * axis.x.show
        * legend.hide
        * legend.position
        * tooltip.show
        * tooltip.grouped
        * point.focus.expand.enabled
        * subchart.size.height
        * point.focus.expand.r
        * point.select.r
        * line.connectNull


        param kind: str
        * line
        * spline
        * step
        * areas
        * area-spline
        * area-step
        * bar
        * scatter
        * pie
        * donut
        * gauge

        param x_axis_type: str
        * timeseries
        * category
        * numeric

        '''
        # kinds = ['line', 'spline', 'step', 'area','area-spline', 'area-step',
        #          'bar', 'scatter', 'pie', 'donut', 'gauge']

        data = {
            'size': {
                'height': height,
            },
            "data": {
                'x': 'x',
                'axes': dict()
            },
            'subchart': {
                'show': subchart
            },
            'point': {
                'show': point
            },
            'grid': {
                'x': {
                    'show': grid
                },
                'y': {
                    'show': grid
                }
            },
            'axis': {
                'rotated': xy_rotated,
                'x': {'tick': {'count': tick_count,
                               'values': x_tick_values,
                               'culling': dict(),
                               },
                      },
                'y': {'tick': {'format': ''}},
                'y2': {'tick': {}},
            },
            'zoom': {}

        }
        if kind:
            data['data']['type'] = kind
        if kinds:
            data['data']['types'] = kinds

        if mark_right:
            df = df.rename(
                columns={col: col + '(right)' for col in secondary_y})
            secondary_y = [y + '(right)' for y in secondary_y]
        if hue and value:
            df = df.groupby([df.index.name, hue])[value].sum().unstack()

        df = df.copy()
        df['x'] = df.index
        df['x'] = df['x'].astype('str').values.tolist()

        data['data']['columns'] = [[col] + df[col].values.tolist()
                                   for col in df.columns]
        # data['data']['columns'].extend([['x'] + df.index.astype('str').values.tolist()])
        for col in df.columns:
            if col in secondary_y:
                data['data']['axes'][col] = 'y2'
            else:
                data['data']['axes'][col] = 'y'
        if len(secondary_y) > 0:
            data['axis']['y2']['show'] = True

        if colors:
            # repeat color palette if not long enough
            colors = colors*math.ceil(len(df.columns)/len(colors))
            color_data = {}
            for col, color in zip(df.columns, colors):
                color_data[col] = color
            data['data']['colors'] = color_data

        if x_axis_type == 'auto':
            index_type = str(df.index.dtype)

            if 'date' in index_type:
                data['axis']['x']['type'] = 'timeseries'
                data['axis']['x']['tick']['format'] = '%Y-%m-%d'

            if 'object' in index_type or 'category' in index_type:
                data['axis']['x']['type'] = 'category'
                data['axis']['x']['tick']['culling'][
                    'max'] = x_axis_tick_culling
        else:
            if 'date' in x_axis_type or 'time' in x_axis_type:
                data['axis']['x']['type'] = 'timeseries'
                data['axis']['x']['tick']['format'] = '%Y-%m-%d'

            if 'categor' in x_axis_type or 'str' in x_axis_type:
                data['axis']['x']['type'] = 'category'
                data['axis']['x']['tick']['culling'][
                    'max'] = x_axis_tick_culling

        if xlim:
            data['axis']['x']['min'] = xlim[0]
            data['axis']['x']['max'] = xlim[1]

        if ylim:
            data['axis']['y']['min'] = ylim[0]
            data['axis']['y']['max'] = ylim[1]

        if stacked:
            group = df.columns.values.tolist()
            group.pop(-1)
            group = [group]

        if group:
            data['data']['groups'] = group

        if zoom:
            data['zoom']['enabled'] = True
            data['zoom']['rescale'] = True

        if xregions:
            data['regions'] = [{'axis': 'x', 'start': region[
                0], 'end':region[1]} for region in xregions]

        if yregions:
            data['regions'] = [{'axis': 'y', 'start': region[
                0], 'end':region[1]} for region in yregions]

        if xlabels:
            data['grid']['x']['lines'] = [
                {'value': label[0], 'text': label[1]} for label in xlabels]

        if ylabels:
            data['grid']['y']['lines'] = [
                {'value': label[0], 'text': label[1]} for label in ylabels]

        if data_labels:
            if data_labels == True:
                data_labels = df.drop('x', axis=1).columns
            if data_label_formats:
                data['data']['labels'] = {}
                for column in data_label_formats:
                    data['data']['labels'][column] = data_label_formats[column]
            else:
                data['data']['labels'] = True

        return data

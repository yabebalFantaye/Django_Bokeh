#!/usr/bin/python

from __future__ import division

from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from django.views.generic.base import TemplateView


def home(request):

    ########################## Plot  >> 1 << ##########################
    from bokeh.plotting import *
    from bokeh.resources import CDN
    from bokeh.embed import components
    from random import randint

    n = 200
    x_s = range(0, 7*n, 7)
    y_s = [randint(-10, 10) for _ in range(n)]
    radius = [randint(1,6) for _ in range(n)]
    plot = circle(x_s, y_s, radius=radius, tools=['pan', 'wheel_zoom', 'box_zoom', 'resize', 'hover', 'reset', 'previewsave'])
    script, div = components(plot, CDN)

    ########################## Plot  >> 2 << ##########################
    from bokeh.sampledata.autompg import autompg

    source = ColumnDataSource(autompg.to_dict("list"))
    source.add(autompg["yr"], name="yr")
    plot_config = dict(plot_width=300, plot_height=300, tools="pan,wheel_zoom,box_zoom,resize,reset,previewsave")

    grid_plot_ = gridplot([

        # First let's plot the "yr" vs "mpg" using the plot config above
        # Note that we are supplying our our data source explicitly
        [circle("yr", "mpg", color="blue", title="MPG by Year", source=source, **plot_config),
        # EXERCISE: add another circle renderer for "hp" vs "displ" with color "green" to this
        # list of plots. This renderer should use the same data source as the renderer above,
        # that is what will cause the plots selections to be linked
        circle("hp", "displ", color="green", title="HP vs. Displacement", source=source, **plot_config)],

        [scatter("yr", "mpg", color="blue", title="MPG by Year", source=source, **plot_config),
        # EXERCISE: add another circle renderer for "hp" vs "displ" with color "green" to this
        # list of plots. This renderer should use the same data source as the renderer above,
        # that is what will cause the plots selections to be linked
        scatter("hp", "displ", color="green", title="HP vs. Displacement", source=source, **plot_config)],


        [circle("mpg", "displ", size="cyl", line_color="red", title="MPG vs. Displacement",
         fill_color=None, source=source, **plot_config),
        circle("mpg", "displ", size="cyl", line_color="red", title="MPG vs. Displacement",
         fill_color=None, source=source, **plot_config)],

        [scatter("mpg", "displ", size="cyl", line_color="red", title="MPG vs. Displacement",
         fill_color=None, source=source, **plot_config),
        scatter("mpg", "displ", size="cyl", line_color="red", title="MPG vs. Displacement",
         fill_color=None, source=source, **plot_config)],

        # EXERCISE: add another circle renderer for "mpg" vs "displ", size proportional to "cyl"
        # Set the the line color to be "red" with no fill, and use the same data source again
        # to link selections
        [line("mpg", "displ", size="cyl", line_color="red", title="MPG vs. Displacement",
         fill_color=None, source=source, **plot_config),
        line("mpg", "displ", size="cyl", line_color="red", title="MPG vs. Displacement",
         fill_color=None, source=source, **plot_config)]

        ])
    script_gridplot, div_gridplot = components(grid_plot_, CDN)

    ########################## Plot  >> 3 << ##########################
    import numpy as np
    from six.moves import zip
    from collections import OrderedDict
    from bokeh.objects import HoverTool

    # Create a set of tools to use
    TOOLS="pan,wheel_zoom,box_zoom,reset,hover"

    xx, yy = np.meshgrid(np.arange(0, 101, 4), np.arange(0, 101, 4))
    x = xx.flatten()
    y = yy.flatten()
    N = len(x)
    inds = [str(i) for i in np.arange(N)]
    radii = np.random.random(size=N)*0.4 + 1.7
    colors = [
        "#%02x%02x%02x" % (r, g, 150) for r, g in zip(np.floor(50+2*x), np.floor(30+2*y))
    ]

    # EXERCISE: create a new data field for the hover tool to interrogate. It can be
    # anything you like, but it needs to have the same length as x, y, etc.
    foo = list(itertools.permutations("abcdef"))[:N]
    bar = np.random.normal(size=N)

    # We need to put these data into a ColumnDataSource
    source = ColumnDataSource(
        data=dict(
            x=x,
            y=y,
            radius=radii,
            colors=colors,
            foo=foo,
            bar=bar,
        )
    )

    hover = curplot().select(dict(type=HoverTool))
    hover.tooltips = OrderedDict([
        # add to this
        ("index", "$index"),
        ("(x,y)", "($x, $y)"),
        ("radius", "@radius"),
        ("fill color", "$color[hex, swatch]:fill_color"),
        ("foo", "@foo"),
        ("bar", "@bar"),
    ])

    plot3 = gridplot([[

    # This is identical to the scatter exercise, but adds the 'source' parameter
    circle(x, y, radius=radii, source=source, tools=TOOLS,
            fill_color=colors, fill_alpha=0.6,
            line_color=None, Title="Hoverful Scatter"),

    # EXERCISE (optional) add a `text` renderer to display the index of each circle
    # inside the circle
    text(x, y, text=inds, alpha=0.5, text_font_size="5pt",
         text_baseline="middle", text_align="center", angle=0),
    # We want to add some fields for the hover tool to interrogate, but first we
    # have to get ahold of the tool. We can use the 'select' method to do that.


    ]])

    script_plot3, div_plot3 = components(plot3, CDN)



    return render_to_response('home.html', {
        'script': script,
        'div': div,

        'script_gridplot': script_gridplot,
        'div_gridplot': div_gridplot,

        'script_plot3': script_plot3,
        'div_plot3': div_plot3,

        })

# This Python file uses the following encoding: utf-8
import pyqtgraph as pg
from functools import partial
import numpy as np


class PngDs(pg.PlotDataItem):
    def __init__(self, parentplot=None, params=None, **kwargs):
        super(PngDs, self).__init__(**kwargs)

        properties = [
            "name",
            "source",
            "description",
            "pen",
            "symbol",
            "symbolPen",
            "symbolBrush",
            "symbolSize",
            "xArrayLinSorted",
        ]
        values = [None, None, None, "red", None, None, None, 1, 0]

        for i, p in enumerate(properties):
            if p in kwargs:
                values[i] = kwargs[p]

        self.prop = dict(zip(properties, values))

        parentplot.addItem(self)
        self.sigClicked.connect(partial(parentplot.set_active_dataset, self))
        self.parentplot = parentplot

    def setData(self, **kwargs):
        super(PngDs, self).setData(**kwargs)
        if self._dataset is not None:
            if self._dataset.x is not None:
                self._dataset.x.flags.writeable = (
                    False  # locks displayed array to find them later
                )
            if self._dataset.y is not None:
                self._dataset.y.flags.writeable = (
                    False  # locks displayed array to find them later
                )

            if self.prop["xArrayLinSorted"]:
                self.set_xArrayLinSorted()

    def y_data(self):
        return self._dataset.y

    def x_data(self):
        return self._dataset.x

    def set_xArrayLinSorted(self):
        if self.prop is None or self._dataset is None:
            return
        self.prop["xArrayLinSorted"] = True
        self.x_inc = self._dataset.x[1] - self._dataset.x[0]
        self.x_0 = self._dataset.x[0]

    def unset_xArrayLinSorted(self):
        self.prop["xArrayLinSorted"] = False
        self.x_inc = None
        self.x_0 = None

    def get_x_min(self):
        if self._dataset is not None and self._dataset.x is not None:
            if "xArrayLinSorted" in self.prop and self.prop["xArrayLinSorted"]:
                return self._dataset.x[0]
            else:
                return np.min(self._dataset.x)
        return None

    def get_x_max(self):
        if self._dataset is not None and self._dataset.x is not None:
            if "xArrayLinSorted" in self.prop and self.prop["xArrayLinSorted"]:
                return self._dataset.x[-1]
            else:
                return np.max(self._dataset.x)
        return None

    def get_visible_data(self):
        xmin, xmax = self.parentplot.viewRange()[0]
        x = self._dataset.x
        y = self._dataset.y
        if x is None or y is None:
            return None
        if "xArrayLinSorted" in self.prop and self.prop["xArrayLinSorted"]:
            ind1 = int((xmin - self.x_0) / self.x_inc)
            ind2 = int((xmax - self.x_0) / self.x_inc)
            return x[ind1:ind2], y[ind1:ind2]
        else:
            x2 = x[(x >= xmin) & (x <= xmax)]
            y2 = y[(x >= xmin) & (x <= xmax)]
            return x2, y2

    def get_ybound_in_range(self, xmin, xmax):
        x = self._dataset.x
        y = self._dataset.y
        if x is None or y is None:
            return None
        if "xArrayLinSorted" in self.prop and self.prop["xArrayLinSorted"]:
            ind1 = int((xmin - self.x_0) / self.x_inc)
            ind2 = int((xmax - self.x_0) / self.x_inc)
            y = y[ind1:ind2]
        else:
            x = x[(x >= xmin) & (x <= xmax)]
            y = y[(x >= xmin) & (x <= xmax)]
        return np.min(y), np.max(y)

    def get_y_min(self):
        if self._dataset is not None and self._dataset.y is not None:
            return np.min(self._dataset.y)
        return None

    def get_y_max(self):
        if self._dataset is not None and self._dataset.y is not None:
            return np.max(self._dataset.y)
        return None

    def change_point_color(self, c):
        self.setSymbolPen(c)
        self.prop["SymbolPen"] = c

    def change_line_color(self, c):
        self.setPen(c)
        self.prop["pen"] = c

    def change_point_symbol(self, c):
        self.setSymbol(c)
        self.prop["Symbol"] = c

    def change_point_fill_color(self, c):
        self.setSymbolBrush(c)
        self.prop["SymbolBrush"] = c

    def change_point_size(self, c):
        self.setSymbolSize(c)
        self.prop["SymbolSize"] = c

    def change_name(self, s):
        self.prop["name"] = s
        self.opts["name"] = s
        self.parentplot.getPlotItem().legend.removeItem(self)
        self.parentplot.getPlotItem().legend.addItem(self, s)

    def save(self):
        return [np.array(list(self.prop.items())), self._dataset.x, self._dataset.y]

from PyQt5 import QtWidgets
from optimeed.visualize.graphs import Widget_graphsVisualLite
from optimeed.core import Graphs, Data, SHOW_WARNING, printIfShown, SHOW_INFO
from optimeed.visualize.widgets import Widget_listWithSearch
import numpy as np


class Widget_SAChaosTuner(QtWidgets.QWidget):
    """Class to tune a OpenTURNS Polynomial Chaos fit, used in sensitivity analysis.
    Provides an interface to select fit degree and display information about its quality"""

    def __init__(self):
        super().__init__()
        main_vertical_layout = QtWidgets.QVBoxLayout(self)
        main_vertical_layout.setContentsMargins(0, 0, 0, 0)

        # Widget slider
        self.widget_poldegree = QtWidgets.QSpinBox()
        self.widget_poldegree.setMinimum(0)
        self.widget_poldegree.setMaximum(10)
        self.widget_poldegree.setValue(2)

        self.label_degree = QtWidgets.QLabel("Order: NA")
        self.label_Q2 = QtWidgets.QLabel("Q2: {:.5f} %".format(1.0*100))

        self.button_fit = QtWidgets.QPushButton("Fit")
        self.button_fit.clicked.connect(self.do_fit)

        self.button_copy = QtWidgets.QPushButton("Copy")
        self.button_copy.clicked.connect(self._copy_metamodel)

        horizontalLayout = QtWidgets.QHBoxLayout()
        horizontalLayout.addWidget(self.widget_poldegree)
        horizontalLayout.addWidget(self.button_fit)
        horizontalLayout.addWidget(self.label_degree)
        horizontalLayout.addWidget(self.label_Q2)
        horizontalLayout.addWidget(self.button_copy)

        main_vertical_layout.addLayout(horizontalLayout)

        theGraphs = Graphs()
        g1 = theGraphs.add_graph(updateChildren=False)
        self.data_ideal = Data([], [], x_label='model', y_label='metamodel', legend='Ideal', is_scattered=False)
        self.data_comparison = Data([], [], x_label='model', y_label='metamodel', legend='Predicted', is_scattered=True, symbolsize=5, outlinesymbol=1)
        theGraphs.add_trace(g1, self.data_ideal, updateChildren=False)
        theGraphs.add_trace(g1, self.data_comparison, updateChildren=False)

        self.wg_graphs = Widget_graphsVisualLite(theGraphs, refresh_time=-1)
        main_vertical_layout.addWidget(self.wg_graphs)

        self.updateMethods = set()

        self.SA_chaos = None
        self.add_update_method(self.wg_graphs.update_graphs)
        self.show()

    def _update_children(self):
        for updateMethod in self.updateMethods:
            updateMethod()

    def _copy_metamodel(self):
        theStr = self.SA_chaos.get_metamodel_as_python_method()
        cb = QtWidgets.QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(theStr, mode=cb.Clipboard)
        printIfShown("{}\nCopied to clipboard!".format(theStr), SHOW_INFO)

    def add_update_method(self, childObject):
        self.updateMethods.add(childObject)

    def set_SA(self, SA_chaos):
        """Set sensitivity analysis to fit.

        :param SA_chaos: SensitivityAnalysis_OpenTURNS_Chaos
        """
        self.SA_chaos = SA_chaos
        self.update()

    def do_fit(self):
        self.SA_chaos.set_fit_degree(self.widget_poldegree.value())
        self.update()

    def update(self):
        self.widget_poldegree.setValue(self.SA_chaos.degree_fitted)
        if self.SA_chaos is None:
            printIfShown("Please use method set_SA before!", SHOW_WARNING)
            return
        Q2, outputs_real, outputs_model = self.SA_chaos.check_goodness_of_fit()

        min_value = min(list(outputs_real) + list(outputs_model))
        max_value = max(list(outputs_real) + list(outputs_model))
        self.data_ideal.set_data([min_value, max_value], [min_value, max_value])
        self.data_comparison.set_data(outputs_real, outputs_model)
        self.label_Q2.setText("Q2: {:.5f} %".format(Q2*100))
        self.label_degree.setText("Order: {}".format(self.SA_chaos.degree_fitted))

        self._update_children()


class Widget_SAChaosMonotonicity(QtWidgets.QWidget):
    """
    Provides an interface to visualize the impact of a single parameter.
    The other parameters are frozen using their central point.
    """
    def __init__(self):
        super().__init__()
        main_vertical_layout = QtWidgets.QVBoxLayout(self)
        main_vertical_layout.setContentsMargins(0, 0, 0, 0)

        # Create widgets
        self.listWithSearch = Widget_listWithSearch()
        self.listWithSearch.myListWidget.currentItemChanged.connect(self.update_graphs)

        theGraphs = Graphs()
        g1 = theGraphs.add_graph(updateChildren=False)
        self.monotonicity = Data([], [], x_label='_', y_label='_', is_scattered=False)
        theGraphs.add_trace(g1, self.monotonicity, updateChildren=False)
        self.wg_graphs = Widget_graphsVisualLite(theGraphs, refresh_time=-1)

        main_vertical_layout.addWidget(self.listWithSearch)
        main_vertical_layout.addWidget(self.wg_graphs)

        self.SA_chaos = None
        self.objectiveName = ""
        self.show()

    def set_SA(self, SA_chaos, objectiveName):
        self.SA_chaos = SA_chaos
        self.objectiveName = objectiveName
        self.listWithSearch.set_list([variable.get_attribute_name() for variable in self.SA_chaos.get_SA_params().get_optivariables()])
        self.update_graphs()

    def _generate_points(self,name_selected, N=100):
        """Generate points along variant selected attribute, with others fixed"""
        opti_variables = self.SA_chaos.get_SA_params().get_optivariables()

        array = list()
        theLine = list()
        for variable in opti_variables:
            if variable.get_attribute_name() == name_selected:
                min_value = variable.get_min_value()
                max_value = variable.get_max_value()
                line = np.linspace(min_value, max_value, N)
                theLine = line
            else:
                middle_interval = (variable.get_min_value() + variable.get_max_value())/2
                line = [middle_interval]*N
            array.append(line)
        return np.array(array).transpose(), theLine

    def update_graphs(self):
        try:
            name_selected = self.listWithSearch.get_name_selected()
        except AttributeError:
            return
        inputs, theLine = self._generate_points(name_selected)
        outputs = self.SA_chaos.evaluate_metamodel(inputs)
        self.monotonicity.set_data(theLine, outputs)
        self.monotonicity.set_kwargs({"x_label": str(name_selected), "y_label": str(self.objectiveName)})
        self.wg_graphs.update_graphs()


class Widget_LiveChaosTuner(QtWidgets.QWidget):
    """Higher level widget to tune a 'live Chaos Collection'.
    Allows to select the attribute to fit.
    Embeds the underlying SA tuner and a monotonicity check.
    """
    def __init__(self, theLiveChaos):
        super().__init__()
        # Window split Left-right:
        # Left: Tuning
        # Right: Check monotonicity
        main_horizontal_layout = QtWidgets.QHBoxLayout(self)

        # Layout tuning
        layout_tuning = QtWidgets.QVBoxLayout()
        main_horizontal_layout.addLayout(layout_tuning)

        self.theLiveChaos = theLiveChaos

        self.listWithSearch = Widget_listWithSearch()
        self.SAChaosTuner = Widget_SAChaosTuner()

        self.theLiveChaos.add_update_method(self.update_available_attributes)
        self.listWithSearch.myListWidget.currentItemChanged.connect(self.update_tune_window)

        layout_tuning.addWidget(self.listWithSearch)
        layout_tuning.addWidget(self.SAChaosTuner)
        # Layout monotonicity
        self.SAMonotonicity = Widget_SAChaosMonotonicity()
        main_horizontal_layout.addWidget(self.SAMonotonicity)
        self.listWithSearch.myListWidget.currentItemChanged.connect(self.update_monotonicity_windows)
        self.SAChaosTuner.add_update_method(self.SAMonotonicity.update_graphs)

        # Updates
        self.update_available_attributes()

    def update_available_attributes(self):
        self.listWithSearch.set_list(list(self.theLiveChaos.fitted_chaos.keys()))

    def update_tune_window(self):
        try:
            attribute_name = self.listWithSearch.get_name_selected()
        except AttributeError:
            return
        chaos = self.theLiveChaos.get_chaos(attribute_name)
        self.SAChaosTuner.set_SA(chaos)

    def update_monotonicity_windows(self):
        try:
            attribute_name = self.listWithSearch.get_name_selected()
        except AttributeError:
            return
        chaos = self.theLiveChaos.get_chaos(attribute_name)
        self.SAMonotonicity.set_SA(chaos, attribute_name)

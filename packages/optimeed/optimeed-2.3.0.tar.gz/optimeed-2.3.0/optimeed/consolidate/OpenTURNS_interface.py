from .sensitivity_analysis import SensitivityAnalysis_LibInterface
import openturns as ot
from typing import List
import numpy as np
import math
from optimeed.core.collection import ListDataStruct_Interface


class LiveChaosCollection(ListDataStruct_Interface):
    """Class for live-fitting a PCE, mimicking the behaviour of a collection so that it can be used with LinkDataGraph."""

    def __init__(self, theSensitivityParameters, theCollection, inputs=None):
        self.fitted_chaos = dict()

        self.theSensitivityParameters = theSensitivityParameters
        self.theCollection = theCollection
        if inputs is None:
            inputs = [theCollection.get_list_attributes("device.{}".format(optivariable.get_attribute_name()))
                      for optivariable in theSensitivityParameters.get_optivariables()]
        self.inputs = list(zip(*inputs))
        self.updateMethods = set()

    def _update_children(self):
        for updateMethod in self.updateMethods:
            updateMethod()

    def add_update_method(self, childObject):
        self.updateMethods.add(childObject)

    def save(self, filename):
        """Save the datastructure to filename"""
        pass

    @staticmethod
    def load(filename, **kwargs):
        pass

    def clone(self, filename):
        """Clone the datastructure to a new location"""
        raise NotImplementedError("Polynomial expansion should not be used for that")

    def add_data(self, data_in):
        raise NotImplementedError("Polynomial expansion should not be used for that")

    def get_data_at_index(self, index):
        raise NotImplementedError("Polynomial expansion should not be used for that")

    def get_data_generator(self):
        return
        yield
        # raise NotImplementedError("Polynomial expansion should not be used for that")

    def delete_points_at_indices(self, indices):
        raise NotImplementedError("Polynomial expansion should not be used for that")

    def get_nbr_elements(self):
        raise NotImplementedError("Polynomial expansion should not be used for that")

    def extract_collection_from_indices(self, theIndices):
        raise NotImplementedError("Polynomial expansion should not be used for that")

    def get_list_attributes(self, attributeName):
        """Returns the interpolation of original collection objectives 'attributeName'.
        If the fit has not been performed, fit it.

        :param attributeName:
        :return:
        """
        if not attributeName:
            return []

        SA_chaos = self.get_chaos(attributeName)
        return SA_chaos.evaluate_metamodel(self.inputs)

    def refresh_attribute(self, attributeName):
        if attributeName not in self.fitted_chaos:
            self.fitted_chaos[attributeName] = SensitivityAnalysis_OpenTURNS_Chaos(self.theSensitivityParameters,
                                                                                   self.theCollection.get_list_attributes(attributeName))
            self._update_children()

    def set_degree(self, attributeName, degree):
        self.refresh_attribute(attributeName)
        self.fitted_chaos[attributeName].set_fit_degree(degree)

    def get_chaos(self, attributeName):
        self.refresh_attribute(attributeName)
        return self.fitted_chaos[attributeName]

    def __str__(self):
        return "Chaos Expansion Fit"


class SensitivityAnalysis_OpenTURNS_Chaos(SensitivityAnalysis_LibInterface):
    """Polynomial chaos expansions based.
    Sobol indices are computed from metamodel."""

    def __init__(self, theSensitivityParameters, theObjectives):
        super().__init__(theSensitivityParameters, theObjectives)
        self.chaosresult = None
        self.objectives_fitted = list()
        self.degree_fitted = 1

    @staticmethod
    def sample_sobol(theOptimizationVariables, N):
        distributionList = [ot.Uniform(variable.get_min_value(), variable.get_max_value()) for variable in theOptimizationVariables]
        distribution = ot.ComposedDistribution(distributionList)
        inputDesign = ot.SobolIndicesExperiment(distribution, N, True)
        return inputDesign.generate()

    def get_sobol_S1(self):
        chaosSI = ot.FunctionalChaosSobolIndices(self.get_chaos())
        return [chaosSI.getSobolIndex(i) for i in range(len(self.theSensitivityParameters.get_optivariables()))]

    def get_sobol_S1conf(self):
        """Not available using Chaos Expansion"""
        return [0.0]*len(self.get_SA_params().get_optivariables())

    def get_sobol_ST(self):
        chaosSI = ot.FunctionalChaosSobolIndices(self.get_chaos())
        return [chaosSI.getSobolTotalIndex(i) for i in range(len(self.get_SA_params().get_optivariables()))]

    def get_sobol_STconf(self):
        """Not available using Chaos Expansion"""
        return [0.0] * len(self.get_SA_params().get_optivariables())

    def get_sobol_S2(self):
        N = len(self.get_SA_params().get_optivariables())
        a = np.empty((N, N,))
        a[:] = np.nan
        for i in range(N):
            for j in range(N):
                if i != j:
                    chaosSI = ot.FunctionalChaosSobolIndices(self.get_chaos())
                    a[i, j] = chaosSI.getSobolIndex([i, j])
        return a

    @staticmethod
    def _end_training_index(outputs):
        return int(0.7*len(outputs))

    def get_chaos(self):
        if not self.performed:  # Perform the fit
            end_training = self._end_training_index(self.theObjectives)
            subset_objectives = self.theObjectives[0:end_training]
            subset_inputs = self.get_SA_params().get_paramvalues()[0:end_training]

            variables = self.get_SA_params().get_optivariables()
            marginals = [ot.Uniform(variable.get_min_value(), variable.get_max_value()) for variable in variables]
            d = ot.ComposedDistribution(marginals)
            polynomials = [ot.StandardDistributionPolynomialFactory(m) for m in marginals]
            basis = ot.OrthogonalProductPolynomialFactory(polynomials)
            total_size = basis.getEnumerateFunction().getStrataCumulatedCardinal(self.degree_fitted)
            adaptive = ot.FixedStrategy(basis, total_size)

            chaosalgo = ot.FunctionalChaosAlgorithm(subset_inputs, [[obji] for obji in subset_objectives], d, adaptive)
            chaosalgo.run()
            self.chaosresult = chaosalgo.getResult()
            self.objectives_fitted = subset_objectives
            self.performed = True
        return self.chaosresult

    def get_metamodel(self):
        return self.get_chaos().getMetaModel()

    def get_metamodel_as_python_method(self):
        arg_name = "theDevice"
        theStr = "def mymetamodel({}):\n".format(arg_name)

        for k, optiVariable in enumerate(self.get_SA_params().get_optivariables()):
            a, b, n = optiVariable.get_min_value(), optiVariable.get_max_value(), optiVariable.get_attribute_name()
            T1 = 2/(b-a)
            T2 = -(a+b)/(b-a)
            if T2 < 0:
                theStr += "    x{} = {}*{}.{} - {}\n".format(k, T1, arg_name, n, -T2)
            else:
                theStr += "    x{} = {}*{}.{} + {}\n".format(k, T1, arg_name, n, T2)
        theComposedMetamodel = str(self.get_chaos().getComposedMetaModel())
        theStr += "    return {}\n".format(theComposedMetamodel.replace("^", "**"))
        return theStr

    def evaluate_metamodel(self, inputs):
        return np.array(self.get_metamodel()(np.array(inputs))).flatten()

    def set_fit_degree(self, degree):
        self.degree_fitted = degree
        self.performed = False

    def check_goodness_of_fit(self):
        end_training = self._end_training_index(self.theObjectives)
        inputs = self.get_SA_params().get_paramvalues()[end_training:]
        outputs_real = self.theObjectives[end_training:]
        outputs = [[obji] for obji in outputs_real]
        theMetaModel = self.get_metamodel()

        val = ot.MetaModelValidation(inputs, outputs, theMetaModel)
        Q2 = val.computePredictivityFactor()[0]
        outputs_model = self.evaluate_metamodel(inputs)
        return Q2, outputs_real, outputs_model


class SensitivityAnalysis_OpenTURNS(SensitivityAnalysis_LibInterface):
    degree_fitted: int
    coefficients: List[List[float]]

    def __init__(self, theSensitivityParameters, theObjectives):
        super().__init__(theSensitivityParameters, theObjectives)
        self.SA = None

    @staticmethod
    def sample_sobol(theOptimizationVariables, N):
        distributionList = [ot.Uniform(variable.get_min_value(), variable.get_max_value()) for variable in theOptimizationVariables]
        distribution = ot.ComposedDistribution(distributionList)
        raw_sample = ot.SobolIndicesExperiment(distribution, N, True).generate()
        return np.array(raw_sample)

    def get_sobol_S1(self):
        return self._get_SA().getFirstOrderIndices()

    def get_sobol_S1conf(self):
        try:
            intervals = self._get_SA().getFirstOrderIndicesInterval()
            lower_bounds = intervals.getLowerBound()
            upper_bounds = intervals.getUpperBound()
            return [up - (low+up)/2 for low, up in zip(lower_bounds, upper_bounds)]
        except TypeError:
            return [0.0]*len(self.get_SA_params().get_optivariables())

    def get_sobol_ST(self):
        return self._get_SA().getTotalOrderIndices()

    def get_sobol_STconf(self):
        try:
            intervals = self._get_SA().getTotalOrderIndicesInterval()
            lower_bounds = intervals.getLowerBound()
            upper_bounds = intervals.getUpperBound()
            return [up - (low+up)/2 for low, up in zip(lower_bounds, upper_bounds)]
        except TypeError:
            return [0.0]*len(self.get_SA_params().get_optivariables())

    def get_sobol_S2(self):
        return np.matrix(self._get_SA().getSecondOrderIndices())

    def _get_SA(self):
        if not self.performed:
            nb_params = len(self.get_SA_params().get_optivariables())

            # Size of sample
            if nb_params == 2:
                eval_per_sample = (2 + nb_params)
            else:
                eval_per_sample = (2 + 2 * nb_params)
            max_N = int(math.floor(len(self.theObjectives) / eval_per_sample))
            objectives = np.array(self.theObjectives[0:max_N * eval_per_sample])
            params = np.array(self.get_SA_params().get_paramvalues()[0:max_N * eval_per_sample])
            self.SA = ot.SaltelliSensitivityAlgorithm(params, [[obji] for obji in objectives], max_N)
            self.performed = True
        return self.SA


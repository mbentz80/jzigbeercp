from numpy.testing import *
import numpy as N

set_local_path('../..')
from svm.dataset import LibSvmRegressionDataSet, LibSvmTestDataSet
from svm.kernel import *
from svm.predict import *
from svm.regression import *
restore_path()

class test_regression(NumpyTestCase):
    def check_basics(self):
        Model = LibSvmEpsilonRegressionModel
        kernel = LinearKernel()
        Model(kernel)
        Model(kernel, epsilon=0.1)
        Model(kernel, cost=1.0)
        model = Model(kernel, shrinking=False)
        self.assert_(not model.shrinking)

        Model = LibSvmNuRegressionModel
        Model(kernel)
        Model(kernel, nu=0.5)
        model = Model(kernel, 0.5, cache_size=60, tolerance=0.005)
        self.assertEqual(model.cache_size, 60)
        self.assertAlmostEqual(model.tolerance, 0.005)

    def check_epsilon_train(self):
        ModelType = LibSvmEpsilonRegressionModel
        y = [10., 20., 30., 40.]
        x = [N.array([0, 0]),
             N.array([0, 1]),
             N.array([1, 0]),
             N.array([1, 1])]
        traindata = LibSvmRegressionDataSet(y, x)
        testdata = LibSvmTestDataSet(x)
        model = ModelType(LinearKernel(), probability=True)
        results = model.fit(traindata)
        results.predict(testdata)
        results.get_svr_probability()

    def _make_basic_datasets(self):
        labels = [0, 1.0, 1.0, 2.0]
        x = [N.array([0, 0]),
             N.array([0, 1]),
             N.array([1, 0]),
             N.array([1, 1])]
        traindata = LibSvmRegressionDataSet(labels, x)
        testdata = LibSvmTestDataSet(x)
        return traindata, testdata

    def _make_basic_kernels(self, gamma):
        kernels = [
            LinearKernel(),
            PolynomialKernel(3, gamma, 0.0),
            RBFKernel(gamma)
            ]
        return kernels

    def check_epsilon_more(self):
        ModelType = LibSvmEpsilonRegressionModel
        epsilon = 0.1
        cost = 10.0
        modelargs = epsilon, cost
        expected_ys = [
            N.array([0.1, 1.0, 1.0, 1.9]),
            N.array([0.24611273, 0.899866638, 0.90006681, 1.90006681]),
            N.array([0.1, 1.0, 1.0, 1.9])
            ]
        self._regression_basic(ModelType, modelargs, expected_ys)

    def _regression_basic(self, ModelType, modelargs, expected_ys):
        traindata, testdata = self._make_basic_datasets()
        kernels = self._make_basic_kernels(traindata.gamma)
        for kernel, expected_y in zip(kernels, expected_ys):
            args = (kernel,) + modelargs
            model = ModelType(*args)
            results = model.fit(traindata)
            predictions = results.predict(testdata)
            # use differences instead of assertAlmostEqual due to
            # compiler-dependent variations in these values
            diff = N.absolute(predictions - expected_y)
            self.assert_(N.alltrue(diff < 1e-3,axis=0))

    def check_cross_validate(self):
        y = N.random.randn(100)
        x = N.random.randn(len(y), 10)
        traindata = LibSvmRegressionDataSet(y, x)
        kernel = LinearKernel()
        model = LibSvmEpsilonRegressionModel(kernel)
        nr_fold = 10
        mse, scc = model.cross_validate(traindata, nr_fold)

    def check_nu_more(self):
        ModelType = LibSvmNuRegressionModel
        nu = 0.4
        cost = 10.0
        modelargs = nu, cost
        expected_ys = [
            N.array([0.0, 1.0, 1.0, 2.0]),
            N.array([0.2307521, 0.7691364, 0.76930371, 1.769304]),
            N.array([0.0, 1.0, 1.0, 2.0])
            ]
        self._regression_basic(ModelType, modelargs, expected_ys)

    def _make_datasets(self):
        y1 = N.random.randn(50)
        x1 = N.random.randn(len(y1), 10)
        y2 = N.random.randn(5)
        x2 = N.random.randn(len(y2), x1.shape[1])
        trndata1 = LibSvmRegressionDataSet(y1, x1)
        trndata2 = LibSvmRegressionDataSet(y2, x2)
        refy = N.concatenate([y1, y2])
        refx = N.vstack([x1, x2])
        trndata = LibSvmRegressionDataSet(refy, refx)
        testdata = LibSvmTestDataSet(refx)
        return trndata, trndata1, trndata2, testdata

    def _make_kernels(self):
        def kernelf(x, y):
            return N.dot(x, y.T)
        def kernelg(x, y):
            return -N.dot(x, y.T)
        kernels = [LinearKernel()]
        kernels += [RBFKernel(gamma)
                    for gamma in [-0.1, 0.2, 0.3]]
        kernels += [PolynomialKernel(degree, gamma, coef0)
                    for degree, gamma, coef0 in
                    [(1, 0.1, 0.0), (2, -0.2, 1.3), (3, 0.3, -0.3)]]
        #kernels += [SigmoidKernel(gamma, coef0)
        #            for gamma, coef0 in [(0.2, -0.5), (-0.5, 1.5)]]
        kernels += [CustomKernel(f) for f in [kernelf, kernelg]]
        return kernels

    def check_all(self):
        trndata, trndata1, trndata2, testdata = self._make_datasets()
        kernels = self._make_kernels()
        for kernel in kernels:
            pctrndata1 = trndata1.precompute(kernel)
            pctrndata = pctrndata1.combine(trndata2)
            models = [
                LibSvmEpsilonRegressionModel(kernel, 1.0, 2.0),
                LibSvmNuRegressionModel(kernel, 0.4, 0.5)
                ]
            fitargs = []
            # CustomKernel needs a precomputed dataset
            if not isinstance(kernel, CustomKernel):
                fitargs += [
                    (trndata, LibSvmPredictor),
                    (trndata, LibSvmPythonPredictor),
                    ]
            fitargs += [
                (pctrndata, LibSvmPredictor),
                (pctrndata, LibSvmPythonPredictor)
                ]
            for model in models:
                refresults = model.fit(*fitargs[0])
                refrho = refresults.rho
                refp = refresults.predict(testdata)
                for args in fitargs[1:]:
                    results = model.fit(*args)
                    self.assertAlmostEqual(results.rho, refrho)
                    p = results.predict(testdata)
                    assert_array_almost_equal(refp, p)

    def check_compact(self):
        traindata, testdata = self._make_basic_datasets()
        kernel = LinearKernel()
        model = LibSvmEpsilonRegressionModel(LinearKernel())
        results = model.fit(traindata, LibSvmPythonPredictor)
        refp = results.predict(testdata)
        results.compact()
        p = results.predict(testdata)
        assert_array_equal(refp, p)

if __name__ == '__main__':
    NumpyTest().run()

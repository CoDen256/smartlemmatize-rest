import unittest

from core.pipelines.abc.abstract_pipeline import Pipeline, AbstractSubmitter, AbstractReceiver, \
    PipelineConnectionException, PipelineExecutionException
from core.pipelines.abc.basic_pipelines import Starter, Finisher, VoidPipeline
from core.pipelines.abc.pipeline_data import PipelineData, PipelineDataException
from core.pipelines.abc.group import PipelineSubmitterGroup, PipelineReceiverGroup


class NamePipeline(Pipeline):

    def __init__(self, name):
        print("\n\nname--")
        super(NamePipeline, self).__init__()
        self.name = name

    def execute(self, incoming_data):
        print(f"{self.name} is executing the data", incoming_data)

        try:
            names = incoming_data.get("names")
        except PipelineDataException:
            names = []

        names.append(self.name)
        self.submit(names=names)

    def __repr__(self):
        return self.name


class ZeroDivisionPipeline(Pipeline):
    def execute(self, incoming_data):
        i = 1 / 0
        i += 1

    def __init__(self):
        super(ZeroDivisionPipeline, self).__init__()

class Void(VoidPipeline):
    def run(self, incoming_data):
        pass


class TestPipeline(unittest.TestCase):

    def setUp(self):
        self.starter = Starter(start="start")
        self.finisher = Finisher()
        self.alpha = NamePipeline("alpha")
        self.beta = NamePipeline("beta")
        self.gamma = NamePipeline("gamma")
        self.delta = NamePipeline("delta")
        self.omega = NamePipeline("omega")

        self.all_pipelines = [self.starter, self.alpha, self.beta, self.gamma, self.delta, self.omega, self.finisher]

    def test_disconnect(self):
        self.alpha.to(self.beta).to(self.gamma).to(self.delta)
        for p in self.all_pipelines:
            p.disconnect()

        self.assert_connections(self.alpha, [], [])
        self.assert_connections(self.beta, [], [])
        self.assert_connections(self.gamma, [], [])
        self.assert_connections(self.delta, [], [])
        self.assert_connections(self.omega, [], [])

    def test_wrong_connections(self):
        self.assertRaises(PipelineConnectionException,
                          lambda: self.starter.to(self.beta, self.alpha.to(self.beta), self.gamma))

        self.assertRaises(PipelineConnectionException,
                          lambda: self.starter.to(self.beta, self.alpha.from_(self.gamma)))

        self.assertRaises(PipelineConnectionException,
                          lambda: self.finisher.from_(self.beta, self.alpha.from_(self.gamma)))

        self.assertRaises(PipelineConnectionException,
                          lambda: self.finisher.from_(self.beta, self.alpha.to(self.gamma)))

    def test_submitter_group(self):
        group = self.starter.to(self.alpha, self.beta, self.gamma)
        self._test_group(group, PipelineSubmitterGroup, [self.alpha, self.beta, self.gamma])

    def test_double_submitter_group(self):
        group = self.starter.to(self.alpha, self.beta).to(self.gamma)
        self._test_group(group, PipelineSubmitterGroup, [self.gamma])

    def test_receiver_group(self):
        group = self.gamma.from_(self.alpha, self.beta, self.omega)
        self._test_group(group, PipelineReceiverGroup, [self.alpha, self.beta, self.omega])

    def test_double_receiver_group(self):
        group = self.finisher.from_(self.delta, self.omega).from_(self.gamma)
        self._test_group(group, PipelineReceiverGroup, [self.gamma])

    def _test_group(self, group, target_type, target_pipelines):
        self.assertIsInstance(group, target_type)
        self.assertEquals(group.pipelines, target_pipelines)

    def test_self_connection(self):
        self.assertRaises(PipelineConnectionException, lambda: self.alpha.to(self.beta, self.gamma, self.alpha))

    def test_diamond_chain(self):

        self.starter.to(self.alpha, self.beta).to(self.gamma)
        self.finisher.from_(self.delta, self.omega).from_(self.gamma)

        self.assert_connections(self.starter, inc=[], out=[self.alpha, self.beta])
        self.assert_connections(self.alpha, inc=[self.starter], out=[self.gamma])
        self.assert_connections(self.beta, inc=[self.starter], out=[self.gamma])
        self.assert_connections(self.gamma, inc=[self.delta, self.omega], out=[self.alpha, self.beta])
        self.assert_connections(self.delta, inc=[self.gamma], out=[self.finisher])
        self.assert_connections(self.omega, inc=[self.gamma], out=[self.finisher])
        self.assert_connections(self.finisher, inc=[self.delta, self.omega], out=[])

    def test_complex_connections(self):
        self.starter.to(self.alpha).to(self.beta).to(self.delta, self.gamma).to(self.omega).to(self.finisher)
        self.finisher.from_(self.starter, self.beta)

        self.assert_connections(self.starter, inc=[], out=[self.alpha, self.finisher])

        self.assert_connections(self.alpha, inc=[self.starter], out=[self.beta])
        self.assert_connections(self.beta, inc=[self.alpha], out=[self.finisher, self.delta, self.gamma])

        self.assert_connections(self.delta, inc=[self.beta], out=[self.omega])
        self.assert_connections(self.gamma, inc=[self.beta], out=[self.omega])

        self.assert_connections(self.omega, inc=[self.gamma, self.delta], out=[self.finisher])

        self.assert_connections(self.finisher, inc=[self.starter, self.beta, self.omega], out=[])

    def test_data_intersection(self):

        self.starter.to(self.alpha, self.beta).to(self.finisher)

        self.assertRaises(PipelineDataException, lambda: self.starter.start())

    def test_wrong_data_key(self):
        self.starter.to(self.finisher)
        self.starter.start()
        result = self.finisher.get_result()
        self.assertRaises(PipelineDataException, lambda: result.get("wrong"))

    def test_data_execution_exception(self):
        wrong = ZeroDivisionPipeline()

        self.starter.to(wrong)

        try:
            self.starter.start()
        except Exception as e:
            self.assertIsInstance(e, PipelineExecutionException)
            self.assertIsInstance(e.cause, ZeroDivisionError)

    def test_execution_not_started(self):
        self.starter.to(self.alpha).to(self.beta).to(self.finisher)
        self.assertRaises(PipelineExecutionException, lambda: self.finisher.get_result())

    def test_no_incoming_pipelines_on_result(self):
        self.assertRaises(PipelineConnectionException, lambda: self.finisher.get_result())

    def test_data_submission(self):

        self.starter.to(self.alpha).to(self.beta)

        self.finisher.from_(self.starter, self.beta)

        self.starter.start()
        result = self.finisher.get_result()

        self.assertTrue(isinstance(result, PipelineData))
        self.assertEqual(result.get_data(), {
            'start': 'start',  # came from starter
            'names': ['alpha', 'beta']  # came from beta (who received only {'names':['alpha']}
        })

    def test_void_pipeline(self):
        self.starter.to(Void()).to(Void()).to(Void()).to(self.finisher)

        self.starter.start()
        result = self.finisher.get_result()

        self.assertTrue(isinstance(result, PipelineData))
        self.assertEqual(result.get_data(), self.starter.start_data)

    def assert_connections(self, pipeline, inc, out):
        if pipeline is AbstractReceiver:
            self.assertEquals(pipeline.incoming_pipelines, inc, type(pipeline).__name__)
        if pipeline is AbstractSubmitter:
            self.assertEquals(pipeline.outcoming_pipelines, out, type(pipeline).__name__)


if __name__ == '__main__':
    unittest.main()

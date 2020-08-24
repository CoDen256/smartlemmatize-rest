import unittest

from core.pipelines.abstract_pipeline import Pipeline, PipelineExecutionException
from core.pipelines.basic_pipelines import VoidPipeline, Starter, Finisher
from core.pipelines.pipeline_data import PipelineData


class TestPipeline(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()

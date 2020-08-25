class PipelineGroup:
    def __init__(self, pipelines):
        self.pipelines = list(pipelines)


class PipelineSubmitterGroup(PipelineGroup):
    def __init__(self, pipelines):
        super(PipelineSubmitterGroup, self).__init__(pipelines)

    def to(self, *to_pipelines):
        for from_pipeline in self.pipelines:
            from_pipeline.to(*to_pipelines)
        return PipelineSubmitterGroup(to_pipelines)


class PipelineReceiverGroup(PipelineGroup):
    def __init__(self, pipelines):
        super(PipelineReceiverGroup, self).__init__(pipelines)

    def from_(self, *from_pipelines):
        for to_pipeline in self.pipelines:
            to_pipeline.from_(*from_pipelines)
        return PipelineReceiverGroup(from_pipelines)
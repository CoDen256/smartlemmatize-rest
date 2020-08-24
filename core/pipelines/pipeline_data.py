
class PipelineData:
    def __init__(self, submitters):
        # data = {pipeline: {arg:val,..}, pipeline:{..}}
        assert isinstance(submitters, dict)
        if submitters: assert all([isinstance(v, dict) for v in submitters.values()])

        self.submitters = submitters
        self.data = self._merge_dicts(self.submitters.values())

    def get_data(self):
        return self.data

    def get_submitters(self):
        return self.submitters

    def get(self, arg):
        for key in self.data.keys():
            if key == arg:
                return self.data[key]
        return PipelineDataException(self, f"No value for argument {arg} was found")

    def _merge_dicts(self, dict_list):
        assert isinstance(dict_list, list)
        assert all([isinstance(d, dict) for d in dict_list])

        base = {}
        for dic in dict_list:
            common = set(dic.keys()) & set(base.keys())
            if common and dic[common] != base[common]:
                raise PipelineDataException(self, "Merging two inputs has discovered argument intersections")
            base.update(dic)
        return base

    @staticmethod
    def of(**data):
        return PipelineData({None: data})


class PipelineDataException(Exception):
    def __init__(self, p_input, *args):
        super().__init__(*args)
        self.p_input = p_input

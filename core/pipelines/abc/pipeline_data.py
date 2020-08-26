
class PipelineData:
    def __init__(self, submitters):
        # data = {pipeline: {arg:val,..}, pipeline:{..}}
        assert isinstance(submitters, dict)
        if submitters: assert all([isinstance(v, dict) for v in submitters.values()])

        self.submitters = submitters
        self.data = self._merge_dicts(list(self.submitters.values()))

    def get_data(self):
        return self.data

    def get_submitters(self):
        return self.submitters

    def get(self, arg):
        for key in self.data.keys():
            if key == arg:
                return self.data[key]
        raise PipelineDataException(self, f"No value for argument {arg} was found")

    def _merge_dicts(self, dict_list):
        assert isinstance(dict_list, list)
        assert all([isinstance(d, dict) for d in dict_list])

        base = {}
        for dic in dict_list:
            common = set(dic.keys()) & set(base.keys())
            for c in common:
                if dic[c] != base[c]:
                    raise PipelineDataException(self, f"Merging two inputs has discovered argument intersections for argument: {c} ({dic[c]} != {base[c]})")
            base.update(dic)
        return base

    @staticmethod
    def of(**data):
        return PipelineData({None: data})

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()


class PipelineDataException(Exception):
    def __init__(self, p_input, *args):
        super().__init__(*args)
        self.p_input = p_input

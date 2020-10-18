from ..pyclass import autoclass, JString, JArrayList
import json

class Feature:
   def name(self):
        return self.extractor.getName()

class AvgICTF(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.AvgICTF')
        self.extractor = Jclass()

class AvgIDF(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.AvgIDF')
        self.extractor = Jclass()

class BM25(Feature):
    def __init__(self, k1=0.9, b=0.4):
        Jclass = autoclass('io.anserini.ltr.feature.base.BM25')
        self.extractor = Jclass(k1, b)

class LMDir(Feature):
    def __init__(self,mu=1000):
        Jclass = autoclass('io.anserini.ltr.feature.base.LMDir')
        self.extractor = Jclass(mu)

class DRF_GL2(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.DFR_GL2')
        self.extractor = Jclass()

class DFR_In_expB2(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.DFR_In_expB2')
        self.extractor = Jclass()

class DocSize(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.DocSize')
        self.extractor = Jclass()

class MatchingTermCount(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.MatchingTermCount')
        self.extractor = Jclass()

class QueryLength(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.QueryLength')
        self.extractor = Jclass()

class AvgSCQ(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.AvgSCQ')
        self.extractor = Jclass()

class SCS(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.SCS')
        self.extractor = Jclass()

class SumMatchingTF(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.SumMatchingTF')
        self.extractor = Jclass()

class UniqueTermCount(Feature):
    def __init__(self):
        Jclass = autoclass('io.anserini.ltr.feature.base.UniqueTermCount')
        self.extractor = Jclass()

class UnorderedSequentialPairs(Feature):
    def __init__(self, gap=8):
        Jclass = autoclass('io.anserini.ltr.feature.UnorderedSequentialPairs')
        self.extractor = Jclass(gap)

class OrderedSequentialPairs(Feature):
    def __init__(self, gap=8):
        Jclass = autoclass('io.anserini.ltr.feature.OrderedSequentialPairs')
        self.extractor = Jclass(gap)

class UnorderedQueryPairs(Feature):
    def __init__(self, gap=8):
        Jclass = autoclass('io.anserini.ltr.feature.UnorderedQueryPairs')
        self.extractor = Jclass(gap)

class OrderedQueryPairs(Feature):
    def __init__(self, gap=8):
        Jclass = autoclass('io.anserini.ltr.feature.OrderedQueryPairs')
        self.extractor = Jclass(gap)

class FeatureExtractor:
    def __init__(self, index_dir, worker_num=1):
        JFeatureExtractorUtils = autoclass('io.anserini.ltr.FeatureExtractorUtils')
        self.utils = JFeatureExtractorUtils(JString(index_dir), worker_num)
        self.feature_name = []

    def add(self, pyclass):
        """
        add feature extractor; cannot add feature extractors in the middle of extraction
        Parameters
        ----------
        pyclass: Feature
            an initialized feature extractor

        """
        self.utils.add(pyclass.extractor)
        self.feature_name.append(pyclass.name())

    def feature_names(self):
        """
        get all feature names
        Returns
        -------
        List[str]   all the feature names in order
        """
        return self.feature_name

    def lazy_extract(self, qid, query_tokens, doc_ids):
        """
        sumbit tasks to workers
        Parameters
        ----------
        qid: str
            unique query id
        query_tokens: List[str]
            tokenized query
        doc_ids: List[str]
            doc id we need to extract on

        """
        input = {'qid': qid, 'queryTokens': query_tokens, 'docIds': doc_ids}
        self.utils.lazyExtract(JString(json.dumps(input)))

    def get_result(self, qid):
        """
        get task result by query id; this call will be blocked until the task is finished
        Parameters
        ----------
        qid: str
         unique query id; mush be the same id that is used to submit the task

        Returns
        -------
        dict: a parsed json

        """
        res = self.utils.getResult(JString(qid))
        return json.loads(res)




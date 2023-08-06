from Corpus.Corpus cimport Corpus
from DependencyParser.ParserEvaluationScore cimport ParserEvaluationScore

cdef class UniversalDependencyTreeBankCorpus(Corpus):

    cdef str language
    cpdef ParserEvaluationScore compareParses(self, UniversalDependencyTreeBankCorpus corpus)

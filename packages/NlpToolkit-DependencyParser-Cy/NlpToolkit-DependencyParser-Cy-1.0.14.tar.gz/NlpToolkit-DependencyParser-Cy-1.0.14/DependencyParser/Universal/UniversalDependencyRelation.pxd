from DependencyParser.DependencyRelation cimport DependencyRelation
from DependencyParser.ParserEvaluationScore cimport ParserEvaluationScore

cdef class UniversalDependencyRelation(DependencyRelation):

    cdef object __universal_dependency_type
    cpdef ParserEvaluationScore compareRelations(self, UniversalDependencyRelation relation)

from cqlpy._internal.types.null import Null
from cqlpy._internal.types.any import CqlAny
from cqlpy._internal.types.code_system import CodeSystem
from cqlpy._internal.types.code import Code
from cqlpy._internal.types.concept import Concept
from cqlpy._internal.types.date import Date
from cqlpy._internal.types.datetime import DateTime
from cqlpy._internal.types.interval import Interval
from cqlpy._internal.types.quantity import Quantity
from cqlpy._internal.types.value_set import ValueSet
from cqlpy._internal.parameter import Parameter
from cqlpy._internal.types.boolean import Boolean
from cqlpy._internal.types.string import String
from cqlpy._internal.types.decimal import Decimal
from cqlpy._internal.types.long import Long
from cqlpy._internal.types.integer import Integer
from cqlpy._internal.types.list import List

# For reference
# https://cql.hl7.org/09-b-cqlreference.html
# https://rszalski.github.io/magicmethods/

# CQL Structured types implemented as Python classes:
# 1.1 CqlAny
# 1.2 Boolean
# 1.3 Code
# 1.4 CodeSystem
# 1.5 Concept
# 1.6 Date (technically a CQL simple type, but CQL uncertainty and date precision concepts require class implementation)
# 1.7 DateTime (technically a CQL simple type, but CQL uncertainty and date precision concepts require class implementation)
# 1.8 Decimal (float)
# 1.9 Long (int)
# 1.10 Integer (int)
# 1.11 Quantity
# 1.12 Ratio (not yet implemented)
# 1.13 String
# 1.14 Time (not yet implemented, technically a CQL simple type, but CQL uncertainty and time precision concepts require class implementation)
# 1.15 ValueSet (extended to include a codes property)
# 1.16 Vocabulary (not yet implemented)
# Parameter (technically not a type, but implemented as one)

__all__ = [
    "Null",
    "CqlAny",
    "CodeSystem",
    "Code",
    "Concept",
    "Date",
    "DateTime",
    "Interval",
    "Quantity",
    "ValueSet",
    "Parameter",
    "Boolean",
    "String",
    "Decimal",
    "Long",
    "Integer",
    "List",
]

# Copyright (C) 2016-present the asyncpg authors and contributors
# <see AUTHORS file>
#
# This module is part of asyncpg and is released under
# the Apache 2.0 License: http://www.apache.org/licenses/LICENSE-2.0


# GENERATED FROM pg_catalog.pg_type
# DO NOT MODIFY, use tools/generate_type_map.py to update

DEF INVALIDOID = 0
DEF MAXBUILTINOID = 9999
DEF MAXSUPPORTEDOID = 5080

DEF BOOLOID = 16
DEF BYTEAOID = 17
DEF CHAROID = 18
DEF NAMEOID = 19
DEF INT8OID = 20
DEF INT2OID = 21
DEF INT4OID = 23
DEF REGPROCOID = 24
DEF TEXTOID = 25
DEF OIDOID = 26
DEF TIDOID = 27
DEF XIDOID = 28
DEF CIDOID = 29
DEF PG_DDL_COMMANDOID = 32
DEF JSONOID = 114
DEF XMLOID = 142
DEF PG_NODE_TREEOID = 194
DEF SMGROID = 210
DEF TABLE_AM_HANDLEROID = 269
DEF INDEX_AM_HANDLEROID = 325
DEF POINTOID = 600
DEF LSEGOID = 601
DEF PATHOID = 602
DEF BOXOID = 603
DEF POLYGONOID = 604
DEF LINEOID = 628
DEF CIDROID = 650
DEF FLOAT4OID = 700
DEF FLOAT8OID = 701
DEF ABSTIMEOID = 702
DEF RELTIMEOID = 703
DEF TINTERVALOID = 704
DEF UNKNOWNOID = 705
DEF CIRCLEOID = 718
DEF MACADDR8OID = 774
DEF MONEYOID = 790
DEF MACADDROID = 829
DEF INETOID = 869
DEF _TEXTOID = 1009
DEF _OIDOID = 1028
DEF ACLITEMOID = 1033
DEF BPCHAROID = 1042
DEF VARCHAROID = 1043
DEF DATEOID = 1082
DEF TIMEOID = 1083
DEF TIMESTAMPOID = 1114
DEF TIMESTAMPTZOID = 1184
DEF INTERVALOID = 1186
DEF TIMETZOID = 1266
DEF BITOID = 1560
DEF VARBITOID = 1562
DEF NUMERICOID = 1700
DEF REFCURSOROID = 1790
DEF REGPROCEDUREOID = 2202
DEF REGOPEROID = 2203
DEF REGOPERATOROID = 2204
DEF REGCLASSOID = 2205
DEF REGTYPEOID = 2206
DEF RECORDOID = 2249
DEF CSTRINGOID = 2275
DEF ANYOID = 2276
DEF ANYARRAYOID = 2277
DEF VOIDOID = 2278
DEF TRIGGEROID = 2279
DEF LANGUAGE_HANDLEROID = 2280
DEF INTERNALOID = 2281
DEF OPAQUEOID = 2282
DEF ANYELEMENTOID = 2283
DEF ANYNONARRAYOID = 2776
DEF UUIDOID = 2950
DEF TXID_SNAPSHOTOID = 2970
DEF FDW_HANDLEROID = 3115
DEF PG_LSNOID = 3220
DEF TSM_HANDLEROID = 3310
DEF PG_NDISTINCTOID = 3361
DEF PG_DEPENDENCIESOID = 3402
DEF ANYENUMOID = 3500
DEF TSVECTOROID = 3614
DEF TSQUERYOID = 3615
DEF GTSVECTOROID = 3642
DEF REGCONFIGOID = 3734
DEF REGDICTIONARYOID = 3769
DEF JSONBOID = 3802
DEF ANYRANGEOID = 3831
DEF EVENT_TRIGGEROID = 3838
DEF JSONPATHOID = 4072
DEF REGNAMESPACEOID = 4089
DEF REGROLEOID = 4096
DEF REGCOLLATIONOID = 4191
DEF ANYMULTIRANGEOID = 4537
DEF ANYCOMPATIBLEMULTIRANGEOID = 4538
DEF PG_BRIN_BLOOM_SUMMARYOID = 4600
DEF PG_BRIN_MINMAX_MULTI_SUMMARYOID = 4601
DEF PG_MCV_LISTOID = 5017
DEF PG_SNAPSHOTOID = 5038
DEF XID8OID = 5069
DEF ANYCOMPATIBLEOID = 5077
DEF ANYCOMPATIBLEARRAYOID = 5078
DEF ANYCOMPATIBLENONARRAYOID = 5079
DEF ANYCOMPATIBLERANGEOID = 5080

cdef ARRAY_TYPES = (_TEXTOID, _OIDOID,)

BUILTIN_TYPE_OID_MAP = {
    ABSTIMEOID: 'abstime',
    ACLITEMOID: 'aclitem',
    ANYARRAYOID: 'anyarray',
    ANYCOMPATIBLEARRAYOID: 'anycompatiblearray',
    ANYCOMPATIBLEMULTIRANGEOID: 'anycompatiblemultirange',
    ANYCOMPATIBLENONARRAYOID: 'anycompatiblenonarray',
    ANYCOMPATIBLEOID: 'anycompatible',
    ANYCOMPATIBLERANGEOID: 'anycompatiblerange',
    ANYELEMENTOID: 'anyelement',
    ANYENUMOID: 'anyenum',
    ANYMULTIRANGEOID: 'anymultirange',
    ANYNONARRAYOID: 'anynonarray',
    ANYOID: 'any',
    ANYRANGEOID: 'anyrange',
    BITOID: 'bit',
    BOOLOID: 'bool',
    BOXOID: 'box',
    BPCHAROID: 'bpchar',
    BYTEAOID: 'bytea',
    CHAROID: 'char',
    CIDOID: 'cid',
    CIDROID: 'cidr',
    CIRCLEOID: 'circle',
    CSTRINGOID: 'cstring',
    DATEOID: 'date',
    EVENT_TRIGGEROID: 'event_trigger',
    FDW_HANDLEROID: 'fdw_handler',
    FLOAT4OID: 'float4',
    FLOAT8OID: 'float8',
    GTSVECTOROID: 'gtsvector',
    INDEX_AM_HANDLEROID: 'index_am_handler',
    INETOID: 'inet',
    INT2OID: 'int2',
    INT4OID: 'int4',
    INT8OID: 'int8',
    INTERNALOID: 'internal',
    INTERVALOID: 'interval',
    JSONBOID: 'jsonb',
    JSONOID: 'json',
    JSONPATHOID: 'jsonpath',
    LANGUAGE_HANDLEROID: 'language_handler',
    LINEOID: 'line',
    LSEGOID: 'lseg',
    MACADDR8OID: 'macaddr8',
    MACADDROID: 'macaddr',
    MONEYOID: 'money',
    NAMEOID: 'name',
    NUMERICOID: 'numeric',
    OIDOID: 'oid',
    OPAQUEOID: 'opaque',
    PATHOID: 'path',
    PG_BRIN_BLOOM_SUMMARYOID: 'pg_brin_bloom_summary',
    PG_BRIN_MINMAX_MULTI_SUMMARYOID: 'pg_brin_minmax_multi_summary',
    PG_DDL_COMMANDOID: 'pg_ddl_command',
    PG_DEPENDENCIESOID: 'pg_dependencies',
    PG_LSNOID: 'pg_lsn',
    PG_MCV_LISTOID: 'pg_mcv_list',
    PG_NDISTINCTOID: 'pg_ndistinct',
    PG_NODE_TREEOID: 'pg_node_tree',
    PG_SNAPSHOTOID: 'pg_snapshot',
    POINTOID: 'point',
    POLYGONOID: 'polygon',
    RECORDOID: 'record',
    REFCURSOROID: 'refcursor',
    REGCLASSOID: 'regclass',
    REGCOLLATIONOID: 'regcollation',
    REGCONFIGOID: 'regconfig',
    REGDICTIONARYOID: 'regdictionary',
    REGNAMESPACEOID: 'regnamespace',
    REGOPERATOROID: 'regoperator',
    REGOPEROID: 'regoper',
    REGPROCEDUREOID: 'regprocedure',
    REGPROCOID: 'regproc',
    REGROLEOID: 'regrole',
    REGTYPEOID: 'regtype',
    RELTIMEOID: 'reltime',
    SMGROID: 'smgr',
    TABLE_AM_HANDLEROID: 'table_am_handler',
    TEXTOID: 'text',
    TIDOID: 'tid',
    TIMEOID: 'time',
    TIMESTAMPOID: 'timestamp',
    TIMESTAMPTZOID: 'timestamptz',
    TIMETZOID: 'timetz',
    TINTERVALOID: 'tinterval',
    TRIGGEROID: 'trigger',
    TSM_HANDLEROID: 'tsm_handler',
    TSQUERYOID: 'tsquery',
    TSVECTOROID: 'tsvector',
    TXID_SNAPSHOTOID: 'txid_snapshot',
    UNKNOWNOID: 'unknown',
    UUIDOID: 'uuid',
    VARBITOID: 'varbit',
    VARCHAROID: 'varchar',
    VOIDOID: 'void',
    XID8OID: 'xid8',
    XIDOID: 'xid',
    XMLOID: 'xml',
    _OIDOID: 'oid[]',
    _TEXTOID: 'text[]'
}

BUILTIN_TYPE_NAME_MAP = {v: k for k, v in BUILTIN_TYPE_OID_MAP.items()}

BUILTIN_TYPE_NAME_MAP['smallint'] = \
    BUILTIN_TYPE_NAME_MAP['int2']

BUILTIN_TYPE_NAME_MAP['int'] = \
    BUILTIN_TYPE_NAME_MAP['int4']

BUILTIN_TYPE_NAME_MAP['integer'] = \
    BUILTIN_TYPE_NAME_MAP['int4']

BUILTIN_TYPE_NAME_MAP['bigint'] = \
    BUILTIN_TYPE_NAME_MAP['int8']

BUILTIN_TYPE_NAME_MAP['decimal'] = \
    BUILTIN_TYPE_NAME_MAP['numeric']

BUILTIN_TYPE_NAME_MAP['real'] = \
    BUILTIN_TYPE_NAME_MAP['float4']

BUILTIN_TYPE_NAME_MAP['double precision'] = \
    BUILTIN_TYPE_NAME_MAP['float8']

BUILTIN_TYPE_NAME_MAP['timestamp with timezone'] = \
    BUILTIN_TYPE_NAME_MAP['timestamptz']

BUILTIN_TYPE_NAME_MAP['timestamp without timezone'] = \
    BUILTIN_TYPE_NAME_MAP['timestamp']

BUILTIN_TYPE_NAME_MAP['time with timezone'] = \
    BUILTIN_TYPE_NAME_MAP['timetz']

BUILTIN_TYPE_NAME_MAP['time without timezone'] = \
    BUILTIN_TYPE_NAME_MAP['time']

BUILTIN_TYPE_NAME_MAP['char'] = \
    BUILTIN_TYPE_NAME_MAP['bpchar']

BUILTIN_TYPE_NAME_MAP['character'] = \
    BUILTIN_TYPE_NAME_MAP['bpchar']

BUILTIN_TYPE_NAME_MAP['character varying'] = \
    BUILTIN_TYPE_NAME_MAP['varchar']

BUILTIN_TYPE_NAME_MAP['bit varying'] = \
    BUILTIN_TYPE_NAME_MAP['varbit']

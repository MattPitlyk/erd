# coding: utf-8
"""
This module contains functions for creating .dot files that
can be fed into graphviz to create Entity Relationship Diagrams (ERDs).

Example
-------
# Start with list of tuples.
# Each tuple should have two tuples:
#   - First tuple is the source (table, field)
#   - Second tuple is the destination (table, field)

tups = [(('Table A', 'Field 1'), ('Table B', 'Field 4')),
        (('Table A', 'Field 2'), ('Table B', 'Field 3')),
        (('Table B', 'Field 1'), ('Table C', 'Field 1')),
        (('Table A', 'Field 1'), ('Table C', 'Field 4'))]

# From list of tuples, create a table -> field mapping.
table_to_fields_mapping = convert_tuples_to_mapping(mapping_example)

# From the table -> field mapping, create tables string.
tables_str = dict_list_to_table_template(table_to_fields_mapping)

# From the list of tuples, create the relationships string.
relationships_str = list_tups_to_mapping_template(mapping_example)

file_str = file_template.format(tables=tables_str, mappings=relationships_str)

with open('erd.dot', 'w') as f:
    f.write(file_str)

"""

# ## Create ERD 

from typing import List, Dict, Tuple, Any, Set


table_template = """{table_name} [label=<
        <table border="0" cellborder="1" cellspacing="0" cellpadding="4">
            <tr><td bgcolor="{bgcolor}">{table_name}</td></tr>
            {rows}  
        </table>
    >]"""


row_template= """<tr><td port="{field_id}" align="left">{field_name}</td></tr>"""


file_template = """digraph {{ 
    // --------------------------------------------------
    // Box for entities
    // --------------------------------------------------
    node [shape=none, margin=0.7]
    rankdir=LR;
    
    {tables}
    {mappings}
    }}
    """


# Dict of table_name to HTML color. Default is 'lightblue'.
color_table_map = {}


def format_name(s):
    return s.replace(' ', '_')


def convert_tuples_to_mapping(tups: List[Tuple[Tuple[str, str], Tuple[str, str]]]) -> Dict[str, List[str]]:
    """Convert list of tuples to a mapping of table -> List(field) preserving field order."""
    mapping = {}
    for source, dest in tups:
        # No ordered set in Python, so use dict keys to preserve field order while also deduping field names.
        mapping.setdefault(format_name(source[0]), {})[format_name(source[1])] = None
        mapping.setdefault(format_name(dest[0]), {})[format_name(dest[1])] = None
    # Convert field dict keys to lists.
    mapping = {k:list(v.keys()) for k,v in mapping.items()}
    return mapping


def dict_list_to_table_template(d: Dict[str, List[str]]) -> str:
    """Create table portion of dot file from table mapping."""
    all_tables = []
    for tab, list_fields in d.items():
        inner_s = []
        for field in list_fields:
            inner_s.append(row_template.format(field_id=field, field_name=field))
        table_name = tab.replace('.', '__')
        all_tables.append(table_template.format(bgcolor=color_table_map.get(table_name,'lightblue'),
                                                table_name=table_name, 
                                                rows='\n'.join(inner_s)))
    return '\n'.join(all_tables)


def list_tups_to_mapping_template(tups: List[Tuple[Tuple[str, str], Tuple[str, str]]]) -> str:
    """Create relationships portion of dot file form list of tuples."""
    mapping = []
    for tup in tups:
        source, dest = tup
        args = list(source) + list(dest)
        args = [format_name(x) for x in args]
        mapping.append('{}:{} -> {}:{}'.format(*args))
    return '\n'.join(mapping)


def make_erd(tuples: List[Tuple[Tuple[str, str], Tuple[str, str]]]) -> str:
    """Create dot file string from list of tuples that can be written to file."""
    table_to_fields_mapping = convert_tuples_to_mapping(tuples)
    tables_str = dict_list_to_table_template(table_to_fields_mapping)
    relationships_str = list_tups_to_mapping_template(tuples)
    file_str = file_template.format(tables=tables_str, mappings=relationships_str)
    return file_str
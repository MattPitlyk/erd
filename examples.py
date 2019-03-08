# coding: utf-8

"""List of tuples of tuples Tuple[Tuple[str, str], Tuple[str, str]]. 
Each inner tuple is Tuple[table_name, field_name] that IDs a field in a 
table. In each pair of tuples, the the first is the source field and the
second is the destination field."""

import erd

if __name__=='__main__':
    mapping_example = [(('Table A', 'Field 1'), ('Table B', 'Field 4')),
                    (('Table A', 'Field 2'), ('Table B', 'Field 3')),
                    (('Table B', 'Field 1'), ('Table C', 'Field 1')),
                    (('Table A', 'Field 1'), ('Table C', 'Field 4'))]
    s = erd.make_erd(mapping_example)
    with open('erd.dot', 'w') as f:
        f.write(s)

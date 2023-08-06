import warnings

from pynwb import get_class

from hdmf.utils import docval
from pynwb.core import VectorIndex


@docval({'name': 'excitation_source',
         'type': int,
         'doc': 'references rows of ExcitationSourcesTable',
         'default': None},
        {'name': 'photodetector',
         'type': int,
         'doc': 'references rows of PhotodetectorsTable',
         'default': None},
        {'name': 'fluorophores',
         'doc': 'references rows of FluorophoresTable',
         'type': 'array_data',
         'default': None,
         'shape': (None,)},
        {'name': 'location',
         'type': str,
         'doc': 'location of fiber',
         'default': None},
        {'name': 'notes',
         'type': str,
         'doc': 'description of fiber',
         'default': None},
        {'name': 'fiber_model_number',
         'type': str,
         'doc': 'fiber model number',
         'default': None},
        {'name': 'dichroic_model_number',
         'type': str,
         'doc': 'dichroic model number',
         'default': None},
        allow_extra=True)
def add_fiber(self, **kwargs):
    """
    Add a row per fiber to the fibers table
    Checks to see if the tables are properly referenced
    If not, gets their references from the nwbfile
    """
    super(FibersTable, self).add_row(**kwargs)
    referenced_tables = ('excitation_sources', 'photodetectors', 'fluorophores')
    for arg, table in zip(kwargs, referenced_tables):
        col = self[arg].target if isinstance(self[arg], VectorIndex) else self[arg]
        if col.table is None:
            nwbfile = self.get_ancestor(data_type='NWBFile')
            col.table = getattr(nwbfile.lab_meta_data['fiber_photometry'], table)
            if col.table is None:
                warnings.warn(f'Reference to {table} that does not yet exist')


FibersTable = get_class('FibersTable', 'ndx-photometry')
FibersTable.add_fiber = add_fiber

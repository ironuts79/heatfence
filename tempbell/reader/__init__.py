from logging import getLogger

from .abc import Reader
from .thinkpad import ( ThinkpadT4XXReader,
                        ThinkpadE4XXReader )

# oh, no!
logger = getLogger('ReaderFactory')

class ReaderFactory:
    __reader_tag: str = ''
    __reader_cached: Reader = None

    @staticmethod
    def get_reader(vendor: str, model: str) -> Reader or None:
        vendor = vendor.lower()
        model = model.lower()

        tag = "{}_{}".format(vendor, model)

        if ReaderFactory.__reader_cached is not None and ReaderFactory.__reader_tag == tag:
           logger.debug('Return cached reader [{}]'.format(tag))

           return ReaderFactory.__reader_cached
         
        # flush cache
        ReaderFactory.__reader_tag = ''
        ReaderFactory.__reader_cached = None

        if tag.startswith('lenovo'):
            if tag in ['lenovo_thinkpad t490', 'lenovo_thinkpad t495']:
                ReaderFactory.__reader_cached = ThinkpadT4XXReader()
             
            elif tag in ['lenovo_thinkpad e490', 'lenovo_thinkpad e495']:
                ReaderFactory.__reader_cached = ThinkpadE4XXReader()
        
        # set new reader tag
        if ReaderFactory.__reader_cached is not None:
            logger.debug("Create and cache new reader [{}]".format(ReaderFactory.__reader_cached.__class__.__name__))
            ReaderFactory.__reader_tag = tag
        
        # and return
        return ReaderFactory.__reader_cached

__all__ = ( 'ReaderFactory' )

from dknovautils.commons import *

DkAppVer = '0.0.24'
_unknown_err = '_unknown_err4035'


class AT(object):

    @staticmethod
    def checksys():
        assert sys.version_info >= (3, 11)

    @staticmethod
    def fepochMillis() -> int:
        millisec = int(AT.fepochSecs() * 1000)
        return millisec

    @staticmethod
    def fepochSecs() -> float:
        '''
         time.monotonic()

        '''
        return time.monotonic()
        return time.time()

    '''
        # dd/mm/YY H:M:S
    dts = now.strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dts)

    # 20200101T120000
    dts = now.strftime("%Y%m%dT%H%M%S")
    print("date and time =", dts)
    
    
    '''

    @staticmethod
    def sdf_logger():
        pass

    @staticmethod
    def sdf_logger_fomrat_datetime(dt: int = None) -> str:
        # "yyyy-MM-dd HH:mm:ss"

        if dt is not None:
            dt = datetime.fromtimestamp(dt/1000, tz=None)
        else:
            dt = datetime.now()

        dts = dt.strftime("%Y-%m-%d %H:%M:%S")

        return dts

    @staticmethod
    def assert_(b: bool, s: str = None):
        # todo 改成完善的形式
        assert b, _unknown_err if s is None else s
        pass

    @staticmethod
    def astTrace(b: bool, s: str):
        '''在prod中完全不需要的'''
        AT.assert_(b, s)

    @staticmethod
    def unsupported(s: str = None):
        AT.assert_(False, s if s is not None else 'err8255 unsupported 不支持的功能')

    @staticmethod
    def unimplemented(s: str = None):
        AT.assert_(False, s if s is not None else 'err4823 unimplemented 未实现的功能')

    VERSION = DkAppVer


'''

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

logging.basicConfig(filename='/mnt/d/tmp/demo0726.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)





'''

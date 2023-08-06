
import dknovautils
from dknovautils.commons import *

DkAppVer = '0.0.26'
_unknown_err = '_unknown_err4035'


class AT(object):

    _innerLoggerFun_ = None

    _AstErrorCnt_ = 0

    @staticmethod
    def log_basicConfig(filename='my.log', loggerName='dkn', initInnerLoggerFun=True):
        LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
        DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

        logging.basicConfig(filename=filename, level=logging.NOTSET,
                            format=LOG_FORMAT, datefmt=DATE_FORMAT)

        logger = logging.getLogger(loggerName)

        # create logger
        # logger = logging.getLogger('simple_example')
        logger.setLevel(logging.DEBUG)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        def mloggerFun(obj, llevel):
            assert isinstance(llevel, LLevel)
            if False:
                pass
            elif llevel == LLevel.Trace:
                # 也用debug级别。只是在prod模式下可以关闭。
                logger.debug(obj)
            elif llevel == LLevel.Debug:
                logger.debug(obj)
            elif llevel == LLevel.Info:
                logger.info(obj)
            elif llevel == LLevel.Warn:
                logger.warning(obj)
            elif llevel == LLevel.Error:
                logger.error(obj)
            else:
                assert False,f"bad {llevel}"

            pass

        if initInnerLoggerFun:
            AT._innerLoggerFun_ = mloggerFun

        return mloggerFun

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
        # 改成完善的形式

        assert isinstance(b, bool)

        if not b:
            return

        AT._AstErrorCnt_ += 1
        msg = _unknown_err if s is None else s

        dknovautils.commons.iprint_error(msg)

        # assert b,
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

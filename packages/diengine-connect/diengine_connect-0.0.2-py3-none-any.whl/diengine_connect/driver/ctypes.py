import logging
import os

import diengine_connect.driver.dataconv as pydc
import diengine_connect.driver.npconv as pync
from diengine_connect.driver.buffer import ResponseBuffer
from diengine_connect.driver.common import coerce_bool

logger = logging.getLogger(__name__)

RespBuffCls = ResponseBuffer
data_conv = pydc
numpy_conv = pync

if coerce_bool(os.environ.get('DIENGINE_CONNECT_USE_C', True)):
    try:
        from diengine_connect.driverc.buffer import ResponseBuffer as CResponseBuffer
        import diengine_connect.driverc.dataconv as cdc

        data_conv = cdc
        RespBuffCls = CResponseBuffer
        logger.info('Successfully imported Diengine Connect C data optimizations')
    except ImportError as ex:
        CResponseBuffer = None
        logger.warning('Unable to connect optimized C data functions [%s], falling back to pure Python',
                       str(ex))
    try:
        import diengine_connect.driverc.npconv as cnc

        numpy_conv = cnc
        logger.info('Successfully import Diengine Connect C/Numpy optimizations')
    except ImportError as ex:
        logger.warning('Unable to connect Diengine Connect C to Numpy API [%s], falling back to pure Python',
                       str(ex))
else:
    logger.info('Diengine Connect C optimizations disabled')

"""The analysis server. Process raw image to PDF."""
from bluesky.callbacks.zmq import RemoteDispatcher
from databroker.v2 import Broker
from pkg_resources import resource_filename

from pdfstream.pipeline.core import XPDConfig
from pdfstream.pipeline.core import XPDRouter
from .tools import ServerConfig, run_server

CFG = {
    "XPD": resource_filename("pdfstream", "configs/pdf_xpdserver.ini"),
    "PDF": resource_filename("pdfstream", "configs/xpd_xpdserver.ini")
}


class XPDServerConfig(XPDConfig, ServerConfig):
    """The configuration for xpd server."""
    pass


class XPDServer(RemoteDispatcher):
    def __init__(self, config: XPDServerConfig, *, raw_db: Broker = None, an_db: Broker = None):
        super(XPDServer, self).__init__(config.address, prefix=config.prefix)
        self.subscribe(XPDRouter(config, raw_db=raw_db, an_db=an_db))


def make_and_run(cfg: str, *, test_tiff_base: str = None, test_raw_db: Broker = None, test_an_db: Broker = None):
    """Run the xpd data reduction server.

    The server will receive message from proxy and process the data in the message. The processed data will be
    visualized and exported to database and the file system.

    Parameters
    ----------
    cfg :
        The path to configuration .ini file. It also accept a name of default configuration for a specific
        beam line. 'XPD' for xpd beam line, 'PDF' for pdf beam line.

    test_tiff_base :
        A test tiff base option for developers.

    test_raw_db :
        A test database option for developers.

    test_an_db :
        A test database option for developers.
    """
    cfg_file = CFG.get(cfg, cfg)
    config = XPDServerConfig()
    config.read(cfg_file)
    if test_tiff_base:
        config.tiff_base = test_tiff_base
    server = XPDServer(config, raw_db=test_raw_db, an_db=test_an_db)
    run_server(server)

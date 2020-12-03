import typing as tp

from databroker.core import BlueskyRun

from pdfstream.analyzers.base import AnalyzerConfig, Analyzer
from pdfstream.servers.xpd_server import XPDRouter, XPDConfig


class XPDAnalyzerConfig(XPDConfig, AnalyzerConfig):
    """The configuration of the XPDAnalyzer."""
    pass


class XPDAnalyzer(XPDRouter, Analyzer):
    """The class to process the XPD data to PDF data. """
    pass


def replay(run: BlueskyRun) -> tp.Tuple[str, XPDAnalyzerConfig, XPDAnalyzer]:
    """Generate the original data, original configure and the XPD analyzer of it.

    Parameters
    ----------
    run :
        The run containing the processed data.

    Returns
    -------
    uid :
        The uid of the original run.

    config :
        The original configuration.

    analyzer :
        The original analyzer.
    """
    uid = run.metadata['start']['original_run_uid']
    config = XPDAnalyzerConfig()
    config.read_run(run)
    analyzer = XPDAnalyzer(config)
    return uid, config, analyzer

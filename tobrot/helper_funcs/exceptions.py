class DirectDownloadLinkException(Exception):
    """No method found to download from that Direct Link :("""
    pass


class NotSupportedExtractionArchive(Exception):
    """The Archive Format you are trying to Extract Is Not Supported"""
    pass
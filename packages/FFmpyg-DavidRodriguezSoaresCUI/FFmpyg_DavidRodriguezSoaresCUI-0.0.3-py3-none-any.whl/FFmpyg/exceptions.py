""" All business exceptions are declared here
"""


class FfprobeExecutionError(Exception):
    """Used whenever a call to Ffprobe fails to return expected values"""


class FilterComputationFailed(Exception):
    """Something went wrong in the process of computing a complex filter"""

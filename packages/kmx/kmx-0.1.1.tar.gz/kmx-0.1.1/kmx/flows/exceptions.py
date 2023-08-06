class DelayFlowTask(Exception):
    """
    Exception should be raised in task cb to delay its execution on
    `delay` seconds
    """
    def __init__(self, delay: int, *args: object) -> None:
        super().__init__(*args)
        self.delay = delay


class StopFlowRun(Exception):
    """ """

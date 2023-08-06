from typing import Union


class PublicMetrics():
    def __init__(self, view_count: Union[int, None] = None) -> None:
        self.view_count = view_count

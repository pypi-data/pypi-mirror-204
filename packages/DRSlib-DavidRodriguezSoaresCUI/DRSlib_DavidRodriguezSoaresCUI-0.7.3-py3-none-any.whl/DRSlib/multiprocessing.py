"""
Multiprocessing
===============

For when even the most basic parallel processing is
better than nothing
"""
import multiprocessing
from typing import Any, Callable, List, Tuple


class SimpleMultiProcessing:
    """Parallel processing made simpler"""

    @staticmethod
    def apply_kwargs(
        user_function_and_arguments: Tuple[Callable, tuple, dict]
    ) -> Callable:
        """Workaround for imap only taking one argument per thread
        Executes user function with provided arguments"""
        user_function, args, kwargs = user_function_and_arguments
        return user_function(*args, **kwargs)

    @staticmethod
    def bulk_processing(
        user_function: Callable, arguments: List[dict], parallel_instances: int
    ) -> List[Any]:
        """Takes in callable, kwargs arguments for each thread and number of instances
        to execute in parallel at a time. Returns execution's return value in order.
        """
        user_function_and_arguments = [
            (user_function, (), _args) for _args in arguments
        ]
        with multiprocessing.Pool(parallel_instances) as pool:
            return list(
                pool.imap(
                    SimpleMultiProcessing.apply_kwargs, user_function_and_arguments
                )
            )

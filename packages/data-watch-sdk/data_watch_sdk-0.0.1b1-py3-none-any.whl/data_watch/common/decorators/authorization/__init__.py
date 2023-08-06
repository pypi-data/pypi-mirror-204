"""
Authenticated request decorators.
"""
from data_watch.common.decorators.authorization.asynchronous import (
    async_authenticated_request,
)
from data_watch.common.decorators.authorization.synchronous import authenticated_request

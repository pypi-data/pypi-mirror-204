import aiohttp
import typing as tp
from .exceptions import HTTPException

if tp.TYPE_CHECKING:
    import loguru


class HttpClient:
    """
    The HTTP client that NewsDash is using

    Attributes
    ----------
    session : aiohttp.ClientSession, optional
        Custom ClientSession you want the client to use., by default None
    logger: loguru.logger
        The logger used to log information.

    """

    def __init__(
        self,
        *,
        session: tp.Optional[aiohttp.ClientSession] = None,
        logger: "loguru.logger",
    ) -> None:
        """
        Parameters
        ----------
        logger : loguru.logger
            The logger used to log information.
        session : tp.Optional[aiohttp.ClientSession], optional
            The session to use for making requests.

        Returns
        -------
        HttpClient
            The http client.
        """
        self.session = session
        self.logger = logger

    async def connect(self) -> None:
        """
        connect to the http client.
        """
        if self.session is None:
            self.session = aiohttp.ClientSession()
            self.logger.info("successfully connected to the http client")

    async def request(
        self, url: str, method: str, params: dict = {}, headers: dict = {}
    ) -> tp.Any:
        """
        Make requests to api.

        Parameters
        ----------
        url : str
            The url to which request is to be made
        method : str
            The method for making request.
        params : dict, optional
            The params for url for making request, by default {}
        headers : dict, optional
            The headers for url for making request, by default {}

        Returns
        -------
        tp.Any
            The response from api.

        Raises
        ------
        HTTPException.from_response
            If you get bad response codes.
        HTTPException
            If the session is not provided
        """
        if self.session is None:
            await self.connect()
        if self.session is not None:
            async with self.session.request(
                method, url, params=params, headers=headers
            ) as response:
                if 300 > response.status >= 200:
                    return await response.json()
                else:
                    resp = await response.json()
                    message = f"received status code {response.status} with code > {resp['code']}"
                    self.logger.error(message)
                    raise HTTPException.from_response(await response.json())
        else:
            raise HTTPException("No session was provided")

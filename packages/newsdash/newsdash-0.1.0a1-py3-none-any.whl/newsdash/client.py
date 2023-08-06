import typing as tp
from .http import HttpClient
import loguru

if tp.TYPE_CHECKING:
    import aiohttp
    import os
    from types import TracebackType


class NewsDash:
    """
    A class to interact with NewsAPI.

    Attributes
    ----------
    logger : loguru.Logger
        The logger used to log information.
    _http_client : .HttpClient
        The HTTP client used to make requests to the api.

    Examples
    --------
    >>> from newsdash import NewsDash
    >>> import asyncio
    >>> client = NewsDash('YOUR_API_KEY')
    >>> async def get_news():
    ... print(await client.get_everything(query='apple'))
    ... await client.close()
    >>> asyncio.run(get_news())
    """

    def __init__(
        self,
        api_key: str,
        *,
        session: tp.Optional["aiohttp.ClientSession"] = None,
        file_logging: tp.Union[
            bool,
            list[
                "os.PathLike",
                tp.Union[bool, str],
                tp.Union[bool, str],
                tp.Union[bool, str],
            ],
        ] = False,
    ) -> None:
        """
        Parameters
        ----------
        api_key : str
            The api key you get from NewsApi.
        session : typing.Optional[aiohttp.ClientSession], optional
            Custom ClientSession you want the client to use., by default None
        file_logging : typing.Union[bool,list[os.PathLike,typing.Union[bool, str],typing.Union[bool, str],typing.Union[bool, str],],], optional
            Custom ClientSession you want the client to use., by default False

        Returns
        -------
        NewsDash
            The NewsDash client.
        """
        self.logger = loguru.logger
        self.api_key = api_key
        if file_logging != False:
            file = file_logging[0]
            if len(file_logging) > 1 and file_logging[1]:
                rotation = file_logging[1]
            else:
                rotation = None
            if len(file_logging) > 2 and file_logging[2]:
                retention = file_logging[2]
            else:
                retention = None
            if len(file_logging) > 3 and file_logging[3]:
                compression = file_logging[3]
            else:
                compression = None
            self.logger.add(
                file, rotation=rotation, retention=retention, compression=compression
            )
        self._http_client = HttpClient(session=session, logger=self.logger)

    async def __aexit__(
        self,
        exc_type: tp.Optional[tp.Type[BaseException]],
        exc_val: tp.Optional[BaseException],
        exc_tb: tp.Optional["TracebackType"],
    ) -> None:
        if self._http_client.session is not None:
            await self._http_client.session.close()

    async def __aenter__(self) -> "NewsDash":
        return self

    async def close(self) -> None:
        """
        Closes the session, Note- no need to use it if you are using context manager.
        """
        self.logger.info("Closing session")
        if self._http_client.session is not None:
            await self._http_client.session.close()

    @property
    def http_client(self) -> HttpClient:
        """
        The http client NewsDash is using.

        Returns
        -------
        HttpClient
            The http client..
        """
        return self._http_client

    async def get_everything(
        self,
        *,
        query: str,
        searchIn: tp.Literal["title", "description", "body"] = None,
        sources: str = None,
        domains: str = None,
        excludeDomains: str = None,
        date_from: str = None,
        date_to: str = None,
        language: tp.Literal[
            "ar",
            "de",
            "en",
            "es",
            "fr",
            "he",
            "it",
            "nl",
            "no",
            "pt",
            "ru",
            "sv",
            "ud",
            "zh",
        ] = None,
        sortBy: tp.Literal["relevancy", "popularity", "publishedAt"] = None,
        pageSize: int = None,
        page: int = None,
    ) -> tp.Any:
        """
        Get every news from the NewsApi by searching with query and other optional paameters.

        Parameters
        ----------
        query : str
            Keywords or phrases to search for in the article title and body.
        searchIn : typing.Literal["title","description","body"], optional
            The fields to restrict your query search to,by default None
        sources : str, optional
            A comma-seperated string of identifiers (maximum 20) for the news sources or blogs you want headlines from, by default None
        domains : str, optional
            A comma-seperated string of domains (eg bbc.co.uk, techcrunch.com, engadget.com) to restrict the search to, by default None
        excludeDomains : str, optional
            A comma-seperated string of domains (eg bbc.co.uk, techcrunch.com, engadget.com) to remove from the results, by default None
        date_from : str, optional
            A date and optional time for the oldest article allowed. This should be in ISO 8601 format (e.g. 2023-04-17 or 2023-04-17T12:33:30), by default None
        date_to : str, optional
            A date and optional time for the newest article allowed. This should be in ISO 8601 format (e.g. 2023-04-17 or 2023-04-17T12:33:30), by default None
        language : typing.Literal["ar", "de", "en", "es", "fr", "he", "it", "nl", "no", "pt", "ru", "sv", "ud", "zh"], optional
            The 2-letter ISO-639-1 code of the language you want to get headlines for. Possible options: ar de en es fr he it nl no pt ru sv ud zh, by default None
        sortBy : typing.Literal["relevancy", "popularity", "publishedAt"], optional
            The order to sort the articles in. Possible options: relevancy, popularity, publishedAt. relevancy = articles more closely related to q come first. popularity = articles from popular sources and publishers come first. publishedAt = newest articles come first, by default None
        pageSize : int, optional
            The number of results to return per page, by default None
        page : int, optional
            Use this to page through the results, by default None

        Returns
        -------
        typing.Any
            The response from NewsApi after getting news.

        Raises
        ------
        HTTPException
            raises HTTPException if the status code is not `ok`.

        Examples
        -------
        >>> from newsdash import NewsDash
        >>> import asyncio
        >>> async def main():
        ... async with NewsDash('YOUR_API_KEY') as nd:
        ... print(await nd.get_everything(query='apple'))
        >>> asyncio.run(main())
        """
        params = {}
        if query is not None:
            if not isinstance(query, str):
                raise TypeError("query should be a string")
            params["q"] = query
        if searchIn is not None:
            if isinstance(searchIn, str):
                if searchIn not in ["title", "description", "body"]:
                    raise ValueError(
                        "searchIn should be one of 'title', 'description', or 'body'"
                    )
            else:
                raise TypeError("searchIn should be a string")
            params["searchIn"] = searchIn
        if sources is not None:
            if not isinstance(sources, str):
                raise TypeError("sources should be a string")
            params["sources"] = sources
        if domains is not None:
            if not isinstance(domains, str):
                raise TypeError("domains should be a string")
            params["domains"] = domains
        if excludeDomains is not None:
            if not isinstance(excludeDomains, str):
                raise TypeError("excludeDomains should be a string")
            params["excludeDomains"] = excludeDomains
        if date_from is not None:
            if not isinstance(date_from, str):
                raise TypeError("date_from should be a string")
            params["from"] = date_from
        if date_to is not None:
            if not isinstance(date_to, str):
                raise TypeError("date_to should be a string")
            params["to"] = date_to
        if language is not None:
            if isinstance(language, str):
                if language not in [
                    "ar",
                    "de",
                    "en",
                    "es",
                    "fr",
                    "he",
                    "it",
                    "nl",
                    "no",
                    "pt",
                    "ru",
                    "sv",
                    "ud",
                    "zh",
                ]:
                    raise ValueError(
                        "language should be one out of the languages provided by newsapi"
                    )
            else:
                raise TypeError("language should be a string")
            params["language"] = language
        if sortBy is not None:
            if isinstance(sortBy, str):
                if sortBy not in ["relevancy", "popularity", "publishedAt"]:
                    raise ValueError(
                        "sortBy should be one out of relevancy, popularity or publishedAt"
                    )
            else:
                raise TypeError("sortBy should be a string")
            params["sortBy"] = sortBy
        if pageSize is not None:
            if isinstance(pageSize, int):
                if pageSize < 0:
                    raise ValueError("pageSize should be greater than 0")
            else:
                raise TypeError("pageSize should be an integer")
            params["pageSize"] = pageSize
        if page is not None:
            if isinstance(page, int):
                if page < 0:
                    raise ValueError("page should be greater than 0")
            else:
                raise TypeError("page should be an integer")
            params["page"] = page
        headers = {"X-Api-Key": self.api_key}
        data = await self._http_client.request(
            "https://newsapi.org/v2/everything", "GET", headers=headers, params=params
        )
        if data:
            return data

    async def get_top_headlines(
        self,
        *,
        country: tp.Literal[
            "ae",
            "ar",
            "at",
            "au",
            "be",
            "bg",
            "br",
            "ca",
            "ch",
            "cn",
            "co",
            "cu",
            "cz",
            "de",
            "eg",
            "fr",
            "gb",
            "gr",
            "hk",
            "hu",
            "id",
            "ie",
            "il",
            "in",
            "it",
            "jp",
            "kr",
            "lt",
            "lv",
            "ma",
            "mx",
            "my",
            "ng",
            "nl",
            "no",
            "nz",
            "ph",
            "pl",
            "pt",
            "ro",
            "rs",
            "ru",
            "sa",
            "se",
            "sg",
            "si",
            "sk",
            "th",
            "tr",
            "tw",
            "ua",
            "us",
            "ve",
            "za",
        ] = None,
        category: tp.Literal[
            "business",
            "entertainment",
            "general",
            "health",
            "science",
            "sports",
            "technology",
        ] = None,
        sources: str = None,
        query: str = None,
        pageSize: int = None,
        page: int = None,
    ) -> tp.Any:
        """
        Get the top headleines of news from the NewsApi by searching with query and other optional paameters.

        Parameters
        ----------
        country : typing.Literal["ae", "ar", "at", "au", "be", "bg", "br", "ca", "ch", "cn", "co", "cu", "cz", "de", "eg", "fr", "gb", "gr", "hk", "hu", "id", "ie", "il", "in", "it", "jp", "kr", "lt", "lv", "ma", "mx", "my", "ng", "nl", "no", "nz", "ph", "pl", "pt", "ro", "rs", "ru", "sa", "se", "sg", "si", "sk", "th", "tr", "tw", "ua", "us", "ve", "za"], optional
            The 2-letter ISO 3166-1 code of the country you want to get headlines for. Possible options: ae ar at au be bg br ca ch cn co cu cz de eg fr gb gr hk hu id ie il in it jp kr lt lv ma mx my ng nl no nz ph pl pt ro rs ru sa se sg si sk th tr tw ua us ve za, by default None
        category : typing.Literal["business","entertainment","general","health","science","sports","technology"], optional
            The category you want to get headlines for. Possible options: business entertainment general health science sports technology, by default None
        sources : str, optional
            A comma-seperated string of identifiers for the news sources or blogs you want headlines from, by default None
        query : str, optional
            Keywords or a phrase to search for, by default None
        pageSize : int, optional
            he number of results to return per page (request). 20 is the default, 100 is the maximum, by default None
        page : int, optional
            Use this to page through the results if the total results found is greater than the page size, by default None

        Returns
        -------
         typing.Any
            The response from NewsApi after getting news.

        Raises
        ------
        HTTPException
            raises HTTPException if the status code is not `ok`.

        Examples
        -------
        >>> from newsdash import NewsDash
        >>> import asyncio
        >>> async def main():
        ... async with NewsDash('YOUR_API_KEY') as nd:
        ... print(await nd.get_top_headlines(query='apple'))
        >>> asyncio.run(main())
        """
        params = {}
        if country is not None:
            if country not in [
                "ae",
                "ar",
                "at",
                "au",
                "be",
                "bg",
                "br",
                "ca",
                "ch",
                "cn",
                "co",
                "cu",
                "cz",
                "de",
                "eg",
                "fr",
                "gb",
                "gr",
                "hk",
                "hu",
                "id",
                "ie",
                "il",
                "in",
                "it",
                "jp",
                "kr",
                "lt",
                "lv",
                "ma",
                "mx",
                "my",
                "ng",
                "nl",
                "no",
                "nz",
                "ph",
                "pl",
                "pt",
                "ro",
                "rs",
                "ru",
                "sa",
                "se",
                "sg",
                "si",
                "sk",
                "th",
                "tr",
                "tw",
                "ua",
                "us",
                "ve",
                "za",
            ]:
                raise ValueError(
                    "country should be one out of the countries provided by news api"
                )
            params["country"] = country
        if category is not None:
            if category not in [
                "business",
                "entertainment",
                "general",
                "health",
                "science",
                "sports",
                "technology",
            ]:
                raise ValueError(
                    "category should be one out of the categories provided by news api"
                )
            params["category"] = category
        if sources is not None:
            if not isinstance(sources, str):
                raise TypeError("sources should be an string")
            params["sources"] = sources
        if query is not None:
            if not isinstance(query, str):
                raise TypeError("query should be an string")
            params["q"] = query
        if pageSize is not None:
            if not isinstance(pageSize, int):
                raise TypeError("pageSize should be an integer")
            params["pageSize"] = pageSize
        if page is not None:
            if not isinstance(page, int):
                raise TypeError("page should be an integer")
            params["page"] = page
        headers = {"X-Api-Key": self.api_key}
        data = await self._http_client.request(
            "https://newsapi.org/v2/top-headlines",
            "GET",
            headers=headers,
            params=params,
        )
        if data:
            return data

    async def get_sources(
        self,
        *,
        country: tp.Literal[
            "ae",
            "ar",
            "at",
            "au",
            "be",
            "bg",
            "br",
            "ca",
            "ch",
            "cn",
            "co",
            "cu",
            "cz",
            "de",
            "eg",
            "fr",
            "gb",
            "gr",
            "hk",
            "hu",
            "id",
            "ie",
            "il",
            "in",
            "it",
            "jp",
            "kr",
            "lt",
            "lv",
            "ma",
            "mx",
            "my",
            "ng",
            "nl",
            "no",
            "nz",
            "ph",
            "pl",
            "pt",
            "ro",
            "rs",
            "ru",
            "sa",
            "se",
            "sg",
            "si",
            "sk",
            "th",
            "tr",
            "tw",
            "ua",
            "us",
            "ve",
            "za",
        ] = None,
        language: tp.Literal[
            "ar",
            "de",
            "en",
            "es",
            "fr",
            "he",
            "it",
            "nl",
            "no",
            "pt",
            "ru",
            "se",
            "ud",
            "zh",
        ] = None,
        category: tp.Literal[
            "business",
            "entertainment",
            "general",
            "health",
            "science",
            "sports",
            "technology",
        ] = None,
    ) -> tp.Any:
        """
        Get the sources or publishers of news available on NewsApi.

        Parameters
        ----------
        country : typinp.Literal["ae", "ar", "at", "au", "be", "bg", "br", "ca", "ch", "cn", "co", "cu", "cz", "de", "eg", "fr", "gb", "gr", "hk", "hu", "id", "ie", "il", "in", "it", "jp", "kr", "lt", "lv", "ma", "mx", "my", "ng", "nl", "no", "nz", "ph", "pl", "pt", "ro", "rs", "ru", "sa", "se", "sg", "si", "sk", "th", "tr", "tw", "ua", "us", "ve", "za"], optional
            The 2-letter ISO 3166-1 code of the country you want to get headlines for. Possible options: ae ar at au be bg br ca ch cn co cu cz de eg fr gb gr hk hu id ie il in it jp kr lt lv ma mx my ng nl no nz ph pl pt ro rs ru sa se sg si sk th tr tw ua us ve za,, by default None
        language : typinp.Literal["ar", "de", "en", "es", "fr", "he", "it", "nl", "no", "pt", "ru", "sv", "ud", "zh"], optional
            The 2-letter ISO-639-1 code of the language you want to get headlines for. Possible options: ar de en es fr he it nl no pt ru sv ud zh, by default None
        category : typing.Literal["business","entertainment","general","health","science","sports","technology"] , optional
            The category you want to get headlines for. Possible options: business entertainment general health science sports technology, by default None

        Returns
        -------
         typing.Any
            The response from NewsApi after getting sources.

        Raises
        ------
        HTTPException
            raises HTTPException if the status code is not `ok`.

        Examples
        -------
        >>> from newsdash import NewsDash
        >>> import asyncio
        >>> async def main():
        ... async with NewsDash('YOUR_API_KEY') as nd:
        ... print(await nd.get_sources(catgory='entertainment'))
        >>> asyncio.run(main())
        """
        params = {}
        if country is not None:
            if country not in [
                "ae",
                "ar",
                "at",
                "au",
                "be",
                "bg",
                "br",
                "ca",
                "ch",
                "cn",
                "co",
                "cu",
                "cz",
                "de",
                "eg",
                "fr",
                "gb",
                "gr",
                "hk",
                "hu",
                "id",
                "ie",
                "il",
                "in",
                "it",
                "jp",
                "kr",
                "lt",
                "lv",
                "ma",
                "mx",
                "my",
                "ng",
                "nl",
                "no",
                "nz",
                "ph",
                "pl",
                "pt",
                "ro",
                "rs",
                "ru",
                "sa",
                "se",
                "sg",
                "si",
                "sk",
                "th",
                "tr",
                "tw",
                "ua",
                "us",
                "ve",
                "za",
            ]:
                raise ValueError(
                    "country should be one out of the countries provided by news api"
                )
            params["country"] = country
        if category is not None:
            if category not in [
                "business",
                "entertainment",
                "general",
                "health",
                "science",
                "sports",
                "technology",
            ]:
                raise ValueError(
                    "category should be one out of the categories provided by newsapi"
                )
            params["category"] = category
        if language is not None:
            if language not in [
                "ar",
                "de",
                "en",
                "es",
                "fr",
                "he",
                "it",
                "nl",
                "no",
                "pt",
                "ru",
                "se",
                "ud",
                "zh",
            ]:
                raise ValueError(
                    "language should be one out of languages provided by newsapi"
                )
        headers = {"X-Api-Key": self.api_key}
        data = await self._http_client.request(
            "https://newsapi.org/v2/top-headlines",
            "GET",
            headers=headers,
            params=params,
        )
        if data:
            return data

from typing import Tuple


class GitUrlUtil:

    @staticmethod
    def get_organization_and_repository_name_from_url(url: str) -> Tuple[str, str]:
        """
        Returns the organization name and repository name from the given url.
        :param url: The url to parse.
        :return: A tuple containing the organization name and repository name.
        """
        split_url = url.split("/")
        return split_url[-4], split_url[-3]

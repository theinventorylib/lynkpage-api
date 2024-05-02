from django.db import models


class PortfolioManager(models.Manager):
    """_summary_

    Args:
        models (_type_): _description_
    """

    def get_queryset(self):
        """_summary_"""

        return super().get_queryset().filter(is_published=True)

    # create a new table in the persona portfolio database
    def add_extra_data(self):
        """_summary_"""

        return (
            super()
            .get_queryset()
            .filter(is_published=True)
            .extra(select={"length": "Length(description)"})
        )

# Standard library imports
from os import environ
from typing import Any, Optional

# Third party imports
import google.auth
import pandas as pd
import sqlalchemy
from google.cloud import bigquery as gcp_bigquery
from google.cloud import bigquery_storage
from tabulate import tabulate

# fmt: off
__all__ = [
    "create_bq_engine",
    "RunBigQuery",
]
# fmt: on


def create_bq_engine(
    project: str,
    dataset: Optional[str] = None,
    credentials: Optional[str] = None,
    **kwargs: Any,
) -> sqlalchemy.engine.Engine:
    """
    Create a SQLAlchemy Engine for Google BigQuery

    Args:
        project (): google project name
        dataset (): google dataset name
        credentials (): path of the google credentials. Defaults GCP_CREDENTIALS environment variable

    Returns:
        BigQuery engine
    """
    if credentials is None:
        credentials = environ.get("GCP_CREDENTIALS")
        assert (
            credentials is not None
        ), "credentials must be provided or GCP_CREDENTIALS set"

    uri = "bigquery://{}".format(project)
    if dataset is not None:
        uri += "/{}".format(dataset)

    engine = sqlalchemy.create_engine(uri, credentials_path=credentials, **kwargs)
    return engine


class RunBigQuery(object):
    """
    Wrapper to run a SQL from pandas so that the engine is encapsulated.

    This is the to alleviate constantly passing in the engine. For Example:

    .. highlight:: python
    .. code-block:: python

        run_sql = RunBigQuery(project, dataset)
        df1 = run_sql("select 1 as foo")
        df2 = run_sql("select 2 as foo")
    """

    def __init__(self, project: Optional[str] = None, dataset: Optional[str] = None):
        self.credentials, _ = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        self.project = project
        self.dataset = dataset
        self.bq_client = gcp_bigquery.Client(
            credentials=self.credentials, project=self.project, location=self.dataset
        )
        self.bq_storage_client = bigquery_storage.BigQueryReadClient(
            credentials=self.credentials
        )

    def __call__(
        self,
        query: str,
        verbose: bool = False,
        display: bool = False,
        display_progress_bar: bool = False,
    ) -> Optional[pd.DataFrame]:
        try:
            if verbose:
                print(query)
            if display_progress_bar:
                df = (
                    self.bq_client.query(query)
                    .result()
                    .to_dataframe(
                        bqstorage_client=self.bq_storage_client,
                        progress_bar_type="tqdm",
                    )
                )
            else:
                df = (
                    self.bq_client.query(query)
                    .result()
                    .to_dataframe(bqstorage_client=self.bq_storage_client)
                )
            if display:
                # Standard library imports
                import sys

                # Third party imports
                from IPython.display import display as ip_display

                if "ipykernel" in sys.modules:
                    # noinspection PyTypeChecker
                    ip_display(df.head(3))
                else:
                    if df.empty:
                        print("pandas.DataFrame has no rows")
                        return None
                    print(tabulate(df.head(5), headers="keys", tablefmt="psql"))
            return df
        except Exception as e:
            print(e)
            raise e

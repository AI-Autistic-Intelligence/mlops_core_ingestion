from abc import ABC, abstractmethod
import pandas as pd

class BaseDataClient(ABC):
    """
    Abstract Base Class for all data ingestion clients.
    """
    
    @abstractmethod
    def get_dataframe(self) -> pd.DataFrame:
        """
        Returns the fetched data as a pandas DataFrame.
        """
        pass

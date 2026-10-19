from pydantic_settings import BaseSettings, SettingsConfigDict

class Macro_DB_Settings(BaseSettings):
    '''
    Data validation of the environment variables using PyDantic.
    To be generalized for every type of databse (check @classmethod alternative)
    '''
    POSTGRES_SERVER: str
    POSTGRES_PORT : int 
    POSTGRES_USER : str
    POSTGRES_PASSWORD : str
    POSTGRES_FRED_DB : str
    FRED_API_KEY : str

    model_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore_empty=True,
        extra="ignore" #ignore everything in the .env file that is not defined above 
    )

    # property decorator allow us to access the method as if it were a class property 
    @property
    def POSTGRES_URL(self):
        # The url to a postgresql databa base is of type:
        # "postgresql+asyncpg://user:password@host:port/db"
        return F"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_FRED_DB}"

macro_sett = Macro_DB_Settings()

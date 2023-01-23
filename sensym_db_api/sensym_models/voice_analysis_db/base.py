from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData


metadata = MetaData(schema="voice_analysis")
Base = declarative_base(metadata=metadata)

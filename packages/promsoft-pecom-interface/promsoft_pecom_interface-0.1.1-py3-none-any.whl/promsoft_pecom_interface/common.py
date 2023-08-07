from pydantic import BaseModel


class IdentityCard(BaseModel):
    """
    Документ удостоверяющий личность  [Object]
    """

    type: int = 10  # 10 - ПАСПОРТ ГРАЖДАНИНА РФ,
    series: str = ""  # Серия [String]
    number: str = ""  # Номер [String]
    date: str = ""  # Дата [DateTime]

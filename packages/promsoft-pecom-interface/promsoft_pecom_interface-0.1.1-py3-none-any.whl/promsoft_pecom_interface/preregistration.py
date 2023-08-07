from pydantic import BaseModel, Field
from promsoft_pecom_interface.common import IdentityCard


class SenderPreregistration(BaseModel):
    """
    Данные об отправителе [Object]
    """

    city: str = ""  # Город [String]
    title: str = ""  # Наименование отправителя [String]
    inn: str = ""  # ИНН
    phone: str = ""  # Телефон [String]
    person: str = ""  # Контактное лицо [String]
    warehouseId: str = ""  # Идентификатор склада [String]
    addressStock: str = ""
    identityCard: IdentityCard = (
        IdentityCard()
    )  # Документ удостоверяющий личность  [Object]


class CommonPreregistration(BaseModel):
    """
    Общие данные о грузе [Object]
    """

    cargoPlaceList: list = Field(default_factory=list)  # Массив грузомест
    customerCorrelation: str = ""  # id заказа
    type: str = "3"  # Тип перевозки (1 - Авиаперевозка, 3 - Автоперевозка) [Number]
    declaredCost: int = 0  # Объявленная стоимость товара [Number]    // sum_zakaz
    accompanyingDocuments: bool = (
        False  # Есть комплект сопроводительных документов [Boolean]
    )
    positionsCount: int = 1  # Количество мест [Number]  //  Сейчас всегда 1
    description: str = "Оборудование"  # Описание груза [String]
    orderNumber: str = ""  # Номер заказа клиента [String], н/о  // idmonopolia
    typeClientBarcode: str = (
        "CODE128"  # Тип штрих-кодов, указанных для мест грузов заявки [String]
    )
    clientPriority: str = "1"  # приоритет [Number]


class ReceiverPreregistration(BaseModel):
    """
    Получатель [Object]
    """

    city: str = ""  # Город получателя [City] // city - из поля address в монополии, пропущенное через дадату и ПЭК
    title: str = ""  # Наименование получателя [String]
    phone: str = ""  # Телефон [String]
    person: str = ""  # Контактное лицо
    warehouseId: str = ""  # Склад
    inn: str = ""  # ИНН [String]
    addressStock: str = ""  # Адрес склада
    identityCard: IdentityCard = IdentityCard()  # Документ удостов. личность  [Object]


def _get_def_payer():
    return dict(type=2)


class ServicesPreregistration(BaseModel):
    """
    Услуги [Object]
    """

    class Transporting(BaseModel):
        """
        Перевозка [Object]
        # за услуги платит получатель, не отправитель
        """

        payer: dict = Field(
            default_factory=_get_def_payer
        )  # Плательщик [Object] (детальное описание см. ниже)

    class HardPacking(BaseModel):
        """
        Защитная транспортировочная упаковка [Object]
        # Заказана ли услуга [Boolean]
        """

        enabled: bool = False

    class Insurance(BaseModel):
        """
        Страхование [Object]
        """

        enabled: bool = False  # Заказана ли услуга [Boolean]
        cost: int = 0  # Оценочная стоимость, руб [Number]
        payer: dict = Field(default_factory=_get_def_payer)  # Плательщик [Object]

    class Delivery(BaseModel):
        """
        Доставка [Object]
        """

        enabled = True  # Заказана ли услуга [Boolean] // false, если в монополии есть слово "терминал"
        payer: dict = Field(default_factory=_get_def_payer)  # Плательщик [Object]

    class Sealing(BaseModel):
        """
        Пломбировка [Object]
        """

        enabled = False  # Заказана ли услуга [Boolean]

    class Strapping(BaseModel):
        """
        Упаковка стреппинг-лентой [Object]
        """

        enabled = False  # Заказана ли услуга [Boolean]

    class DocumentsReturning(BaseModel):
        """
        Возврат документов [Object]
        """

        enabled = False  # Заказана ли услуга [Boolean]

    transporting: Transporting = Transporting()
    hardPacking: HardPacking = HardPacking()
    insurance: Insurance = Insurance()
    delivery: Delivery = Delivery()
    sealing: Sealing = Sealing()
    strapping: Strapping = Strapping()
    documentsReturning: DocumentsReturning = DocumentsReturning()


class CargoPreregistration(BaseModel):
    """
    Данные об одном грузе [Object]
    """

    common: CommonPreregistration = CommonPreregistration()
    receiver: ReceiverPreregistration = ReceiverPreregistration()
    services: ServicesPreregistration = ServicesPreregistration()

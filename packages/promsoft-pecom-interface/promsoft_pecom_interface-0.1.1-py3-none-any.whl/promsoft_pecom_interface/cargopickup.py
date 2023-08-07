from pydantic import BaseModel, Field
from typing import Optional
from promsoft_pecom_interface.common import IdentityCard


class CommonCargopickup(BaseModel):
    """
    Общие данные [Object]
    """

    cargoPlaceList: list = Field(default_factory=list)  # Массив грузомест
    type: str = (
        "3"  # Тип заявки (1 - Авиаперевозка, 3 - Забор груза, 12 - Изи Уэй) [Number]
    )
    applicationDate: str = ""  # Дата исполнения заявки [Date] такого вида: "2021-03-30"
    description: str = "Оборудование"  # Описание груза [String]
    weight: float = 0.01  # Вес груза, кг [Number]
    volume: float = 0.001  # Объём груза, м3 [Number]
    positionsCount: int = 1  # Количество мест, шт [Number]
    width: float = 0.01  # Ширина, м [Number]
    length: float = 0.01  # Длина, м [Number]
    height: float = 0.01  # Высота, м [Number]
    isFragile: bool = False  # Хрупкий груз [Boolean]
    isGlass: bool = False  # Стекло [Boolean]
    isLiquid: bool = False  # Жидкость [Boolean]
    isOtherType: bool = False  # Груз другого типа [Boolean]
    isOtherTypeDescription: Optional[
        str
    ] = None  # Описание груза другого типа [String], поле обязательно, если isOtherType=true
    isOpenCar: bool = False  # Необходима открытая машина [Boolean]
    isSideLoad: bool = False  # Необходима боковая погрузка [Boolean]
    isDayByDay: bool = False  # Необходим забор день в день [Boolean]
    whoRegisterApplication: int = (
        1  # Представитель какой стороны оформляет заявки (1 - отправитель,
    )
    # 2 - получатель, 3 - третье лицо)
    responsiblePerson: str = ""  # ФИО ответственного за оформление заявки [String]
    typeClientBarcode: str = (
        "CODE128"  # Тип штрих-кодов, указанных для мест грузов заявки [String]
    )
    clientPositionsBarcode: list = Field(
        default_factory=list
    )  # Штрих-коды мест груза [Array] Каждый Штрих-код клиента [String]
    customerCorrelation: str = (
        ""  # Произвольное значение для синхронизации на стороне клиента [String],
    )


class ServicesCargopickup(BaseModel):
    """
    Услуги [Object]
    """

    isHP: bool = False  # Изготовление защитной транспортировочной упаковки [Boolean]
    isInsurance: bool = False  # Дополнительное страхование груза [Boolean]
    isInsurancePrice: int = 0  # Стоимость груза для страхования, руб / поле обязательно, если "isInsurance": True
    isSealing: bool = False  # Пломбировка груза (только до 3 кг) [Boolean]
    isStrapping: bool = False  # Упаковка груза стреппинг-лентой [Boolean]
    isDocumentsReturn: bool = False  # Возврат документов [Boolean]
    isLoading: bool = False  # Необходима погрузка силами «ПЭК» [Boolean]
    accompanyingDocuments: bool = (
        False  # Есть комплект сопроводительных документов [Boolean]
    )


class PersonInfoCargopickup(BaseModel):
    inn: str = ""  # ИНН [String],
    city: str = ""  # Город [String]
    title: str = ""  # Наименование отправителя [String]
    person: str = ""  # Контактное лицо [String]
    phone: str = ""  # Телефон [String]
    phoneAdditional: str = ""  # добавочный номер (максимум 10 символов) [String]
    identityCard: IdentityCard = (
        IdentityCard()
    )  # Документ удостоверяющий личность  [Object]


class SenderCargopickup(PersonInfoCargopickup):
    """
    Отправитель [Object]
    """

    addressOffice: str = ""  # Адрес офиса [String]
    addressOfficeComment: str = ""  # Комментарий к адресу офиса [String]
    addressStock: str = ""  # Адрес склада [String]
    addressStockComment: str = ""  # Комментарий к адресу склада [String]
    latitudeForCar: str = ""  # Координаты для подачи машины [String]
    longitudeForCar: str = ""  # Координаты для подачи машины [String]
    cargoDocumentNumber: str = ""  # Номер счета на оплату груза накладной
    isAuthorityNeeded: bool = False  # Для получения груза необходима доверенность «ПЭК» # (иначе, доверенность клиента)


class ReceiverCargopickup(PersonInfoCargopickup):
    """
    Получатель [Object]
    """

    isCityDeliveryNeeded: bool = True
    isCityDeliveryNeededAddress: str = ""
    isCityDeliveryNeededAddressComment: str = ""
    declaredCost: int = 0
    warehouseId: str = ""


class PaymentsCargopickup(BaseModel):
    """
    Оплата [Object]
    """

    class PickUp(BaseModel):
        """
        Оплата забора груза [Object]
        """

        type: int = (
            2  # Плательщик (1 - отправитель, 2 - получатель, 3 - третье лицо) [Number]
        )
        paymentCity: str = ""

    class Moving(BaseModel):
        """
        Оплата перевозки [Object]
        """

        type: int = (
            2  # Плательщик (1 - отправитель, 2 - получатель, 3 - третье лицо) [Number]
        )
        paymentCity: str = ""

    class Insurance(BaseModel):
        """
        Оплата страхования [Object],  # поле обязательно если services.isInsurance = True
        """

        type: int = (
            2  # Плательщик (1 - отправитель, 2 - получатель, 3 - третье лицо) [Number]
        )
        paymentCity: str = ""

    class Delivery(BaseModel):
        """
        Оплата доставки по городу получателя [Object], # поле обязательно если receiver.isCityDeliveryNeeded = True
        """

        type: int = (
            2  # Плательщик (1 - отправитель, 2 - получатель, 3 - третье лицо) [Number]
        )
        paymentCity: str = ""

    class HardPacking(BaseModel):
        """
        Оплата жесткой упаковки груза ( Обрешетка )
        """

        type: int = (
            2  # Плательщик (1 - отправитель, 2 - получатель, 3 - третье лицо) [Number]
        )
        paymentCity: str = ""

    pickUp: PickUp = PickUp()
    moving: Moving = Moving()
    insurance: Insurance = Insurance()
    delivery: Delivery = Delivery()
    hardpacking: HardPacking = HardPacking()


class BaseCargopickup(BaseModel):
    common: CommonCargopickup = CommonCargopickup()
    services: ServicesCargopickup = ServicesCargopickup()
    sender: SenderCargopickup = SenderCargopickup()
    receiver: ReceiverCargopickup = ReceiverCargopickup()
    payments: PaymentsCargopickup = PaymentsCargopickup()
    files: list = Field(default_factory=list)  # Файлы [Array]

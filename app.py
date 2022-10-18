from python_helper import DateTimeHelper, ObjectHelper, EnvironmentHelper, log
import datetime as dt

EnvironmentHelper.update('ENABLE_LOGS_WITH_COLORS', True)
EnvironmentHelper.update('LOGS_WITH_COLORS', True)
EnvironmentHelper.update('DEBUG', True)
log.loadSettings()

MONTHLY_OPERATIONAL_COST = 100.0


class Item:

    def __init__(self,
        itemType: str = None,
        aquisitionDate: dt.datetime = None,
        dayValidity: int = None,
        monthValidity: int = None,
        wear: float = None,
        maxWear: float = None,
        unityPrice: float = 0,
        quantity: int = 0
    ):
        self.itemType = itemType
        self.aquisitionDate = aquisitionDate if aquisitionDate else DateTimeHelper.dateNow()
        self.monthValidity = monthValidity
        self.dayValidity = dayValidity
        if wear > 100 or wear < 0:
            raise Exception(f"O desgaste do item {self.itemType} é inválido: {wear}")
        self.wear = wear
        if maxWear > 100 or maxWear < 0:
            raise Exception(f"O desgaste máximo do item {self.itemType} é inválido: {maxWear}")
        self.maxWear = maxWear
        self.unityPrice = unityPrice
        self.quantity = quantity
        # if self.wear > self.maxWear:
        #     raise Exception(f"O desgaste atual ({self.wear}) está maior que o máximo desgaste ({self.maxWear}) do item {self.itemType}")

    def __repr__(self):
        return f'{self.__class__.__name__}(itemType={self.itemType}, aquisitionDate={DateTimeHelper.dateOf(dateTime=self.aquisitionDate)}, monthValidity={self.monthValidity}, dayValidity={self.dayValidity}, wear={self.wear}, maxWear={self.maxWear}, unityPrice={self.unityPrice}, quantity={self.quantity})'

def getItemsToRenew(itemList):
    "deve retornar apenas os items que prescisam ser renovados"
    itemToRenewList = []
    for item in itemList:
        if isItemToRenew(item):
            itemToRenewList.append(item)
    return itemToRenewList

def isItemToRenew(item):
    "Item que devem ser renovados"
    return not isItemWithinValidity(item) or not isItemWearWithinTolerance(item) and 0 < item.quantity

def isItemWithinValidity(item):
    "true se está na validade e false caso não"
    # data de compra, data atual e data de validade em dias
    if ObjectHelper.isNone(item.dayValidity):
        return DateTimeHelper.plusMonths(item.aquisitionDate, months=item.monthValidity) > DateTimeHelper.now()
    else:
        return DateTimeHelper.plusDays(item.aquisitionDate, days=item.dayValidity) > DateTimeHelper.now()

def isItemWearWithinTolerance(item):
    "true se estiver dentro da tolerancia e false caso não"
    return item.wear < item.maxWear

def updateItemListWear(itemList, newWear):
    "atualiza os desgastes dos itens"
    for item in itemList:
        updateItemWear(item, newWear)
    return itemList

def updateItemWear(item, newWear):
    "Atualiza o desgaste do item e retorna o item"
    item.wear = newWear
    return item

def getItemListByType(itemList, desiredItemType):
    "filtra itens pelo tipo dado"
    if ObjectHelper.isNone(desiredItemType):
        return []
    desiredItemList = []
    for item in itemList:
        if ObjectHelper.isNotNone(item) and ObjectHelper.isNotNone(item.itemType) and desiredItemType == item.itemType:
            desiredItemList.append(item)
    return desiredItemList

def getItemType(item):
    "Retorna um item especifico"
    return item.itemType

def getRenovationCost(itemList):
    unityPrice = 0.0
    for item in getItemsToRenew(itemList):
        validateItemCost(item)
        unityPrice = unityPrice + getItemCost(item)
    return unityPrice + MONTHLY_OPERATIONAL_COST

def getItemCost(item):
    return item.quantity * item.unityPrice

def validateItemCost(item):
    if ObjectHelper.isNone(item.quantity):
        Exception('Quantidade do item não pode ser zero')
########################################################################################################################
########################################################################################################################
########################################################################################################################

wasteItemList = [
    Item(
        itemType='serra',
        aquisitionDate=DateTimeHelper.now(),
        monthValidity=6,
        wear=0.0,
        maxWear=80.0,
        unityPrice = 10.0,
        quantity = 1
    ),
    Item(
        itemType='cola',
        aquisitionDate=DateTimeHelper.minusMonths(DateTimeHelper.now(), months=6),
        monthValidity=2,
        wear=0.0,
        maxWear=80.0,
        unityPrice = 10.0,
        quantity = 1
    ),
    Item(
        itemType='prego',
        aquisitionDate=DateTimeHelper.now(),
        monthValidity=6,
        wear=0.0,
        maxWear=80.0,
        unityPrice = 10.0,
        quantity = 1
    ),
    Item(
        itemType='fita',
        aquisitionDate=DateTimeHelper.now(),
        dayValidity=60,
        wear=90.0,
        maxWear=80.0,
        unityPrice = 10.0,
        quantity = 1
    ),
    Item(
        itemType='fita',
        aquisitionDate=DateTimeHelper.now(),
        dayValidity=60,
        wear=0.0,
        maxWear=80.0,
        unityPrice = 10.0,
        quantity = 1
    ),
    Item(
        itemType='banana',
        aquisitionDate=DateTimeHelper.minusDays(DateTimeHelper.now(), days=30),
        dayValidity=20,
        wear=0.0,
        maxWear=80.0,
        unityPrice = 10.0,
        quantity = 1
    ),
    Item(
        itemType='banana',
        aquisitionDate=DateTimeHelper.minusDays(DateTimeHelper.now(), days=30),
        dayValidity=20,
        wear=0.0,
        maxWear=80.0,
        unityPrice = 10.0,
        quantity = 0
    )
]

# log.prettyPython(getItemsToRenew, 'items to renew', getItemsToRenew(wasteItemList), logLevel=log.DEBUG)
# log.prettyPython(getItemListByType, 'items por tipo', getItemListByType(wasteItemList, 'fita'), logLevel=log.DEBUG)
# log.prettyPython(getRenovationCost, 'get renovation unityPrice', getRenovationCost(wasteItemList), logLevel=log.DEBUG)

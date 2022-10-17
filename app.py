from python_helper import DateTimeHelper
import datetime as dt


# items:
class Item:


    def __init__(self, itemType: str = None, dataDeCompra: dt.datetime = None, validadeEmMeses: int = None,
                 desgaste: float = None, toleranciaDeDesgaste: float = None):
        self.itemType = itemType
        self.dataDeCompra = dataDeCompra if dataDeCompra else DateTimeHelper.dateNow()
        self.validadeEmMeses = validadeEmMeses
        if desgaste > 100 or desgaste < 0:
            raise Exception(f"O desgaste do item {itemType} é invalido: {desgaste}")
        self.desgaste = desgaste
        if toleranciaDeDesgaste > 100 or toleranciaDeDesgaste < 0:
            raise Exception(f"A tolerancia de desgaste do item {itemType} é invalida: {toleranciaDeDesgaste}")
        self.toleranciaDeDesgaste = toleranciaDeDesgaste


def __repr__(self):
    return f'{self.__class__.__name__}(itemType={self.itemType}, dataDeCompra={self.dataDeCompra}, ' \
           f'validadeEmMeses={self.validadeEmMeses}, desgaste={self.desgaste}, toleranciaDeDesgaste={self.toleranciaDeDesgaste})'


def getItemsToRenew(item):
    "deve retornar apenas os items que prescisam ser renovados"
    itemsToRenew = item

    for Item in item:
        if isItemToRenew(Item):
            itemsToRenew.append(item)
    return itemsToRenew


def isItemToRenew(Item):
    "Item que devem ser renovados"
    return not itemEstaDentroDaValidade(Item) or not desgasteDoItemDentroDaTolerancia(Item)


def itemEstaDentroDaValidade(Item):
    "true se está na validade e false caso não"
    # data de compra, data atual e data de validade em dias
    return DateTimeHelper.plusMonths(Item.dataDeCompra, months=Item.validadeEmMeses) > DateTimeHelper.now()


def desgasteDoItemDentroDaTolerancia(Item):
    "true se estiver dentro da tolerancia e false caso não"
    return Item.toleranciaDeDesgaste > Item.desgaste


def desgasteDoItem(Item):
    "Retorna o desgaste dos items"
    return Item.desgaste


def tipoDoItem(Item):
    "Retorna um item especifico"
    return Item.itemType



materialDeConsumo = [
    [Item(itemType='serra', dataDeCompra=DateTimeHelper.minusMonths(DateTimeHelper.now(), months=0), validadeEmMeses=0,
          desgaste=0.0, toleranciaDeDesgaste=0.0)],
    [Item(itemType='cola', dataDeCompra=DateTimeHelper.minusMonths(DateTimeHelper.now(), months=6), validadeEmMeses=6,
          desgaste=0.0, toleranciaDeDesgaste=80.0)],
    [Item(itemType='prego', dataDeCompra=DateTimeHelper.minusMonths(DateTimeHelper.now(), months=6), validadeEmMeses=6,
          desgaste=0.0, toleranciaDeDesgaste=80.0)],
    [Item(itemType='fita', dataDeCompra=DateTimeHelper.minusMonths(DateTimeHelper.now(), months=6), validadeEmMeses=6,
          desgaste=0.0, toleranciaDeDesgaste=80.0)]
]

# for p in materialDeConsumo:
print(tipoDoItem(Item))

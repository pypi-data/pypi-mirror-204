from ayaka import AyakaCat, get_adapter
from sqlmodel import select
from ..utils import subscribe

cat = AyakaCat("背包", db="ayaka_games")
adapter = get_adapter()


# @subscribe.cls_property_watch
class Money(cat.db.UserDBBase, table=True):
    money: int = 0


@cat.on_cmd(cmds=["bag", "背包"], always=True)
async def show_bag():
    '''展示背包；你还可以 bag @xx 查看其他人的背包'''
    uid = cat.user.id
    name = cat.user.name

    if cat.event.at:
        user = await cat.get_user(cat.event.at)
        if not user:
            return await cat.send("查无此人")
        uid = user.id
        name = user.name

    money = Money.get_or_create(cat.group.id, uid)
    await cat.send(f"[{name}]当前有 {money.money}金")


@cat.on_cmd(cmds="群首富", always=True)
async def show_bag_1():
    statement = select(Money).filter_by(
        group_id=cat.group.id).order_by(-Money.money).slice(0, 10)
    cursor = cat.db_session.exec(statement)
    data = cursor.all()

    items = []
    for d in data:
        user = await cat.get_user(d.user_id)
        if not user:
            continue
        name = user.name
        money = d.money
        items.append((f"[{name}]当前有 {money}金"))
    await cat.send_many(items)


@cat.on_cmd(cmds="群首负", always=True)
async def show_bag_2():
    statement = select(Money).filter_by(
        group_id=cat.group.id).order_by(Money.money).slice(0, 10)
    cursor = cat.db_session.exec(statement)
    data = cursor.all()

    items = []
    for d in data:
        user = await cat.get_user(d.user_id)
        if not user:
            continue
        name = user.name
        money = d.money
        items.append((f"[{name}]当前有 {money}金"))
    await cat.send_many(items)

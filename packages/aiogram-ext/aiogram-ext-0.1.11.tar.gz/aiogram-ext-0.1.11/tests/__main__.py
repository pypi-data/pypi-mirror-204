from botty import dp, Message, reply


@dp.command("test")
def _(msg: Message):
    return reply(msg, "test1")


@dp.command("test").state().extra(is_reply=True)
def _(msg: Message):
    return reply(msg, "test*")


dp.run()

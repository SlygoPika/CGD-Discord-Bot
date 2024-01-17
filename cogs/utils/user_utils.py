def get_user_roles(ctx):
    if ctx == None:
        return
    return ctx.author.roles


def get_user_roles_name(ctx):
    if ctx == None:
        return
    return [role.name for role in ctx.author.roles]

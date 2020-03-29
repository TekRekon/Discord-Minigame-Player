from discord.ext import commands


class RoleEnforcer(commands.Cog):
    guild = None
    djRole = None
    getsAdsRole = None
    getsNotifsRole = None
    botNotifsRole = None
    gameNotifsRole = None
    moderatorRole = None
    extraCategoryRole = None
    levelCategoryRole = None
    profileCategoryRole = None
    botReportsChannel = None
    modRequiredRoles = None
    memberRequiredRoles = None

    def __init__(self, bot):
        self.bot = bot
        guild = self.bot.get_guild(477829362771689484)
        RoleEnforcer.djRole = guild.get_role(490183595386863636)
        RoleEnforcer.getsAdsRole = guild.get_role(515548066871246888)
        RoleEnforcer.getsNotifsRole = guild.get_role(511316628013580309)
        RoleEnforcer.botNotifsRole = guild.get_role(556277198361722900)
        RoleEnforcer.gameNotifsRole = guild.get_role(513767484571254816)
        RoleEnforcer.moderatorRole = guild.get_role(488756415738150922)
        RoleEnforcer.extraCategoryRole = guild.get_role(513535344449159188)
        RoleEnforcer.levelCategoryRole = guild.get_role(513535057110106134)
        RoleEnforcer.profileCategoryRole = guild.get_role(513536050434539540)
        RoleEnforcer.botReportsChannel = self.bot.get_channel(488726201607782421)
        RoleEnforcer.modRequiredRoles = [RoleEnforcer.djRole, RoleEnforcer.getsAdsRole, RoleEnforcer.getsNotifsRole, RoleEnforcer.gameNotifsRole, RoleEnforcer.botNotifsRole, RoleEnforcer.profileCategoryRole,
                            RoleEnforcer.levelCategoryRole, RoleEnforcer.extraCategoryRole]
        RoleEnforcer.memberRequiredRoles = [RoleEnforcer.levelCategoryRole, RoleEnforcer.profileCategoryRole, RoleEnforcer.extraCategoryRole]


    @commands.Cog.listener()
    async def on_member_update(self, old_member, new_member):
        # Enforce Member-Required Roles
        if old_member.roles.sort() != new_member.roles.sort():
            for role in RoleEnforcer.memberRequiredRoles:
                if role not in new_member.roles:
                    await new_member.user.add_roles(role)
                    await RoleEnforcer.botReportsChannel.send(content='WARNING ' + new_member.mention + ": " + role.name
                                                                      + ' is a REQUIRED role')

        # Enforce Mod-Required Roles
        if RoleEnforcer.moderatorRole in new_member.roles:
            for role in RoleEnforcer.modRequiredRoles:
                if role not in new_member.roles:
                    await new_member.add_roles(role)
                    await RoleEnforcer.botReportsChannel.send(content='WARNING ' + new_member.mention
                                                                      + ': Moderators are required to have the '
                                                                      + role.name + ' role')


def setup(bot):
    bot.add_cog(RoleEnforcer(bot))

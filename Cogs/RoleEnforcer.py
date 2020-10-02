from discord.ext import commands


class RoleEnforcer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(477829362771689484)
        self.djRole = guild.get_role(490183595386863636)
        self.getsAdsRole = guild.get_role(515548066871246888)
        self.getsNotifsRole = guild.get_role(511316628013580309)
        self.botNotifsRole = guild.get_role(556277198361722900)
        self.gameNotifsRole = guild.get_role(513767484571254816)
        self.moderatorRole = guild.get_role(488756415738150922)
        self.extraCategoryRole = guild.get_role(513535344449159188)
        self.levelCategoryRole = guild.get_role(513535057110106134)
        self.profileCategoryRole = guild.get_role(513536050434539540)
        self.botReportsChannel = self.bot.get_channel(488726201607782421)
        self.modRequiredRoles = [self.djRole, self.getsAdsRole, self.getsNotifsRole, self.gameNotifsRole, self.botNotifsRole, self.profileCategoryRole, self.levelCategoryRole, self.extraCategoryRole]
        self.memberRequiredRoles = [self.levelCategoryRole, self.profileCategoryRole, self.extraCategoryRole]

    @commands.Cog.listener()
    async def on_member_update(self, old_member, new_member):
        # Enforce Member-Required Roles
        if old_member.roles.sort() != new_member.roles.sort():
            for role in self.memberRequiredRoles:
                if role not in new_member.roles:
                    await new_member.add_roles(role)
                    await self.botReportsChannel.send(content='WARNING ' + new_member.mention + ": " + role.name + ' is a REQUIRED role')

        # Enforce Mod-Required Roles
        if self.moderatorRole in new_member.roles:
            for role in self.modRequiredRoles:
                if role not in new_member.roles:
                    await new_member.add_roles(role)
                    # await new_member.remove_roles(*[self.moderatorRole, self.getsAdsRole, self.djRole])
                    await self.botReportsChannel.send(content='WARNING ' + new_member.mention + ': Moderators are required to have the ' + role.name + ' role')


def setup(bot):
    bot.add_cog(RoleEnforcer(bot))

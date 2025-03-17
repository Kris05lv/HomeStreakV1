class Household:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add_member(self, user):
        if user not in self.members:
            self.members.append(user)

    def get_leaderboard(self):
        return sorted(self.members, key=lambda user: getattr(user, 'points', 0), reverse=True)

    def to_dict(self):
        return {
            'name': self.name,
            'members': [member.to_dict() for member in self.members]
        }

from .abstract_models import AbstractUser

class User(AbstractUser):
	@property
	def permission_set(self):
		_permission_set = set()
		for i in self.roles.all():
			_permission_set |= set(i.permissions)
		return _permission_set
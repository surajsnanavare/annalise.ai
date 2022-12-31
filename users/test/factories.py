import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = get_user_model()
        django_get_or_create = ('username',)

    first_name = factory.Sequence(lambda n: "First %03d" % n)
    last_name = factory.Sequence(lambda n: "Last %03d" % n)
    username = factory.Sequence(lambda n: "user%03d" % n)
    is_active = True

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        # By using this method password can never be set to `None`!
        self.raw_password = 'default_password' if extracted is None else extracted
        self.set_password(self.raw_password)
        if create:
            self.save()
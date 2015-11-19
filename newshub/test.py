from django.test import TestCase
from .models import Profile, Author, Endorsement, Follow
from django.contrib.auth.models import User


class AnimalTestCase(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(
            username='test',
            email='abc@cam.ac.uk',
            first_name='Tamas',
            last_name='Sztanka')
        self.u2 = User.objects.create(
            username='test2',
            email='abcd@cam.ac.uk',
            first_name='User',
            last_name='ABC')
        Profile.objects.create(
            user=self.u1,
            picture='a')
        Profile.objects.create(
            user=self.u2,
            picture='b')
        self.a = Author.objects.create(
            user=self.u1)
        Endorsement.objects.create(
            author=self.a,
            endorsed_user=self.u2)
        Follow.objects.create(
            author=self.a,
            followed_by=self.u2)

    def test_animals_can_speak(self):
        print self.a.endorsed_by.count()
        print [x for x in self.u2.follow_set.all()[0].author.user]

from django.test import TestCase
from osmaxx.utilities.shortcuts import get_object_or_none, get_list_or_none
from osmaxx.utilities.tests.test_models.models import Article, Author


class GetObjectOrNoneTests(TestCase):
    available_apps = [
        'osmaxx.utilities.tests.test_models',
    ]

    def test_get_object_or_none(self):
        a1 = Author.objects.create(name="Brave Sir Robin")
        a2 = Author.objects.create(name="Patsy")

        # No Articles yet, so we should get None.
        self.assertEqual(None, get_object_or_none(Article, title="Foo"))

        article = Article.objects.create(title="Run away!")
        article.authors = [a1, a2]
        # get_object_or_none can be passed a Model to query.
        self.assertEqual(
            get_object_or_none(Article, title__contains="Run"),
            article
        )

        # We can also use the Article manager through an Author object.
        self.assertEqual(
            get_object_or_none(a1.article_set, title__contains="Run"),
            article
        )

        # No articles containing "Camelot".  This should return None.
        self.assertEqual(
            None,
            get_object_or_none(a1.article_set, title__contains="Camelot")
        )

        # Custom managers can be used too.
        self.assertEqual(
            get_object_or_none(Article.by_a_sir, title="Run away!"),
            article
        )

        # QuerySets can be used too.
        self.assertEqual(
            get_object_or_none(Article.objects.all(), title__contains="Run"),
            article
        )

        # Just as when using a get() lookup, you will get an error if more than
        # one object is returned.

        self.assertRaises(
            Author.MultipleObjectsReturned,
            get_object_or_none, Author.objects.all()
        )

        # Using an empty QuerySet returns None.
        self.assertEqual(
            None,
            get_object_or_none(Article.objects.none(), title__contains="Run")
        )

        # get_list_or_none can be used to get lists of objects
        self.assertEqual(
            get_list_or_none(a1.article_set, title__icontains="Run"),
            [article]
        )

        # An empty list is returned if the list is empty.
        self.assertEqual(
            [],
            get_list_or_none(a1.article_set, title__icontains="Shrubbery")
        )

        # Custom managers can be used too.
        self.assertEqual(
            get_list_or_none(Article.by_a_sir, title__icontains="Run"),
            [article]
        )

        # QuerySets can be used too.
        self.assertEqual(
            get_list_or_none(Article.objects.all(), title__icontains="Run"),
            [article]
        )

    def test_bad_class(self):
        # Given an argument klass that is not a Model, Manager, or Queryset
        # raises a helpful ValueError message
        self.assertRaisesMessage(
            ValueError,
            "Object is of type 'str', but must be a Django Model, Manager, "
            "or QuerySet",
            get_object_or_none, str("Article"), title__icontains="Run"
        )

        class CustomClass(object):
            pass

        self.assertRaisesMessage(
            ValueError,
            "Object is of type 'CustomClass', but must be a Django Model, "
            "Manager, or QuerySet",
            get_object_or_none, CustomClass, title__icontains="Run"
        )

        # Works for lists too
        self.assertRaisesMessage(
            ValueError,
            "Object is of type 'list', but must be a Django Model, Manager, "
            "or QuerySet",
            get_list_or_none, [Article], title__icontains="Run"
        )

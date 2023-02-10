from random import randint
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rango_project.settings")
import django

django.setup()

from rango.models import Category, Page

CATEGORIES = {
    "Python": {
        "views": 128,
        "likes": 64,
        "pages": [
            {
                "title": "Official Python Tutorial",
                "url": "http://docs.python.org/3/tutorial/",
            },
            {
                "title": "How to Think like a Computer Scientist",
                "url": "http://www.greenteapress.com/thinkpython/",
            },
            {
                "title": "Learn Python in 10 Minutes",
                "url": "http://www.korokithakis.net/tutorials/python/",
            },
        ],
    },
    "Django": {
        "views": 64,
        "likes": 32,
        "pages": [
            {
                "title": "Official Django Tutorial",
                "url": "https://docs.djangoproject.com/en/2.1/intro/tutorial01/",
            },
            {"title": "Django Rocks", "url": "http://www.djangorocks.com/"},
            {
                "title": "How to Tango with Django",
                "url": "http://www.tangowithdjango.com/",
            },
        ],
    },
    "Other Frameworks": {
        "views": 32,
        "likes": 16,
        "pages": [
            {"title": "Bottle", "url": "http://bottlepy.org/docs/dev/"},
            {"title": "Flask", "url": "http://flask.pocoo.org"},
        ],
    },
}


def add_category(name: str, views: int, likes: int) -> Category:
    c, _ = Category.objects.get_or_create(name=name, views=views, likes=likes)
    c.save()
    return c


def add_page(category: Category, title: str, url: str, views: int = 0) -> Page:
    p, _ = Page.objects.get_or_create(category=category, title=title)
    p.url, p.views = url, views + randint(1, 18)
    p.save()
    return p


def populate():
    for category_name, category_info in CATEGORIES.items():
        category = add_category(
            category_name, category_info["views"], category_info["likes"]
        )
        for page in category_info["pages"]:
            add_page(category, page["title"], page["url"])

    print("Categories added:")
    for category in Category.objects.all():
        for page in Page.objects.filter(category=category):
            print(f"- {category}: {page}")


def main():
    print("Populating...")
    populate()


if __name__ == "__main__":
    main()

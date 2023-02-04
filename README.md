# Hypercells

Infinite scroll for Django QuerySets.

*Note: Commercial use of this library via GitHub is prohibited but commercial 
licenses are available. Hypercells is distributed on GitHub under the 
[CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) license.*

# About

Hypercells allows you to easily add infinite-scrolling lists to your template-based
Django application's user interface. Each Hypercells section consumes a QuerySet
to automatically configure displayed results. As a user scrolls, the interface 
is updated behind the scenes by an automatically-configured REST API. Care 
has been given to optimize the way Hypercells uses a QuerySet to maximize 
performance for complex lookups.

Hypercells is highly configurable. By default hypercells provides a column
and row view, but it is configurable to meet virtually any requirement.

# Quick Look

Adding Hypercells to your app is as easy as dropping the hypercells app
into your project directory, then adding a few code snippets:

In your project `settings.py`:

    INSTALLED_APPS = [
        ...
        "hypercells",
        ...
    ]

In your project `urls.py`:

    import hypercells.lib

    urlpatterns = [
        ...
        path("hypercells/", include(hypercells.lib.urlpatterns)),
        ...
    ]

In your app `views.py`:

    import hypercells.lib

    def index(request):

        qs = Person.objects.all().order_by("first_name", "last_name")

        context = hypercells.lib.create(qs, displayed_fields=["first_name", "last_name"])

        return render(
            request, "templates/index.html", {"context": context, "context2": context2}
        )

And finally add the template tags to your template:

    {% load hypercells_tags %}

    <!doctype html>
    <html lang="en">
        <head>
            ...
        </head>
        
        <body>
            <div class="col-10 mx-auto overflow-scroll" style="height: 100vh">
                {% hypercells_table context %}
            </div>
            {% hypercells_js "hypercells" %}
        </body>
    </html>

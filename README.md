# Hypercells

Infinite scroll for Django QuerySets

*Note: Commercial use of this library via GitHub is prohibited but commercial 
licenses are available. Hypercells is distributed on GitHub under the 
[CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) license.*

## About

Hypercells allows you to easily add infinite-scrolling lists to your template-based
Django application's user interface. Each Hypercells section consumes a QuerySet
to automatically configure displayed results. As a user scrolls, the interface 
is updated behind the scenes by an automatically-configured REST API. Care 
has been given to optimize the way Hypercells uses a QuerySet to maximize 
performance for complex lookups.

Hypercells is highly configurable. By default hypercells provides a column
and row view, but it is configurable to meet virtually any requirement.

## Quick Look

Adding Hypercells to your app is as easy as dropping the hypercells app
(the hypercells directory in this repository) into your project directory 
and then adding a few code snippets:

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

        context = hypercells.lib.create(qs)

        return render(request, "templates/index.html", {"context": context})

And finally add the template tags to your template:

    {% load hypercells_tags %}

    <html>
        ...
        <body>
            <div style="height: 100vh; width: 100vw">
                {% hypercells_table context %}
            </div>
            {% hypercells_js "hypercells" %}
        </body>
    </html>

## Documentation

### `hypercells.lib.create(queryset, uid=None, context_class="", num_pages=10, page_length=100, 
loading_edge_pages=3, displayed_fields=[], hidden_fields=[])`

Creates or replaces a hypercells context in the database. A context stores 
the configuration for a hypercells instance, including the queryset that 
will drive it and other options.

- `queryset`: A QuerySet or conforming object that represents the data to be displayed.
- `uid`: Optional. A string that identifies this hypercells context. Default: a random uuid. Default behavior is unoptimal
because it creates a new context for each instance on every page load. If the uid is reused.
for each user's instance, hypercells will reuse a context instead of creating a new one each time.
- `context_class`: Optional. A string that is passed to the client javascript to distinguish different hypercells
instances for styling purposes.
- `num_pages`: Optional. An integer value of how many pages of data to load per request
- `page_length`: Optional. An integer value of how many rows of data to load per page.
- `loading_edge_pages`: Optional. An integer value of how many pages in advance of the currently loaded data's edge
for the client to begin requesting a new set of data.
- `displayed_fields`: Optional. A list of strings that name which fields of `queryset` to display.
- `hidden_fields`: Optional. A list of strings that name which fields of `queryset` to hide. This is mutually exclusive to `displayed_fields`,
with `displayed_fields` having priority.



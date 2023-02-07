# Hypercells

Infinite scroll for Django QuerySets

*Note: Commercial use of this library via GitHub is prohibited but commercial 
licenses are available. Hypercells is distributed on GitHub under the 
[CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) license.*

## About

Hypercells allows you to easily add infinite-scrolling lists to your template-based
Django application's user interface. Each Hypercells section or "context" consumes 
a QuerySet and automatically configures itself to display results. As a 
user scrolls, the interface is updated behind the scenes by an automatically-configured
REST API. Care has been given to optimize the way Hypercells uses a QuerySet to maximize 
performance for complex lookups. By default Hypercells provides a column and row 
view, but it is configurable to meet virtually any requirement.

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
            <div style="height: 100vh; overflow-y: scroll;">
                {% hypercells_table context %}
            </div>
            {% hypercells_js "hypercells" %}
        </body>
    </html>

## Documentation

### `hypercells.lib.create(queryset, uid=None, context_class="", num_pages=10, page_length=100, loading_edge_pages=3, displayed_fields=[], hidden_fields=[], css_classes={...})`

Creates or replaces a hypercells context in the database. A context stores 
the configuration for a hypercells instance, including the queryset that 
will drive it and other options. It is ok to create and display multiple contexts
per view and template.

- `queryset`: A QuerySet or conforming object that represents the data to be displayed.
- `uid`: Optional. A string that identifies this hypercells context. Default: a random uuid. Default behavior is unoptimal
because it creates a new context for each instance on every page load. If the uid is reused
for each user's instance, hypercells will reuse contexts instead of creating a new one each time.
- `context_class`: Optional. A string that is passed to the client javascript to distinguish different hypercells
instances for styling purposes.
- `num_pages`: Optional. An integer value of how many pages of data to load per request
- `page_length`: Optional. An integer value of how many rows of data to load per page.
- `loading_edge_pages`: Optional. An integer value of how many pages in advance of the currently loaded data's edge
the scroll must be before the client begins requesting a new set of data.
- `displayed_fields`: Optional. A list of strings that name which fields of `queryset` to display.
- `hidden_fields`: Optional. A list of strings that name which fields of `queryset` to hide. This is mutually exclusive to `displayed_fields`,
with `displayed_fields` having priority.
- `css_classes`: Optional. Default value: `{'table': 'table table-responsive table-hover', 'thead': '', 'thead_tr': '',
'thead_th': '', 'tbody': '', 'tbody_tr': '', 'tbody_td': '',}`. A dictionary of css classes to add to various
elements of the table.

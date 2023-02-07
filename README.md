# Hypercells

Infinite scroll for Django QuerySets

*Note: Commercial use of this library via GitHub is prohibited but commercial 
licenses are available. Hypercells is distributed on GitHub under the 
[CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/) license.*

## About

Hypercells allows you to easily add infinite-scrolling lists based on
QuerySet data to your template-based Django application's user interface. 
Each Hypercells section or "context" consumes a QuerySet and automatically 
configures itself to display results. As a user scrolls, the interface is 
updated behind the scenes by an automatically-configured REST API. Care 
has been given to optimize the way Hypercells uses a QuerySet to maximize 
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
            {% hypercells_js "hypercells/" %}
        </body>
    </html>

## Documentation

### `hypercells.lib.create(queryset, uid=None, display_thead=True, context_class="", num_pages=10, page_length=100, loading_edge_pages=3, displayed_fields=[], hidden_fields=[], css_classes={...}, enforce_security=False, request=None)`

Creates or replaces a hypercells context in the database. A context stores 
the configuration for a hypercells instance, including the queryset that 
will drive it and other options. It is ok to create and display multiple contexts
per view and template.

- `queryset`: A QuerySet or conforming object that represents the data to be displayed.
- `uid`: Optional. A string that identifies this hypercells context. If `None` is provided, a random
uid is generated. Default behavior is unoptimal because it creates a new context for each instance on every page load.
For this reason, it is recommended to use `create_uid_from_user` described below.
- `display_thead`: Optional. A boolean value that enables or disables the header row.
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
- `enforce_security`: Optional. If enabled, the API will only respond to requests from the user which created
a context. Note: Contexts owned by anonymous users will have API security disabled, 
since it is impossible to authenticate them.
- `request`: Optional. If enforce_security is enabled, this argument is required. It is used to get the
current user to store in the context.

### `hypercells.lib.create_uid_from_user(request, location_identifier)`

Creates a `uid` for use with `create(...)` that is based off the Django request's currently logged in user.
If no user is logged in, it returns `None`, which will generate a random uuid in `create`.
The `location_identifier` should be a unique string for every uniquely-configured hypercells 
instance on your site. Using this function to generate uids allows hypercells to reuse contexts and
prevent cluttering your database.

### `hypercells.lib.delete_old_contexts(days=0, hours=8, minutes=0)`

Deletes all contexts older than the provided arguments. This should be used in a regularly occurring task
so old contexts do not accumulate.

### `{% hypercells_table context %}`

This template tag renders a django template that contains the HTML necessary to render
a new hypercells table. Each `hypercells_table` tag must include a context created by
`hypercells.lib.create`. Do not share contexts for multiple `hypercells_tables` tags.

Additionally, the `hypercells_table` must be placed as a child of an HTML element
capable of scrolling and generating scroll events. For this reason, if you are
adding the table inside a div, adding `style="height: 100vh; overflow-y: scroll;"`
or similar is required.

### `{% hypercells_js "hypercells/" %}`

This template tag renders a django template that contains the javascript necessary to render
all hypercells tables on a page. Only use one instance of `hypercells_js` on a page.
The template tag takes one string, which is the urlpath root of the hypercells API
you configured in your urls.py.

`hypercells_js` is best included at the bottom of your `<body>` tag but can be placed
anywhere a `<script>` tag can be used.

## Extending Hypercells

The default hypercells interface is display-only and has no interactive features
other than scrolling. It is possible to add interactivity and other features
to hypercells by extending the built-in templates.

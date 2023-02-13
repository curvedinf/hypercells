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

## Running the Example Project

### Dependencies

* Python (tested with 3.10)
* Django (tested with 4.1)
* Django Debug Toolbar - install with `pip install django-debug-toolbar`

### Running

Open a terminal in the project root directory and run:

    python3 manage.py migrate
    python3 manage.py loaddata misc/us-10000.csv.json
    python3 manage.py runserver

## Project Notes

The example project in this repository is a standard django project with two django apps.
The project's name is `project_example`, and the two apps are `app_example` and
`hypercells`. The `hypercells` app is designed to be portable into your project
to provide the infinite scroll functionality. The `app_example` app is designed
to showcase how to use hypercells.

## Documentation

### `hypercells.lib.create(queryset, uid=None, display_thead=True, context_class="", num_pages=10, page_length=100, loading_edge_pages=3, displayed_fields=[...], hidden_fields=[...], transmitted_fields=[...], field_order=[...], css_classes={...}, enforce_security=False, request=None, templates={...})`

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
- `transmitted_fields`: Optional. A list of strings that name which fields of `queryset` should be sent to the client but not displayed. This
setting takes priority over `displayed_fields` and `hidden_fields`. It is useful for implementing detailed views accessible by clicking
on a row or field.
- `field_order`: Optional. A list of strings that provide the order to display the fields of `queryset`. Field names listed that are not 
otherwise visible will be ignored.
- `css_classes`: Optional. A dictionary of css classes to add to various elements of the table. 
Default value: `{'table': 'table table-responsive table-hover', 'thead': '', 'thead_tr': '',
'thead_th': '', 'tbody': '', 'tbody_tr': '', 'tbody_td': '',}`. 
- `enforce_security`: Optional. If enabled, the API will only respond to requests from the user which created
a context. Note: Contexts owned by anonymous users will have API security disabled, 
since it is impossible to authenticate them.
- `request`: Optional. If enforce_security is enabled, this argument is required. It is used to get the
current user for the context.
- `templates`: Optional. A dict of template overrides for the default hypercells templates. Available template keys are defined in
`hypercells.lib`: `HC_TEMPLATE_JS`, `HC_TEMPLATE_TABLE`, `HC_TEMPLATE_LOADER`, `HC_TEMPLATE_TD_JS`, `HC_TEMPLATE_TR_JS`. 
Example usage: `templates={HC_TEMPLATE_TR_JS: "custom_tr_js.html",}`.

### `hypercells.lib.create_uid_from_user(request, location_identifier)`

Creates a `uid` for use with `create(...)` that is based off the Django request's currently logged in user.
If no user is logged in, it returns `None`, which will generate a random uuid in `create`.
The `location_identifier` should be a unique string for every uniquely-configured hypercells 
instance on your site. Using this function to generate uids allows hypercells to reuse contexts and
prevent cluttering your database.

### `hypercells.lib.delete_old_contexts(days=0, hours=8, minutes=0)`

Deletes all contexts older than the provided arguments. This should be used in a regularly occurring task
so old contexts do not accumulate.

## Built-in Template Tags

Each of hypercells' built-in templates is rendered using a matching custom 
template tag.

### `{% hypercells_table context %}`

Renders the hypercells_table template that contains the HTML for a new hypercells table. 
Each `hypercells_table` tag must include a context created by
`hypercells.lib.create`. Do not share contexts for multiple `hypercells_tables` tags.

Additionally, the `hypercells_table` must be placed as a child of an HTML element
capable of scrolling and generating scroll events. For this reason, if you are
adding the table inside a div, adding `style="height: 100vh; overflow-y: scroll;"`
or similar is required.

### `{% hypercells_js "hypercells/" optional_context %}`

Renders the django template that contains the javascript necessary to render
all hypercells tables on a page. Only use one instance of `hypercells_js` on a page.

The template tag takes a required string, which is the urlpath root of the hypercells API
you configured in your urls.py.

If you intend to extend any javascript hypercells templates, you must include optional_context, 
which is a hypercells context object with the appropriate template overloads. Otherwise 
optional_context can be excluded. Note that because you have only one hypercells_js 
tag per page, your javascript template overloads can not be specific for each context, and
must be for the entire page. This may not be obvious because a context is passed
in to provide the templates. Putting the template overloads in the context was a design decision
to keep the template extension system unified and clean on the python side.

Note: `hypercells_js` is best included at the bottom of your `<body>` tag but can be placed
anywhere a `<script>` tag can be used.

## Extending Hypercells

It is possible to add interactivity and other features to hypercells by extending the 
built-in templates. To do this, create a new template in your app's template directory
and pass it into your hypercells context. For example: 
`create(..., templates={HC_TEMPLATE_TR_JS: "my_template.html"})`.

### `hypercells_tr_js.html`

Hypercells provides this template as a way to hook into the javascript
of the row creation process. Internally this tag is used as the body of the
`hc_tr_customization(tr_el, fields, tbody_el, context_class, row_num)` javascript
function defined in `hypercells_js.html`. It can be used to define any events 
or other per-row code and is called after a row is created, but before 
the row is added to the table (pre-render). Several other arguments are passed into the
scope that should allow you to do just about anything with the row.

### `hypercells_td_js.html`

Hypercells provides this template as a way to hook into the javascript
of the cell creation process. Internally this tag is used as the body of the
`hc_generate_td_innerHTML(td_el, field_name, fields, tbody_el, context_class, row_num)` 
javascript function defined in `hypercells_js.html`. It is used to create
the innerHTML of each TD tag in the hypercells instance.

### `hypercells_loader.html`

Hypercells uses this template internally to create the HTML for the animation 
used on loading pages prior to information being received. It can be extended
to replace the animation with a custom one.

### `hypercells_table.html`

Hypercells uses this tag to create the HTML for each hypercells table. It
can be extended to format the table in a custom way.

### `hypercells_js.html`

Hypercells uses this tag to create the javascript that is used for all
hypercells instances on a page. Ultimately, you can rewrite the javascript
completely to your needs by extending this.

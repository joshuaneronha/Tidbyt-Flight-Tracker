load("render.star", "render")
load("http.star", "http")
load("encoding/base64.star", "base64")
load("encoding/json.star", "json")

WN_ICON = base64.decode("""iVBORw0KGgoAAAANSUhEUgAAAA0AAAAMCAYAAAC5tzfZAAAAAXNSR0IArs4c6QAAAIRlWElmTU0AKgAAAAgABQESAAMAAAABAAEAAAEaAAUAAAABAAAASgEbAAUAAAABAAAAUgEoAAMAAAABAAIAAIdpAAQAAAABAAAAWgAAAAAAAABIAAAAAQAAAEgAAAABAAOgAQADAAAAAQABAACgAgAEAAAAAQAAAA2gAwAEAAAAAQAAAAwAAAAAZ5BcHQAAAAlwSFlzAAALEwAACxMBAJqcGAAAAVlpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDYuMC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KGV7hBwAAAk5JREFUKBVdkF9IU3EUx8/2c/M6Kl1uuQdJWhJCrMJhhGtxwyX9gVJsqf3BdHHJpIeK6iFCKQdBT4Wge2uZj2mlJv5jwUzBzUJtWbkmVNowuqHOXe+f3dN2zZe+D4fDOZ/vOYejgn8KDfnOayJfD64ur0grJtOb5XNVw4cWBu0JjnVwcY6aZyl/EV3dvsHDZ++zTrGmFrkCC/KFRcjSDoy0tLIY7UD8bUUMA+KXcpx+3dytmD4EAhWy6yL+AuCjBRZ+MTNHWACt9B0AZytd0lxfmxCbbOBxBNZwsgJnJkeryeFTda4/6cZig/gjoR5/p5XyzETQ69WCPlvm/YMk1hEm33JsBHY65SzdHBHiWVFCl1aWnA5l2EwWi7xrfz6Bl52wxrIgZRtU0patIBtXQe58ATFdobz5QA2ZX+JG1TptfOSkHIcbPYLKY6Ih8aoXiM0KQngGJB0FwrIacLcFsOU+hN1P4aeY+1Zde7as25wjTIGRSnM/joiN7yVYvPMA0uoZ4D9OQUKjAYjzIgWgiW03fDpeUvw8LfWNMvu2S5K8NN7CpmuetIYT/RMUaa44AXvM+SDevJWQkwahvgHWjhytA5UK1YzHo6FpOuAszau6bDcC5GYQKsqJrpogTOcViYb+QZJ+5SqsljguHKNtY0GGSa5OiqZ9ysa+AX+565oXYe8jhB33OIC72NbehxOh6TMpztfUpHCpXBHDeJQJvb1d+243emeddV50P+yI9HT1W1NAMHnROvlf9HiCSgMRNw0MjV1HZDMVQ3C9voH/Bdo4CwAvPmwHAAAAAElFTkSuQmCC""")

MAP = base64.decode('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')

def main():
    rep = http.get(COINDESK_PRICE_URL)
    if rep.status_code != 200:
        fail("CoinDesk request failed with status %d", rep.status_code)

    rate = rep.json()["bpi"]["USD"]["rate_float"]

    return render.Root(
        child = render.Row(
            children = [
                render.Box(
                  render.Column(
                    main_align = 'space_evenly',
                    cross_align = 'center',
                    children = [
                      render.Row(
                        children = [
                          render.Image(src=WN_ICON),
                          render.Text('1075')
                        ]
                      ),

                  render.Text('BWI'),
                  render.Text('12:45'),
                  ],),width=36, height=32),
                render.Box(
                  render.Image(src=MAP,width=28, height=32))
            ]
        )

    )

    return render.Root(
        child = render.Box(
            render.Row(
              children = [
                  render.Column(

                        children = [
                              render.Row(
                                  expanded = True,
                                  cross_align = "center",
                                  children = [
                                      render.Image(src=WN_ICON),
                                      render.Text('WN')
                                  ]
                              ),

                              render.Text('BWI'),
                              render.Text('12:45'),

                        ],
                      ),
                    render.Column(
                          children = [
                              render.Text('WN')
                          ]
                          )
                      ]
                  )
        )
    )

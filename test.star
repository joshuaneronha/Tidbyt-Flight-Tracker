load("render.star", "render")
load("http.star", "http")
load("encoding/base64.star", "base64")
load("encoding/json.star", "json")

JSON_URL = 'https://raw.githubusercontent.com/joshuaneronha/Tidbyt-Flight-Tracker/main/next_flight.json'

WN_ICON = base64.decode("""iVBORw0KGgoAAAANSUhEUgAAAA0AAAAMCAYAAAC5tzfZAAAAAXNSR0IArs4c6QAAAIRlWElmTU0AKgAAAAgABQESAAMAAAABAAEAAAEaAAUAAAABAAAASgEbAAUAAAABAAAAUgEoAAMAAAABAAIAAIdpAAQAAAABAAAAWgAAAAAAAABIAAAAAQAAAEgAAAABAAOgAQADAAAAAQABAACgAgAEAAAAAQAAAA2gAwAEAAAAAQAAAAwAAAAAZ5BcHQAAAAlwSFlzAAALEwAACxMBAJqcGAAAAVlpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IlhNUCBDb3JlIDYuMC4wIj4KICAgPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4KICAgICAgPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIKICAgICAgICAgICAgeG1sbnM6dGlmZj0iaHR0cDovL25zLmFkb2JlLmNvbS90aWZmLzEuMC8iPgogICAgICAgICA8dGlmZjpPcmllbnRhdGlvbj4xPC90aWZmOk9yaWVudGF0aW9uPgogICAgICA8L3JkZjpEZXNjcmlwdGlvbj4KICAgPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KGV7hBwAAAk5JREFUKBVdkF9IU3EUx8/2c/M6Kl1uuQdJWhJCrMJhhGtxwyX9gVJsqf3BdHHJpIeK6iFCKQdBT4Wge2uZj2mlJv5jwUzBzUJtWbkmVNowuqHOXe+f3dN2zZe+D4fDOZ/vOYejgn8KDfnOayJfD64ur0grJtOb5XNVw4cWBu0JjnVwcY6aZyl/EV3dvsHDZ++zTrGmFrkCC/KFRcjSDoy0tLIY7UD8bUUMA+KXcpx+3dytmD4EAhWy6yL+AuCjBRZ+MTNHWACt9B0AZytd0lxfmxCbbOBxBNZwsgJnJkeryeFTda4/6cZig/gjoR5/p5XyzETQ69WCPlvm/YMk1hEm33JsBHY65SzdHBHiWVFCl1aWnA5l2EwWi7xrfz6Bl52wxrIgZRtU0patIBtXQe58ATFdobz5QA2ZX+JG1TptfOSkHIcbPYLKY6Ih8aoXiM0KQngGJB0FwrIacLcFsOU+hN1P4aeY+1Zde7as25wjTIGRSnM/joiN7yVYvPMA0uoZ4D9OQUKjAYjzIgWgiW03fDpeUvw8LfWNMvu2S5K8NN7CpmuetIYT/RMUaa44AXvM+SDevJWQkwahvgHWjhytA5UK1YzHo6FpOuAszau6bDcC5GYQKsqJrpogTOcViYb+QZJ+5SqsljguHKNtY0GGSa5OiqZ9ysa+AX+565oXYe8jhB33OIC72NbehxOh6TMpztfUpHCpXBHDeJQJvb1d+243emeddV50P+yI9HT1W1NAMHnROvlf9HiCSgMRNw0MjV1HZDMVQ3C9voH/Bdo4CwAvPmwHAAAAAElFTkSuQmCC""")

def main():
    rep = http.get(JSON_URL)
    if rep.status_code != 200:
        fail("whoops", rep.status_code)

    flight_number = rep.json()['flight_number']
    arr_iata = rep.json()['arr_iata']
    short_time = rep.json()['short_time']
    map = base64.decode(rep.json()['map'])

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
                          render.Text(flight_number)
                        ]
                      ),

                  render.Text(arr_iata),
                  render.Text(short_time),
                  ],),width=36, height=32),
                render.Box(
                  render.Image(src=map,width=28, height=32))
            ]
        )

    )

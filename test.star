load("render.star", "render")
load("http.star", "http")
load("encoding/base64.star", "base64")
load("encoding/json.star", "json")

JSON_URL = 'https://raw.githubusercontent.com/joshuaneronha/Tidbyt-Flight-Tracker/main/next_flight.json'
LOGOS_URL = 'https://raw.githubusercontent.com/joshuaneronha/Tidbyt-Flight-Tracker/main/logos.json'

def main():
    rep = http.get(JSON_URL)
    logo = http.get(LOGOS_URL)
    if rep.status_code != 200:
        fail("whoops", rep.status_code)

    flight_number = rep.json()['flight_number']
    airline = rep.json()['airline_iata']
    arr_iata = rep.json()['arr_iata']
    short_time = rep.json()['short_time']
    map = base64.decode(rep.json()['map'])
    logo = base64.decode(logo.json()[airline])

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
                          render.Image(src=logo),
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

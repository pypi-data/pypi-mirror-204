# astronomica

<img src='astronomica.png'></img>
<h6>logo created with kittl.com</h6>

[![ForTheBadge built-with-love](https://forthebadge.com//images/badges/built-with-love.svg)](https://github.com/PyndyalaCoder/)
## Introduction and Purpose
The purpose of astronomica is to provide a set of tools for analyzing, generating, searching and visualizing astronomical data. This library aims to make it easy for astronomers, researchers, and students to explore and understand the universe using Python. By providing a comprehensive set of tools and a user-friendly interface, this library aims to empower astronomers and researchers to gain new insights into the universe and advance our understanding of the cosmos.

### Note of Usage:
<b>Astronomica is 100% free</b>!! It is also <b>driven by the <i>community</i></b>, so we welcome tips, bug fixes, and more methods added by users and the general python & astronomy community. You can also join our reddit community at https://www.reddit.com/r/pythonlibraries/ 


## Example usage:

For example, use the following piece of information:
- Heliocentric coordinates are coordinates that are measured relative to the center of the Sun, which is the primary source of gravitational attraction in the Solar System. Astronomers need heliocentric coordinates of Mars to study the planet's motion relative to the Sun, as well as to understand the dynamics of the Solar System.

The Helicocentric coordinates of any planet can be computed easily with astronomica - 

```python
from astronomica import *  # import all the tools offered by astronomica
xmars, ymars, zmars = planet_heliocentric_coordinates('mars')  # get the coordinates of mars right now
print(f"The Heliocentric Coordinates of Mars right now are: ({xmars}, {ymars}, {zmars}).")
```

Here is another usage example: 

- Astronomers need to know when astronomical night is so they can see the stars the best:

```python
# Import datetime module
import datetime
from astronomica import *

def get_astronomical_night():
    # Get the local sunset time as a datetime object
    sun = Sun(47.6, -122.2)
    sunset_time = sun.get_local_sunset_time(datetime.datetime.now())
    print(f"The local sunset time is {sunset_time}")

    # Calculate duration of the day in hours and minutes
    day_duration = datetime.timedelta(hours=24) - datetime.timedelta(hours=sunset_time.hour, minutes=sunset_time.minute)
    day_duration_hours, day_duration_minutes = divmod(day_duration.seconds // 60, 60)

    # Calculate the duration of astronomical twilight as a timedelta object
    twilight_duration = datetime.timedelta(minutes=day_duration.total_seconds() * 0.2666 / 60)

    # Calculate the duration of astronomical night as a timedelta object
    night_duration = day_duration - twilight_duration

    # Calculate the time of astronomical night as a datetime object
    night_time = sunset_time + night_duration

    # Format the time of astronomical night as a string in the format "HH:MM"
    night_time_str = night_time.strftime("%H:%M")

    print(f"The time of astronomical night is {night_time_str}")

get_astronomical_night()
```

## Utilities: 
astronomica provides a <b>wide</b> range of functions and tools that extend not only into astronomy, but physics and mathematics as well. Here are some of the things astronomica offers:
- ## Mathematics:
  - astronomica provides a wide range of trigonometry functions such as sine, cosine, tangent, arcsine, arccosine, arctangent, and more. It can also calculate a nth root of a number or raise a number to the nth power.
- ## Visualization:
  - astronomica provides visualization tools for a growing amount of astronomical data. As of Wednesday April 12th, Astronomica provides visualization for the mean anomaly of all nine planets, and more tools for plotting your own lists.
- ## Time:
  - astronomica provides two accurate functions for getting the current date and time as an str. They can be used in advanced calculations, as they are accurate to the second. Astronomica also has functions for getting the current julian date, local sidereal time, and conversions between gregorian and julian calendars.
- ## Astronomy:
  - astronomica provides a strong set of methods developed to make astronomy observations easier. It includes a host of general sun calculations, sunrise and set times, heliocentric coordinates (see the example), geocentric coordinates, geocentric latitude and longitude, star calculations (including the ability to map star names to their type), scraping astronomical databases for equatorial coordinates of stars, lunar phase calculation, lunar age and percent of age calculation, and finally, a method for getting the definition of a hard astronomy word.
- ## Physics:
  - astronomica currently has one function to get the gravitational force experienced by the earth from another object given its distance in astronomical units (the distance from the sun to earth is around 1 AU), and mass in kilograms. 




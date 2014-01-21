"""
Translation rules for Vancouver street addresses. Modified from Paul Norman's
rules for Surrey road names. Intended to be run against the property_addresses
dataset from the City of Vancouver's Open Data "Property information" bundle,
available at http://data.vancouver.ca/datacatalogue/propertyInformation.htm
at time of writing.

Copyright (c) 2011-2014 Paul Norman and Adam Williamson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

from string import capwords
import time


def translateName(rawname):
    suffixlookup = {}
    suffixlookup.update({'AV':'Avenue'})
    suffixlookup.update({'ST':'Street'})

    suffixlookup.update({'E':'East'})
    suffixlookup.update({'S':'South'})
    suffixlookup.update({'N':'North'})
    suffixlookup.update({'W':'West'})
    suffixlookup.update({'NE':'Northeast'})
    suffixlookup.update({'NW':'Northwest'})
    suffixlookup.update({'SE':'Southeast'})
    suffixlookup.update({'SW':'Southwest'})


    newName = ''
    for partName in rawname.split():
        newName = newName + ' ' + suffixlookup.get(partName,partName)
        # We can't use str.title(); it doesn't handle ordinals right
        newName = capwords(newName)

    return newName.strip()


def filterFeature(ogrfeature, fieldNames, reproject):
    if ogrfeature is None:
        return
    # Drop any entries without both a house number and street name (the dataset
    # contains a thousand or so entries missing both, for some reason)
    housenumber = ogrfeature.GetFieldAsString("CIVIC_NO")
    streetname = ogrfeature.GetFieldAsString("STREETNAME")
    if not (housenumber and streetname):
        return
    else:
        return ogrfeature


def filterTags(attrs):
    if not attrs:
        return

    tags = {}

    # Add the source. This includes the date/time you run the conversion
    # at. Obviously, it's only strictly correct if you downloaded the data
    # on the same day you run the conversion, but that should be close
    # enough.
    tags.update({'source':'City of Vancouver GIS data ' + time.strftime("%Y-%m-%d")})
    tags.update({'addr:city':'Vancouver'})
    tags.update({'addr:country':'CA'})
    #automagically convert names
    if attrs['STREETNAME']:
        tags.update({'addr:street':translateName(attrs['STREETNAME'].strip(' '))})

    if attrs['CIVIC_NO']:
        tags.update({'addr:housenumber':attrs['CIVIC_NO']})

    return tags


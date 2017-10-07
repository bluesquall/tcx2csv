#!/usr/bin/env python3

import os
from lxml import objectify
import csv
# import dateutil


def convert(tcxfile, csvfile=None):

    if csvfile is None:
        csvfile = '{}.csv'.format(os.path.splitext(tcxfile)[0])
    elif csvfile == '-':
        raise NotImplementedError

    activity = objectify.parse(tcxfile).getroot().Activities.Activity
    #tcxns = dict(TCX=activity.nsmap[None])
    sport = activity.attrib['Sport']

    with open(csvfile, 'wt') as outfile:
        outfile.write('# {}\n'.format(sport))
        out = csv.writer(outfile)
        out.writerow(['time','longitude','latitude','altitude','lap',
                        'distance','speed','cadence','power','heartrate'])
        lap_number = 0
        # for lap in activity.xpath('TCX:Lap', namespaces=tcxns):
        for lap in activity.iter('{*}Lap'):
            lap_number +=1
            # for point in lap.xpath('TCX:Trackpoint', namespaces=tcxns):
            for point in lap.Track.iter('{*}Trackpoint'):
                time = point.Time

                try:
                    longitude = point.Position.LongitudeDegrees
                except AttributeError:
                    longitude = ''

                try:
                    latitude = point.Position.LatitudeDegrees
                except AttributeError:
                    latitude = ''

                try:
                    altitude = point.AltitudeMeters
                except AttributeError:
                    altitude = ''

                try:
                    distance = point.DistanceMeters
                except AttributeError:
                    distance = ''

                speed = point.Extensions.find('.//{*}Speed')

                if sport == 'Running':
                    cadence = point.Extensions.find('.//{*}RunCadence')
                else: # sport == 'Biking'
                    try:
                        cadence = point.Cadence
                    except AttributeError:
                        cadence = ''

                power = point.find('.//{*}Watts')

                try:
                    heartrate = point.HeartRateBpm.Value
                except AttributeError:
                    heartrate = ''

                out.writerow([time, longitude, latitude, altitude, lap_number,
                        distance, speed, cadence, power, heartrate])


def main(tcxfile, csvfile = None):
    convert(tcxfile, csvfile)


if __name__ == "__main__":
    import argparse
    # instantiate parser
    parser = argparse.ArgumentParser(description='convert TCX to csv')
    # add positional arguments
    parser.add_argument('tcxfile', help='the TCX file to convert')
    # actually parse the arguments
    args = parser.parse_args()
    # call the main method to do something interesting
    main(**args.__dict__) #TODO more pythonic?

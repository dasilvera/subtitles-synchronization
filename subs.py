import re
import fileinput

def time_to_string(time):
    milesimas = time % 1000
    time //= 1000
    seconds = time % 60
    time //= 60
    minutes = time % 60
    time //= 60
    hours = time
    return '{}:{}:{},{}'.format('%02d' % (hours,),
                                '%02d' % (minutes,),
                                '%02d' % (seconds,),
                                '%03d' % (milesimas,))

def string_to_time(string):
    return int(string[9:12]) + 1000*(int(string[6:8]) + 60*(int(string[3:5]) + 60*int(string[0:2])))

if __name__ == '__main__':
    direction = input('Direccion de los subs: ')

    start = input('Comienzo de subs en el tiempo(hh:mm:ss:mmm): ')
    start = string_to_time(start)

    subs = open(direction, 'r')
    first_sub_time = re.findall('\d+:\d+:\d+,\d+', subs.read())[0]
    first_sub_time = string_to_time(first_sub_time)

    difference = start - first_sub_time

    for line in fileinput.input(direction, inplace = True):
        if re.match('\d+:\d+:\d+,\d+\s-->\s\d+:\d+:\d+,\d+\s*', line):
            times = re.findall('\d{2}:\d{2}:\d{2},\d{3}', line)
            new_time1 = time_to_string(string_to_time(times[0]) + difference)
            new_time2 = time_to_string(string_to_time(times[1]) + difference)
            print('{} --> {}'.format(new_time1, new_time2))
        else:
            print(line, end='')

    subs.close()

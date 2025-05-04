
import sys
argv = sys.argv

option = sys.argv[1]
if option=='-a':
    filename = sys.argv[2]
    with open(filename, 'r') as f:
        lines=[line.strip() for line in f.readlines()]
    if not lines:
        print("No distance information in this file")
    else:
        print("Origin-destination cities:")
        for line in lines:
            parts = line.split(',')
            print(f"{parts[0]}-{parts[1]}")
elif option=='-o':
    if len(sys.argv) != 4:
        print("Usage: python travelhelper.py -o argument_file")
        sys.exit()
    origin=sys.argv[2]
    filename = sys.argv[3]
    with open(filename, 'r') as f:
        lines=[line.strip() for line in f.readlines()]
    if not lines:
        print("No distance information in this file")
    else:
        data = []
        for line in lines:
            parts = line.split(',')
            parts[2] = int(parts[2])
            data.append(tuple(parts))
        destinations = [(dest, dist) for (orig, dest, dist) in data if orig == origin]
        if destinations:
            print(f"Destinations from {origin}:")
            for city, dist in destinations:
                print(f"City: {city}")
                print(f"Distance: {dist}")
        else:
            print(f"No known destinations from {origin}")
elif option=='-d':
    if len(argv) != 4 or not argv[2].isdigit():
        print("it misses the distance argument")
        sys.exit()
    distance = int(argv[2])
    filename = sys.argv[3]
    with open(filename, 'r') as f:
        lines=[line.strip() for line in f.readlines()]
    if not lines:
        print("No distance information in this file")
    else:
        data=[]
        for line in lines:
            parts = line.split(',')
            parts[2]=int(parts[2])
            data.append(tuple(parts))
        results = [(orig, dest, dist) for (orig, dest, dist) in data if dist <= distance]
        if results:
            print(f"Cities within {distance} Km distance:")
            for orig, dest, dist in results:
                print(f"{orig}-{dest}")
                print(f"Distance: {dist}")
        else:
            print(f"No cities within {distance} Km")
elif option == '-v':
    if len(argv) != 3:
        print("it misses the argument argument")
        sys.exit()
    print("Name: aaa")
    print("Surname: bbb")
    print("Student ID: 12345678")
    print("Date of completion: 2025-05-04")
else:
    print("this option doesn't exist")

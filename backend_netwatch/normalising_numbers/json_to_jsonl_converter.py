import sys, os, json, jsonlines, time


start_time = time.time()
filename = sys.argv[1]
pointless_values = sys.argv[2:] + [""]
print(pointless_values)

if os.path.exists(filename):
    new_json_list = []

    with open(filename, 'r') as json_file:
        for json_str in json_file:
            data = {}
            result = json.loads(json_str)
            for key, val in result.items():
                if not val in pointless_values:
                    data[key] = val
            new_json_list.append(data)

        with jsonlines.open('new' + filename, 'w') as writer:
            writer.write_all(new_json_list)

else:
    print('file does not exist')

end_time = time.time()
print(end_time - start_time)




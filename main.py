from tempbell import TempShot, get_tempshot_reader

reader = get_tempshot_reader(vendor = "lenovo", model = "thinkpad e495")

print(reader.read())

#! create sqlite db from csvs
import csv, sqlite3
def create_schedule(last_update_date: str):
    with open('last_update_date.txt','rw') as f:
        most_recent_update_date = f.readline()
        if last_update_date == most_recent_update_date:
            return
        else:
            f.write(last_update_date)

    con = sqlite3.connect("marta_schedule.sqlite")
    cur = con.cursor()
    #con.commit()
    with open('schema.sql','r') as schema_file:
        cur.executescript(schema_file.read())
    marta_csv_files = {
        'routes.txt':9
        ,'stops.txt':12
        ,'trips.txt':10
        ,'stop_times.txt':10
    }

    for file_name, num_fields in marta_csv_files.items():
        table_name,_,_ = file_name.partition('.')

        with open(file_name,'r') as f:
            num_cols = ', '.join('?' for x in range(num_fields))
            sql = f'INSERT INTO {table_name} VALUES({num_cols})'
            route_reader = csv.reader(f)
            headers = route_reader.__next__()
            cur.executemany(sql, route_reader)
            print(headers)
        con.commit()
    con.close()
if __name__ == '__main__':
    create_schedule(r'4/20/2024')
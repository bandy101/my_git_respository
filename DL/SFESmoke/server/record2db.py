import os
from os import path
import json

from DBModel import Record, Session


def main(dir_name: str):
    f = "record.json"
    for dn in os.listdir(dir_name):
        records = []
        for p, _, fl in os.walk(path.join(dir_name, dn)):
            if f in fl:
                with open(path.join(p, f), encoding="utf-8") as fp:
                    data = json.load(fp)
                record = Record()
                record.timestamp = data["timestamp"]
                record.st_id = data["st_id"]
                record.st_name = data["st_name"]
                record.Ringelmann = data["Ringelmann"]
                record.RingelmannLimit = data["RingelmannLimit"]
                record.plate = data["plate"]
                record.plate_color = data["plate_color"]
                record.plate_type = "其他"
                record.car_color = data["car_color"]
                record.car_type = data["car_type"]
                record.car_lane = data["car_lane"]
                record.save_dir = path.abspath(p)
                record.status = path.isfile(path.join(p, "status"))
                if path.isfile(path.join(p, "2")):
                    record.upload_status = "2"
                elif path.isfile(path.join(p, "1")):
                    record.upload_status = "1"
                else:
                    record.upload_status = "0"
                records.append(record)

        print(dn, "total", len(records))
        if records:
            try:
                sess = Session()
                sess.add_all(records)
                sess.commit()
            except:
                import traceback
                traceback.print_exc()
                sess.rollback()
                raise


if __name__ == "__main__":
    from fire import Fire
    Fire(main)

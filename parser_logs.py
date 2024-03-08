import argparse
import glob
import os
from collections import Counter
import json
import re


# Парсинг логов
def parse_logs(log_file):
    logs = []
    list_ip_addr = []
    list_method = []
    # парсим указанный файл с логами с помощью регулярных выражений
    with open(f"{log_file}", 'r') as file:
        for line in file.readlines():
            log_line = re.search(r"(?P<ip>^(\d{1,3}\.){3}\d{1,3}) .*? (?P<date>\[.+]) \"(?P<method>\w+) (?P<protocol>.+?)\" (?P<code>\d{3}) (?P<bytes>.*?) \"*(?P<url>.*?)\"* \"(?P<user_agent>.*)\" (?P<duration>\d+)", line)
            list_ip_addr.append(log_line.group("ip"))
            list_method.append(log_line.group("method"))
            log_item = {"ip": log_line.group("ip"),
                        "date": log_line.group("date"),
                        "method": log_line.group("method"),
                        "url": log_line.group("url"),
                        "duration": int(log_line.group("duration"))}
            logs.append(log_item)
    # составляем итоговый отчет
    result = {"top_ips": dict(Counter(list_ip_addr).most_common(3)),
              "top_longest": sorted(logs, key=lambda x: x["duration"], reverse=True)[0:3],
              "total_stat": dict(Counter(list_method)),
              "total_requests": len(logs)}
    # запись в файл
    log_name = os.path.split(log_file)[-1].split('.')[0]
    with open(f"report_{log_name}.json", "w") as f:
        report = json.dumps(result, indent=4)
        f.write(report)
    print(f"\n====== LOG FILE: {log_file} ======\n {report}")


def create_report():
    if os.path.isfile(args.log_path):
        parse_logs(args.log_path)
    elif os.path.isdir(args.log_path):
        log_files = glob.glob(f"{args.log_path}/*.log")
        for file in log_files:
            parse_logs(file)
    else:
        raise ValueError("Неправильный путь до логов")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-log_path', '--log_path', help='Path to log file or directory containing log files')
    args = parser.parse_args()
    create_report()

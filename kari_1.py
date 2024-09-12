import csv
import time

# CSVファイルの名前
filename = 'numbers.csv'

# CSVファイルを開く（存在しない場合は新規作成）
with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Number'])  # ヘッダー行を書き込む

    number = 0
    try:
        while True:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([timestamp, number])
            file.seek(0, 2)  # ファイルポインタをファイルの末尾に移動
            file.flush()  # バッファをクリアして即座に書き込む
            print(f'{timestamp}: {number}')
            number += 1
            time.sleep(1)  # 1秒待機
    except KeyboardInterrupt:
        print('終了しました。')

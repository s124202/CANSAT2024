import bluetooth
import time

def connect_bluetooth(target_address):
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1  # RFCOMMポートは通常1を使用

    try:
        sock.connect((target_address, port))
        print("接続成功")
        return sock
    except bluetooth.btcommon.BluetoothError as e:
        print(f"接続エラー: {e}")
        return None

def maintain_connection(target_address, max_retries=5):
    while True:
        sock = connect_bluetooth(target_address)
        if sock:
            try:
                # ここで接続中の処理を行う
                while True:
                    # 定期的に接続状態を確認
                    try:
                        sock.getpeername()
                    except:
                        print("接続が切断されました。再接続を試みます。")
                        break
                    time.sleep(5)  # 5秒ごとに確認
            except Exception as e:
                print(f"エラーが発生しました: {e}")
            finally:
                sock.close()
        
        # 再接続を試みる
        for i in range(max_retries):
            print(f"再接続を試みています... (試行 {i+1}/{max_retries})")
            time.sleep(5)  # 5秒待ってから再試行
            if connect_bluetooth(target_address):
                break
        else:
            print(f"{max_retries}回の再接続試行後も失敗しました。プログラムを終了します。")
            break

# 使用例
target_address = "B8:27:EB:A9:5B:64"  # 接続先のBluetoothアドレス
maintain_connection(target_address)
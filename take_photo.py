import picamera2 as picamera
import logging
import os
import cv2

logging.getLogger('picmaera2').setLevel(logging.WARNING)
os.environ["LIBCAMERA_LOG_LEVELS"] = "3"

def picture(path, width=320, height=240):
    filepath = None

    def filename(f, ext):
        """
        ファイル名に番号をつけるための関数
        引数f:つけたいファイル名
        引数ext:ファイルの拡張子
        戻り値f:ファイル名+0000.拡張子
        戻り値の番号は増えていく
        """
        i = 0
        while 1:
            num = ""
            if len(str(i)) <= 4:
                for j in range(4 - len(str(i))):
                    num = num + "0"
                num = num + str(i)
            else:
                num = str(i)
            if not (os.path.exists(f + num + "." + ext)):
                break
            i = i + 1
        f = f + num + "." + ext
        return f
      
    
    with picamera.Picamera2() as camera:
        filepath = filename(path, 'jpg') # カメラのファイル名作成
        camera_config = camera.create_still_configuration(main={"size": (width, height)}, lores={"size": (width, height)}, display="lores")
        camera.configure(camera_config)
        camera.start()
        camera.capture_file(filepath) # 撮影した画像を保
        #画像を読み込んで回転させる
        image = cv2.imread(filepath)
        image = cv2.resize(image, (width, height))
        image = cv2.rotate(image, cv2.ROTATE_180)
        cv2.imwrite(filepath, image)
    
    return filepath


if __name__ == '__main__':
    try:
        photoName = picture('../photo/test_imgs', 320, 240)
    except KeyboardInterrupt:
        print('stop')
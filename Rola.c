const int ledPin = 48;

void setup() {
  Serial.begin(9600);       // シリアル通信を9600bpsで開始
  pinMode(ledPin, OUTPUT);  // LEDピンを出力モードに設定
}

void loop() {
  delay(900); // 900ms待機

  digitalWrite(ledPin, HIGH);
  
  // 16進数「0xFF, 0xFF, 0x01, 0xFF」をシリアル通信で送信
  Serial.write(0xFF);   //ブロードキャスト上位
  Serial.write(0xFF);   //ブロードキャスト下位
  Serial.write(0x01);   //チャンネル番号
  Serial.write(0xFF);   //DATA

  Serial.print("\r\n"); // CRLF（改行）をシリアル通信で送信

  delay(100);

  digitalWrite(ledPin, LOW);
}
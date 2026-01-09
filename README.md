# Gen-AI-tools
Tiny gen ai tools

# Real-time Voice Converter (Vosk + Azure Neural TTS)

Ubuntu環境で動作するリアルタイム音声変換ツールです。  
マイクから入力した音声をオフラインで認識（Vosk）し、Azure Cognitive ServicesのNeural TTSで選択したアクセント・声質に変換して即座に再生します。  
音声認識から合成・再生までの遅延を最小限に抑えた低レイテンシ設計です。

## 1. 機能
- オフライン音声認識（Vosk small 英語モデル）
- Azureの高品質Neuralボイスによるリアルタイム音声合成
- アメリカ・イギリス・インド・オーストラリア英語の男女計8種類の声を選択可能
- マイク入力 → テキスト認識 → 指定声で再生 のフルリアルタイム処理

## 2. 必要環境
- Ubuntu 20.04 / 22.04 / 24.04（推奨）
- Python 3.8 以上
- マイクとスピーカー（ヘッドセット推奨）

## 3. インストール手順

### 3.1 システム依存パッケージのインストール
```bash
sudo apt update
sudo apt install portaudio19-dev python3-pyaudio
###　3.2 Pythonパッケージのインストール
Bashpip install pyaudio vosk azure-cognitiveservices-speech
###　3.3 Voskモデルのダウンロードと配置
Bashwget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
# 展開されたフォルダ「vosk-model-small-en-us-0.15」を
# voice_converter.py と同じディレクトリに配置してください
3.4 Azure Speechリソースの作成

Azure Portal で「Cognitive Services」→「Speech」リソースを作成
作成後、キー（Key 1 または Key 2） と リージョン（例: japaneast, eastus） をメモ

3.5 環境変数の設定
Bashexport AZURE_SPEECH_KEY="your-speech-key-here"
export AZURE_REGION="your-region-here"   # 例: japaneast
永続的に設定したい場合は ~/.bashrc または ~/.profile に上記を追記し、source ~/.bashrc で反映してください。
4. 実行方法
Bashpython3 voice_converter.py
起動後、表示される1〜8の番号から希望の声を入力してください。
マイクに向かって話すと、選択した声でほぼリアルタイムに再生されます。
終了は Ctrl + C。
5. トラブルシューティング

マイクが認識されないarecord -l でマイクデバイスを確認。alsamixer や pavucontrol で入力音量とキャプチャデバイスを調整してください。
音が出ない
スピーカーが正しく選択されているか確認（pavucontrol が便利）。ヘッドセット使用時は出力デバイスを切り替えてください。
Voskモデルが見つからないエラーvosk-model-small-en-us-0.15 フォルダがスクリプトと同じディレクトリにあるか確認してください。
Azure認証エラー
環境変数が正しく設定されているか echo $AZURE_SPEECH_KEY で確認してください。
遅延が大きい場合
ネットワーク環境やAzureリージョンとの距離が影響します。日本在住なら japaneast を選択すると改善します。

6. 注意事項

Azure Speechサービスは従量課金制です。テスト終了後はリソースを停止・削除して課金を抑えてください。
Voskのsmallモデルは軽量ですが認識精度はlargeモデルに劣ります。必要に応じてlargeモデルに置き換え可能です。
本ツールは英語音声認識・合成専用です（モデル依存）。

7. ライセンス
MIT License
Copyright (c) 2026
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
楽しんでご利用ください！

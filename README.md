# Gen-AI-tools
Tiny gen ai tools

# Real-time Voice Converter (Vosk + Azure Neural TTS)

Ubuntuで動作する、リアルタイム音声変換ツールです。  
マイクからの音声をオフライン（Vosk）で認識し、Azure Cognitive ServicesのNeural TTSで指定の声（アクセント）に変換して即座に再生します。

## 機能
- オフライン音声認識（Vosk smallモデル）
- Azureの高品質Neuralボイスによるリアルタイム音声合成
- アメリカ・イギリス・インド・オーストラリア英語の男女8種類の声を選択可能
- 低遅延処理

## 必要環境
- Ubuntu 20.04 / 22.04 / 24.04（推奨）
- Python 3.8 以上
- マイクとスピーカー（またはヘッドセット）

## インストール手順

### 1. システム依存パッケージのインストール
```bash
sudo apt update
sudo apt install portaudio19-dev python3-pyaudio
2. Pythonパッケージのインストール
Bashpip install pyaudio vosk azure-cognitiveservices-speech
3. Voskモデルのダウンロード
Bashwget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
# フォルダ名を以下にリネーム（コードと合わせるため）
mv vosk-model-small-en-us-0.15 vosk-model-small-en-us-0.15
4. Azure Speechのリソース作成

Azure Portalで「Cognitive Services」→「Speech」リソースを作成
キー（Key）とリージョン（例: japaneast）を取得

5. 環境変数の設定
Bashexport AZURE_SPEECH_KEY="your-speech-key-here"
export AZURE_REGION="your-region-here"  # 例: japaneast, eastus
※永続的に設定したい場合は ~/.bashrc や ~/.profile に追記してください。
実行方法
Bashpython3 voice_converter.py
起動後、1〜8から希望の声を番号で選択してください。
話しかけると、選択した声でリアルタイムに再生されます。
終了は Ctrl+C。
トラブルシューティング

マイクが認識されない
→ arecord -l でマイクを確認。alsamixer で入力音量を調整。
音が出ない
→ スピーカーが正しく選択されているか確認（PulseAudioの場合、pavucontrolで確認）。
Voskモデルエラー
→ モデルフォルダがカレントディレクトリにあり、名前が正しいか確認。
Azure認証エラー
→ 環境変数が正しく設定されているか、echo $AZURE_SPEECH_KEY で確認。

注意事項

Azure Speechは従量課金制です。不要時はリソースを停止してください。
Vosk smallモデルは軽量ですが、精度はlargeモデルより劣ります（必要に応じて置き換え可能）。

ライセンス
MIT License（自由に改変・再配布可能です）
楽しんでご利用ください！

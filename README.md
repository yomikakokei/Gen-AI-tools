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

# 受講映像から集中度を推定する実験

- 受講生の授業中の様子を撮影した動画（以後受講映像）から受講者の集中度を推定する実験に使用するコード
- ３つの興味を惹く動画と１つのリラックスする動画を再生し、その時の視聴者の様子をWebカメラで撮影します
- 動画は興味を惹く動画とリラックス動画の交互で繰り返し再生され、合間に集中度に関するアンケートを実施します

# 実験のやり方
## フォルダ構成  

project  
┣ logdir/  
┃ ┣ ここにログのCSVファイルが入ります  
┣ video_audio/  
┃ ┣ audio/  
┃ ┃ ┣ ここにwavファイルが入ります  
┃ ┣ video  
┃ ┃ ┣ ここにmp4ファイルが入ります  
┣ audio.py  
┣ log_for_CSV.py  
┣ video.py  
┣ video_audio.py  
┗ watch_zikken.py  

## 実行
    python watch_zikken.py
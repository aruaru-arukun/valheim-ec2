# valheim-ec2
ValheimのサーバーをEC2で構築するリポジトリです。

## はじめに
Valheimサーバーの構築をCloudFormationを使ってやってみた。
EC2はスポットインスタンス利用し、平日夜中はサーバー停止するような構成にして最小限のコストに抑えた。
似たような事やりたい人は参考にしてもらえたらよき！

（CloudFormationでスポットインスタンス取り扱ってるドキュメント少なくて泣いた。）

## 前提
- awsCLIが利用できること
- AWSの認証情報が設定されていること
- AWSアカウントを持っていること
- このリポジトリのセットアップが完了していること（https://github.com/aruaru-arukun/common）

## 初回の設定
#### Valheimのパスワードを設定
パラメーターストアにてVALHEIM_PASSWORDというキーでパスワードを設定してください。

#### Valheimサーバーの設定
cloudformation\Application.ymlにvalheim.envを編集している箇所があるので、お好みでカスタマイズしてください。

> valheim.envで検索すれば該当の箇所が見つかるはず！

#### CloudFormationのデプロイ
以下の順番でコマンドを実行してください
```
./sh/deploy-cfn.sh -e {環境名} -p {AWSプロファイル} -c sec
./sh/deploy-cfn.sh -e {環境名} -p {AWSプロファイル} -c app
```

#### EC2の初期設定
初めてCloudFormationスタックを起動したときのみ、EC2の初期設定が必要です。
以下の2つのコマンドを上から順にEC2のターミナルで実行してください。

```
./mount_ebs.sh
./init_valheim.sh
```

#### Valheimサーバー起動
ValheimサーバーはDockerコンテナで動作させています。
Dockerを起動してください。
```
cd $HOME/valheim-server && docker-compose up -d
```

#### インスタンスが置き換わった時の設定
EC2のターミナルで以下のコマンドを実行してください。

実行すると、Valheimのデータを保存しているストレージをアタッチし、EC2再起動時も自動でアタッチされるようになります。
```
/mount_ebs.sh
```

## スタック削除時
マネージドコンソールからCloudFormationスタックを削除してください。
スポットリクエストだけはスタックを削除しても残ってしまうので、手動でキャンセルしてください。

## おわりに
本当はCloudFormationをデプロイするだけで全ての設定が完了して、Valheimサーバーが立ち上がるようにしたかったが、スポットインスタンスに拒まれました。
なんかできる方法あったら教えてください。
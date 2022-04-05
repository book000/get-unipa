# Memo

- 複数ブラウザ(セッション)による同時ログイン可能
- ほぼすべての通信が POST で行われている
- トークン系は rx-token, rx-loginKey, rx-deviceKbn, rx-loginType, javax.faces.ViewState で構成されている
- 同一ページ内に同じIDの振られた要素が複数ある (掲示板 id="keiji")
- 要検証: 掲示板などにおいて、アイテムに付与されているIDは可変ではないか

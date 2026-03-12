# Password-Manager
基于Streamlit开发的Python密码管理器

功能
- 添加/查看/修改/删除密码
- 二级密码保护
- 搜索功能

文件说明
- `app.py` - 主程序
- `requirements.txt` - 依赖列表
- `account_webs.json` - 账户数据（自动生成）
- `personal_pwd.txt` - 二级密码（自动生成）


注意！！！！
- 二级密码使用 Base64 编码存储（仅供个人使用）
- 数据保存在本地 JSON 文件，删除文件即丢失数据

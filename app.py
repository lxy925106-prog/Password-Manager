import streamlit as st
import json
import os
import base64


if not os.path.exists("account_webs.json"):   #检测有没有存储密码文件
    with open("account_webs.json", "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=4)


pwd_file="personal_pwd.txt"
if not os.path.exists(pwd_file) :
    st.title("🔐 首次使用，请设置二级密码")
    with st.form("二级密码") :
        pwd1=st.text_input("输入二级密码",type="password")
        pwd2=st.text_input("再次确认二级密码",type="password")
        if st.form_submit_button("设置") :
            if pwd1 and pwd2 :
                encoded = base64.b64encode(pwd1.encode('utf-8')).decode('utf-8')
                with open(pwd_file, "w", encoding="utf-8") as f:
                    f.write(encoded)
                st.success("设置成功")
                st.rerun()
            else:
                st.error("密码不一致，重新输入")
    st.stop()


if "menu" not in st.session_state :  #初始化菜单
    st.session_state.menu="所有账户"
    st.session_state.websites=None
    st.session_state.account=None
    st.session_state.password=None

st.set_page_config(
    page_title="密码管理器",
    page_icon="🔐",
    layout="wide"
)

st.title("密码管理器")
st.caption("基于Streamlit开发的一种 Python密码管理器")
st.divider()

web_account={}

with st.sidebar :
    st.header("菜单")
    selected=st.radio(
        label="选择功能",
        options=["所有账户","添加密码","修改密码"],
        index=["所有账户","添加密码","修改密码"].index(st.session_state.menu)  #通过索引查找位置 .index()是列表的查找方法
    )

    if selected != st.session_state.menu : #只有当选择的侧边栏菜单和初始化菜单不相同的时候，调换
        st.session_state.menu=selected
        st.rerun()

if st.session_state.menu == "所有账户" :

    with open("account_webs.json","r",encoding="utf-8") as f :  #读取文件
        web_account=json.load(f)

    search=st.text_input("请输入网址")

    if search :  #搜索框
        clear_data={}
        for website,info in web_account.items() :  #将清洗过的文件重新添加到clear_data中
            if search.lower() in website.lower() :
                clear_data[website]=info
    else:
        clear_data=web_account

    with st.container(height=400) :     #滑动列表框
        for website,info in clear_data.items() :
            cols=st.columns([2,2,1,1,1])
            cols[0].write(website)
            cols[1].write(f" 👤 {info['account']}")
            if cols[2].button("删除",key=f"user_delete_{website}") :
                del web_account[website]
                with open("account_webs.json","w",encoding="utf-8") as file :
                    json.dump(web_account,file,ensure_ascii=False)
                    st.success("删除完成")
                    st.rerun()
            if cols[3].button("修改密码",key=f"user_fix_{website}") :
                st.session_state.websites=website
                st.session_state.account=info['account']
                st.session_state.menu="修改密码"
                st.rerun()
            if cols[4].button("显示密码",key=f"user_look_{website}") :
                st.session_state[f"show_pwd_{website}"] = True
                st.rerun()

            if st.session_state.get(f"show_pwd_{website}", False):
                with st.popover("二级密码验证"):
                    sec_pwd = st.text_input("请输入二级密码", type="password", key=f"sec_{website}")
                    if st.button("确认", key=f"verify_{website}"):
                        with open(pwd_file, "r", encoding="utf-8") as f:
                            stored = f.read().strip()
                        input_encoded = base64.b64encode(sec_pwd.encode('utf-8')).decode('utf-8')

                        if input_encoded == stored:
                            # 验证成功
                            decoded_password = base64.b64decode(info['password'].encode('utf-8')).decode('utf-8')
                            st.success(f"密码：{decoded_password}")
                            st.session_state[f"show_pwd_{website}"] = False
                        else:
                            st.error("二级密码错误")

            st.divider()

if st.session_state.menu == "添加密码" :
    with st.form(key="user_info_form",clear_on_submit=True) :   #clear_on_submit是完成后清空输入框
        website_input = st.text_input("输入网址")
        account_input = st.text_input("输入账号")
        password_input = st.text_input("输入密码",type="password")
        submit_button = st.form_submit_button(label="添加")

        if submit_button :
            if website_input and account_input and password_input :
                encoded_password = base64.b64encode(password_input.encode('utf-8')).decode('utf-8')  #加密密码
                with open("account_webs.json","r",encoding="utf-8") as f :
                    web_account=json.load(f)
                    web_account[website_input]={
                        "account":account_input,
                        "password":encoded_password
                    }
                    st.success("添加成功！")
                with open("account_webs.json","w",encoding="utf-8") as fs:
                        json.dump(web_account,fs,ensure_ascii=False)

if st.session_state.menu == "修改密码" :
    with st.form(key="user_info_fix_form",clear_on_submit=True) :
        st.markdown(f"要修改的网址为: :rainbow[**{st.session_state.websites}**]")  #   :{color}[文本]  给文本添加颜色
        st.markdown(f"要修改的账号为: :rainbow[**{st.session_state.account}**]")
        new_password=st.text_input("输入要修改的新密码",type="password")
        check_new_password=st.text_input("确认要修改的密码",type="password")
        if st.form_submit_button(label="确认修改") :
            if new_password == check_new_password :
                with open("account_webs.json","r",encoding="utf-8") as files :
                    web_account=json.load(files)
                    encoded_password = base64.b64encode(new_password.encode('utf-8')).decode('utf-8')  #加密密码
                    for web,info in web_account.items() :
                        if web == st.session_state.websites :
                            info["password"]=encoded_password   #存储加密密码
                            st.success("修改成功！")
                            st.session_state.websites=None
                            st.session_state.account=None
                with open("account_webs.json","w",encoding="utf-8") as ff:
                    json.dump(web_account,ff,ensure_ascii=False)
            else:
                st.error("密码不一致")
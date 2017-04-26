#coding:utf-8
import web
import time
import MySQLdb

conn = MySQLdb.connect(
        host='localhost',
        user='root',
        passwd='wangzq',
        db='TreeHole',
        charset="utf8",
        )

urls = ('/', 'login', 
        "/user/(.+)", "user",
        '/new', 'newuser',
        '/delete/(.+)', 'delete',
        '/check/(.+)', 'check',
        '/logout', 'logout'
        )

class login:
    def GET(self):
        try:
            username = web.cookies().username
            raise web.seeother("/user/%s"%username)
        except:
            web.header("Content-Type","text/html; charset=utf-8")
            return """
            <html>
            <body bgcolor="#C0C0C0">
            <form method="POST">
            <div style="width:300px;
                        height:200px;
                        margin:100px auto;
                        background:#525252;
                        box-shadow:#666 0px 0px 6px;
                        border-radius:4px">
            <center>
            <div style="width:300px;
                        height:30px;
                        margin=3px auto;
                        background:#606060;
                        line-height:30px;
                        border-radius:4px;
                        text-shadow:1px 1px 1px #949494">
            <font color="#DFDFDF">登录树洞</font>
            </div>
            <input style="width:200px;
                          height:30px;
                          margin:30px auto 3px;
                          border:none;
                          background:#DFDFDF;
                          border-radius:4px;
                          -webkit-appearance:none;"
                          type="text" name="username" placeholder="登录名">
            <br>
            <input style="width:200px;
                          height:30px;
                          margin:3px auto 10px;
                          border:none;
                          background:#DFDFDF;
                          border-radius:4px;
                          -webkit-appearance:none;"
                          type="password" name="password" placeholder="密码">
            <br>
            </center>
            <a href="/new" style="width:90px;
                                  height:30px;
                                  padding:5px 10px 5px 10px;
                                  margin:50px 50px 10px;
                                  font-size:14px;
                                  background:#9DC45F;
                                  text-decoration:none;
                                  border:none;
                                  color:#585858;
                                  border-radius:4px;
                                  box-shadow:1px 1px 1px #3D3D3D;
                                  -webkit-appearance:none;
                                  text-shadow:1px 1px 1px #949494;">注册</a>
            <input type="submit" style="width:90px;
                                        height:30px;
                                        font-size:14px;
                                        background:#FFCC02;
                                        border:none;
                                        color:#585858;
                                        border-radius:4px;
                                        box-shadow:1px 1px 1px #3D3D3D;
                                        text-shadow:1px 1px 1px #949494;
                                        -webkit-appearance:none;"
                                        value="登录">
            </div>
            </form>
            """

    def POST(self):
        x = web.input();
        cur = conn.cursor()
        aa = cur.execute("select password from pw where name='%s'" %x.username)
        info = cur.fetchmany(aa)
        cur.close()
        namecolor='#DFDFDF'
        nametext='登录名'
        pwtext='密码'
        pwcolor='#DFDFDF'

        if len(info) != 0:
            if x.password == info[0][0]:
                web.setcookie('username',x.username,3600)
                raise web.seeother("/user/%s" %x.username)
            else:
                pwcolor='#E27575'
                pwtext='密码错误'
        else:
            namecolor='#E27575'
            nametext='没有此用户'

        web.header("Content-Type","text/html; charset=utf-8")
        return """
        <html>
        <body bgcolor="#C0C0C0">
        <form method="POST">
        <div style="width:300px;
                    height:200px;
                    margin:100px auto 20px;
                    background:#525252;
                    box-shadow:#666 0px 0px 6px;
                    border-radius:4px">
        <center>
        <div style="width:300px;
                    height:30px;
                    margin=3px auto;
                    background:#606060;
                    line-height:30px;
                    border-radius:4px;
                    text-shadow:1px 1px 1px #949494">
        <font color="#DFDFDF">登录树洞</font>
        </div>
        <input style="width:200px;
                      height:30px;
                      margin:30px auto 3px;
                      border:none;
                      background:%s;
                      border-radius:4px;
                      -webkit-appearance:none;"
                      type="text" name="username" placeholder="%s">
        <br>
        <input style="width:200px;
                      height:30px;
                      margin:3px auto 10px;
                      border:none;
                      background:%s;
                      border-radius:4px;
                      -webkit-appearance:none;"
                      type="password" name="password" placeholder="%s">
        <br>
        </center>
        <a href="/new" style="width:90px;
                              height:30px;
                              padding:5px 10px 5px 10px;
                              margin:50px 50px 10px;
                              font-size:14px;
                              background:#9DC45F;
                              text-decoration:none;
                              border:none;
                              color:#585858;
                              border-radius:4px;
                              box-shadow:1px 1px 1px #3D3D3D;
                              -webkit-appearance:none;
                              text-shadow:1px 1px 1px #949494;">注册</a>
        <input type="submit" style="width:90px;
                                    height:30px;
                                    font-size:14px;
                                    background:#FFCC02;
                                    border:none;
                                    color:#585858;
                                    border-radius:4px;
                                    box-shadow:1px 1px 1px #3D3D3D;
                                    text-shadow:1px 1px 1px #949494;
                                    -webkit-appearance:none;"
                                    value="登录">
        </div>
        </div>
        </form>
        """ %(namecolor,nametext,pwcolor,pwtext)

class logout:
    def GET(self):
        web.setcookie('username', '', -1)
        raise web.seeother("/")

class delete:
    def GET(self, deletetime):
        cookei = web.cookies().get('username')
        cur = conn.cursor()
        cur.execute("delete from data where name='%s' and time='%s'" %(cookei,deletetime))
        conn.commit()
        cur.close()
        raise web.seeother("/user/%s" %cookei)

class check:
    def GET(self, checktime):
        if time.time()-float(checktime) < 7776000:
            web.header("Content-Type","text/html; charset=utf-8")
            return """<html><body><center><h4>还没到时候呢</h4></body></html>"""
        else:
            cur = conn.cursor()
            aa = cur.execute("select * from data where time='%s'" %checktime)
            info = cur.fetchmany(aa)
            cur.close()
            nowtime = time.strftime('%Y-%m-%d %X', time.localtime(float(checktime)))
            web.header("Content-Type","text/html; charset=utf-8")
            return """
            <html>
            <body>
            <div style="width:800px;margin:0 auto;background:#FCC">
            <dt>
            time: %s<br>
            user: %s
            </dt>
            </div>
            <div style="width:800px;margin:0 auto;background:#CCC">
                <dd>
                %s
                </dd><br>
            </div><br>
            </body>
            </html>
            """ %(nowtime, info[0][0], info[0][2])

class newuser:
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return """
        <html>
            <body bgcolor="#C0C0C0">
                <form method="POST">
                    <div style="width:300px;
                                height:230px;
                                margin:100px auto;
                                background:#525252;
                                box-shadow:#666 0px 0px 6px;
                                border-radius:4px">
                        <center>
                            <div style="width:300px;
                                        height:30px;
                                        margin=3px auto;
                                        background:#606060;
                                        line-height:30px;
                                        border-radius:4px;
                                        text-shadow:1px 1px 1px #949494">
                                <font color="#DFDFDF">注册树洞账户</font>
                            </div>
                            <div style="margin:30px auto 10px;">
                                <input style="width:200px;
                                              height:30px;
                                              border:none;
                                              background:#DFDFDF;
                                              border-radius:4px;
                                              -webkit-appearance:none;"
                                              type="text" name="newusername" placeholder="新登录名">
                            </div>
                            <div style="margin:3px auto 10px;">
                                <input style="width:200px;
                                              height:30px;
                                              border:none;
                                              background:#DFDFDF;
                                              border-radius:4px;
                                              -webkit-appearance:none;"
                                              type="password" name="newpassword" placeholder="密码">
                            </div>
                            <div style="margin:3px auto 10px;">
                                <input style="width:200px;
                                              height:30px;
                                              border:none;
                                              background:#DFDFDF;
                                              border-radius:4px;
                                              -webkit-appearance:none;"
                                              type="password" name="confirmpassword" placeholder="确认密码">
                            </div>
                            <div style="margin:3px auto 10px">
                                <input type="submit" style="width:90px;
                                                            height:30px;
                                                            font-size:14px;
                                                            background:#9DC45F;
                                                            border:none;
                                                            color:#585858;
                                                            border-radius:4px;
                                                            box-shadow:1px 1px 1px #3D3D3D;
                                                            text-shadow:1px 1px 1px #949494;
                                                            -webkit-appearance:none;"
                                                            value="注册">
                            </div>
                        </center>
                    </div>
                </form>
            </body>
        </html>
        """

    def POST(self):
        x = web.input()
        cur = conn.cursor()
        aa = cur.execute("select name from pw where name='%s'" %(x.newusername))
        info = cur.fetchmany(aa)
        cur.close()
        namecolor='#DFDFDF'
        pwcolor='#DFDFDF'
        nametext='登录名'
        pwtext='确认密码'
        if len(info) != 0 or x.confirmpassword != x.newpassword or x.newusername == "":
            if len(info) != 0:
                namecolor='#E27575'
                nametext='登陆名已存在'
            else:
                if x.newusername == "":
                    namecolor='#E27575'
                    nametext='用户名不能为空'
                else:
                    pwtext='密码不同'
                    pwcolor='#E27575'

            web.header("Content-Type","text/html; charset=utf-8")
            return """
            <html>
                <body bgcolor="#C0C0C0">
                    <form method="POST">
                        <div style="width:300px;
                                    height:230px;
                                    margin:100px auto;
                                    background:#525252;
                                    box-shadow:#666 0px 0px 6px;
                                    border-radius:4px">
                            <center>
                                <div style="width:300px;
                                            height:30px;
                                            margin=3px auto;
                                            background:#606060;
                                            line-height:30px;
                                            border-radius:4px;
                                            text-shadow:1px 1px 1px #949494">
                                    <font color="#DFDFDF">注册树洞账户</font>
                                </div>
                                <div style="margin:30px auto 10px;">
                                    <input style="width:200px;
                                                  height:30px;
                                                  border:none;
                                                  background:%s;
                                                  border-radius:4px;
                                                  -webkit-appearance:none;"
                                                  type="text" name="newusername" placeholder="%s">
                                </div>
                                <div style="margin:3px auto 10px;">
                                    <input style="width:200px;
                                                  height:30px;
                                                  border:none;
                                                  background:#DFDFDF;
                                                  border-radius:4px;
                                                  -webkit-appearance:none;"
                                                  type="password" name="newpassword" placeholder="密码">
                                </div>
                                <div style="margin:3px auto 10px;">
                                    <input style="width:200px;
                                                  height:30px;
                                                  border:none;
                                                  background:%s;
                                                  border-radius:4px;
                                                  -webkit-appearance:none;"
                                                  type="password" name="confirmpassword" placeholder="%s">
                                </div>
                                <div style="margin:3px auto 10px">
                                    <input type="submit" style="width:90px;
                                                                height:30px;
                                                                font-size:14px;
                                                                background:#9DC45F;
                                                                border:none;
                                                                color:#585858;
                                                                border-radius:4px;
                                                                box-shadow:1px 1px 1px #3D3D3D;
                                                                text-shadow:1px 1px 1px #949494;
                                                                -webkit-appearance:none;"
                                                                value="注册">
                                </div>
                            </center>
                        </div>
                    </form>
                </body>
            </html>
            """ %(namecolor,nametext,pwcolor,pwtext)
        else:
            cur = conn.cursor()
            cur.execute("insert into pw values('%s','%s')" %(x.newusername,x.newpassword))
            conn.commit()
            cur.close()
            raise web.seeother("/")

class user:
    def GET(self, username):
        cookei = web.cookies().get('username')
        if cookei == username:
            cur = conn.cursor()
            aa = cur.execute("select * from data")
            info = cur.fetchmany(aa)
            cur.close()
            addtext=""
            for temp in info:
                temptime = temp[1]
                nowtime = time.strftime('%Y-%m-%d %X', time.localtime(float(temptime)))
                nowtext=''
                color = '#CCF'
                option = 'delete'
                if temp[0] != username:
                    nowtext = '??????'
                    color = '#FCC'
                    option = 'check'
                else:
                    nowtext = temp[2]
                addtext = addtext + """
                    <div style="width:800px;margin:0 auto;background:%s">
                    <dt>
                    time: %s<br>
                    user: %s<br>
                    <a href="/%s/%s">%s</a>
                    </dt>
                    </div>
                    <div style="width:800px;margin:0 auto;background:#CCC">
                        <dd>
                        %s
                        </dd><br>
                    </div><br>
                    """ %(color, nowtime, temp[0], option, temptime, option, nowtext)
            web.header("Content-Type","text/html; charset=utf-8")
            return """
            <html>
            <body>
            当前用户:%s<br>
            <a href="/logout">退出登录</a>
            <br>
            <form method="POST">
            <center>
            <h3>
            写下你要说的话吧～
            </h3>
            <textarea rows="15" cols="70" name="Test"></textarea>
            <br>
            <input type="submit" value="提交咯">
            </form>
            </center>
            <dl>
            %s
            </dl>
            </body>
            </html>
            """ %(username.encode('utf8'),addtext.encode('utf8'))
        else:
            raise web.seeother("/")

    def POST(self, username):
        x = web.input()
        temptext = x.Test
        nowtime = time.time()
        cur = conn.cursor()
        cur.execute("insert into data values('%s','%s','%s')" %(username,nowtime,temptext))
        conn.commit()
        cur.close()
        web.setcookie('username',username,3600)
        raise web.seeother("/user/%s" %username)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()

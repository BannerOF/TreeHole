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
	def GET(self, filename):
		BUF_SIZE = 262144
		filedir = 'C:\Users\wangz\Desktop'
		fout = open(filedir +'\\'+ filename,'rb')
		while True:
			c = fout.read(BUF_SIZE)
			if c:
				yield c
			else:
				break
		fout.close()

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
				tempsavetime = temp[3]
				tempfilename = temp[4]
				option = ""
				if tempfilename !="":
					option = """<a href="/check/%s">attachment</a><br>"""%(tempfilename)
				nowtime = time.strftime('%Y-%m-%d %X', time.localtime(float(temptime)))
				nowtext=''
				if temp[0] != username:
					if time.time()-float(temptime) < float(tempsavetime):
						nowtext = '??????'
						color='#FCC'
						remaintime=float(tempsavetime)-time.time()+float(temptime)
						option = "" 
					else:
						nowtext = temp[2]
						color = '#CFC'
						remaintime='0';
					addtext = addtext + """
						<div style="width:800px;margin:0 auto;background:%s">
						<dt>
						time: %s<br>
						user: %s<br>
						remain: %sS<br>
						%s
						</dt>
						</div>
						<div style="width:800px;margin:0 auto;background:#CCC">
							<dd>
							%s
							</dd><br>
						</div><br>
						""" %(color, nowtime, temp[0], remaintime, option, nowtext)
				else:
					nowtext = temp[2]
					addtext = addtext + """
						<div style="width:800px;margin:0 auto;background:#CCF">
						<dt>
						time: %s<br>
						user: %s<br>
						<a href="/delete/%s">delete</a><br>
						%s
						</dt>
						</div>
						<div style="width:800px;margin:0 auto;background:#CCC">
							<dd>
							%s
							</dd><br>
						</div><br>
						""" %(nowtime, temp[0], temptime, option, nowtext)
			web.header("Content-Type","text/html; charset=utf-8")
			return """
			<html>
			<body bgcolor="#C0C0C0">
			<div style="width:100px;
						height:100px;
						background:#525252;
						box-shadow:#666 0px 0px 6px;
						border-radius:4px">

				<center>

				<div style="width:100px;
							height:30px;
							background:#606060;
							line-height:30px;
							border-radius:4px;
							text-shadow:1px 1px 1px #949494">

					<font color="#DFDFDF">当前用户</font>

				</div>

				<font color="#DFDFDF">%s</font>
				<br>
				<br>
				<a href="/logout" style="width:90px;
									  height:30px;
									  padding:5px 10px 5px 10px;
									  font-size:14px;
									  background:#E27575;
									  text-decoration:none;
									  border:none;
									  color:#585858;
									  border-radius:4px;
									  box-shadow:1px 1px 1px #3D3D3D;
									  -webkit-appearance:none;
									  text-shadow:1px 1px 1px #949494;">退出登陆</a>

			</div>
			<br>
			<form method="POST" enctype="multipart/form-data" action="">
			<center>
			<h2>
			留言
			</h2>
			<textarea style="border:none;
			                 background:#DFDFDF;
							 border-radius:4px;
							 " rows="15" cols="70" name="Test"></textarea>
			<br>
			附件
			<input type="file" name="myfile" />
			<br>
			<br>
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
										value="提交">
			<input type="radio" name="savetime" value="none" checked>即时
			<input type="radio" name="savetime" value="day">一天
			<input type="radio" name="savetime" value="week">一周
			</center>
			</form>
			<dl>
			%s
			</dl>
			</body>
			</html>
			""" %(username.encode('utf8'),addtext.encode('utf8'))
		else:
			raise web.seeother("/")

	def POST(self, username):
		x = web.input(myfile={})
		nowtime = time.time()
		temptext = x.Test
		cur = conn.cursor()
		tempsavetime = "0";
		if x.savetime == "none":
			tempsavetime = "0"
		else:
			if x.savetime == "day":
				tempsavetime = "86400"
			else:
				tempsavetime = "604800"
		filedir = 'C:\Users\wangz\Desktop'
		if 'myfile' in x:
			filepath=x.myfile.filename.replace('\\','/')
			filename=filepath.split('/')[-1]
			if filename != "":
				fout = open(filedir +'\\'+ filename,'wb')
				fout.write(x.myfile.file.read())
				fout.close()
		cur.execute("insert into data values('%s','%s','%s','%s','%s')" %(username,nowtime,temptext,tempsavetime,filename))
		conn.commit()
		cur.close()
		web.setcookie('username',username,3600)
		raise web.seeother("/user/%s" %username)

if __name__ == "__main__":
	app = web.application(urls, globals())
	app.run()


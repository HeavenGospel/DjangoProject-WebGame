from django.http import HttpResponse

def index(request):
    line1 = '<h1 style="text-align:center">我的世界大乱斗</h1>'
    line4 = '<a href="/play/">进入游戏界面</a>'
    line3 = '<hr>'
    line2 = '<img src="https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fi0.hdslb.com%2Fbfs%2Farticle%2F43c94fd466c22f63121235be4bda2c1b34c363a9.jpg&refer=http%3A%2F%2Fi0.hdslb.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1660553379&t=6ac970bd9aa8b16ece06a8e7a1cae0fc" width=1500>'
    return HttpResponse(line1 + line4 + line3 + line2)

def play(request):
    line1 = '<h1 style="text-align:center">游戏界面</h1>'
    line3 = '<a href="/">返回主页面</a>'
    line4 = '<hr>'
    line2 = '<img src="https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fi-1.33app.net%2F2020%2F4%2F10%2F94cff7b8-d8df-43f9-ba2e-5b5dcc19c3d1.jpg&refer=http%3A%2F%2Fi-1.33app.net&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1660554667&t=e2971ae58240d0d23028d7354578ddfb" width=1500>'
    return HttpResponse(line1 + line3 + line4 + line2)

let AC_GAME_OBJECTS = [];

class AcGameObject {
    constructor() {
        AC_GAME_OBJECTS.push(this);

        this.has_called_start = false;  //是否执行过start函数
        this.timedelta = 0;  //当前帧距离上一帧的时间间隔
        this.uuid = this.create_uuid();
    }

    create_uuid() {  // 为游戏里的元素随机一个唯一id
        let res = "";
        for (let i = 0; i < 8; i ++ ) {
            let x = parseInt(Math.floor(Math.random() * 10));  // random返回[0, 1)之间的小数
            res += x;
        }
        return res;
    }

    start() { //只会在第一帧执行一次
    }

    update() { //每一帧均会执行一次
    }

    on_destroy() { //在被销毁前执行一次
    }

    destroy() { //删掉该物体
        this.on_destroy();

        for (let i = 0; i < AC_GAME_OBJECTS.length; i ++ )
        {
            if (AC_GAME_OBJECTS[i] === this)
            {
                AC_GAME_OBJECTS.splice(i, 1);
                break;
            }
        }
    }
}

let last_timestamp;
let AC_GAME_ANIMATION = function(timestamp) {
    for (let i = 0; i < AC_GAME_OBJECTS.length; i ++ )
    {
        let obj = AC_GAME_OBJECTS[i];
        if (!obj.has_called_start)
        {
            obj.start();
            obj.has_called_start = true;
        }
        else
        {
            obj.timedelta = timestamp - last_timestamp;
            obj.update();
        }
    }
    last_timestamp = timestamp;
    requestAnimationFrame(AC_GAME_ANIMATION);
}

requestAnimationFrame(AC_GAME_ANIMATION);

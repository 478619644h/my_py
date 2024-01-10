
from PIL import Image

# 加载图片
flag = Image.open('guoqi.jpeg')
avatar = Image.open('avatar.jpg')

# 将过期尺寸调整为头像大小
flag.resize(avatar.size)

# 遍历国旗头像的每个像素点，修改透明度
for i in range(flag.size[0]):
    for j in range(flag.size[1]):
        r, g, b = flag.getpixel((i, j))
        # 透明度值
        alpha = max(0, 255 - i // 5 - j // 7)
        # 重新填充像素
        flag.putpixel((i, j), (r, g, b, alpha))

# 将新国旗头像粘贴到头像上面
avatar.paste(flag, (0, 0), flag)
# 保存为新图
avatar.save('flag_avatar.png')
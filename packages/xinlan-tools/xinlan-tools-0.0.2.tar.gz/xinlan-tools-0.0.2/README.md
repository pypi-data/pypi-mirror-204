# xinlan-tools
python开发的小工具集。

## 文件加密
命令格式：
```shell
tools encrypt <file_or_dir> [--number n]
```
参数：
- `file_or_dir`
必带参数，需要加密的文件或所在路径
- `--number`
可选参数，加密中使用的字节数，默认为10

文件加密和解密命令一致，运行第一次是加密，运行第二次是解密

## 图片格式转换
支持 png和jpg之间相互转换
命令格式：
```shell
tools convert source target
```
参数：
- `source`
必带参数，需要转换的图片文件名
- `target`
必带参数，需转换成的图片文件名
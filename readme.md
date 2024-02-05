# 说明文档<br/>Readme{.dragonmark}

<hr class="hr-double-arrow"/>

本项目是由`VSCode`插件`EncounterPlus`启发而来的小工具，主要功能是将markdown文件转译为带CSS格式的网页。本文档的完整格式请查看[readme.html](readme.html)。

> 其实这东西好像也没什么价值？毕竟markdown是速记工具不是画图工具。
>
> ——我自己{.aligned_right}

## 使用方式

1. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

2. 基本使用
   ```bash
   # 显示帮助
   python main.py -h
   # 将markdown文档转译成同名html文件
   python main.py --filename readme.md --title 说明文档
   # 支持通过--cssfile参数指定使用的css文件，目前限一个，默认为style.css
   # 支持使用--encoding参数指定输入文件的编码格式，默认为utf-8
   # 因使用环境，目前仅支持输出gbk编码
   ```

## 支持的特性

本工具支持大部分markdown特性，具体未完全测试。

本工具转译markdown文档时，部分标签后附的`{.classname}`用于指定特定标签所属的类。目前支持情况如下：

支持在段后（或者标题后）通过添加`{.classname}`的方式来指定该`<p>`标签所属的类，比如本段使用了`{.aligned_right}`，该类在`style.css`中指定。{.aligned_right}

支持在引文中单独留一行用于指定类，如

```markdown
> 引文
> 
> {.classname}
```

支持在表格中或行末指定类，支持指定表格的title，如

```markdown
`%示例表格%`

|head|head|
|:---|:--:|
|1234|2345|{.aligned_right}
|1|44{.aligned_left}|
```

`%示例表格%`

|head|head|
|:---|:--:|
|1234|2345|{.aligned_right}
|1|44{.aligned_left}|

支持在链接中指定类，如`[sometext{.classname}](someurl)`。效果：

- [有格式的不全书链接{.spell}](https://github.com/DND5eChm)
- [无格式的不全书链接](https://github.com/DND5eChm)
系统软件综合训练课程 银行家算法模拟实现 

使用纯python实现

## ver1.1更新  
新增组件布局自动适应 支持获取桌面分辨率并自适应窗口大小

修改随机数生成逻辑，现在可用资源不会为负数了

输入框新增下拉框内容，现在只用鼠标交互就可以使用软件

## ver1.2更新
新增边界条件处理，用户输入非法数据（如负数）时提示。

新增超时处理，用户输入较大较难计算数据时，计算时间超过10秒就会自动中断程序。

## 打包
利用pyinstaller打包

```csharp
pyinstaller --onefile --windowed --icon="software_bankers/bk.ico" --name="银行家算法模拟ver1.2 -by L1jiu" software_bankers/main.py
```

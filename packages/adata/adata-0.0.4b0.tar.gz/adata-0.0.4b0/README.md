# A Data

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/adata?color=d)](https://pypi.org/project/adata/)[![Licence](https://img.shields.io/hexpm/l/apa?color=d)](https://gitee.com/inchaos/adata/blob/master/LICENSE)


## 0、介绍
免费开源A股数据库，专注量化，向阳而生。

开放、纯净、持续

## 一、快速开始

### （1）安装sdk

#### 1. 简单安装

~~~python
# 首次安装
pip install adata

# 升级版本
pip install -U adata
~~~

#### 2. 指定镜像源安装

~~~
# 首次安装
pip install adata -i http://mirrors.aliyun.com/pypi/simple/

# 升级版本
pip install -U adata -i http://mirrors.aliyun.com/pypi/simple/
~~~

**注：国内镜像可能存在同步延迟，可使用官方镜像源**

#### 3.推荐镜像源列表

国内镜像源

阿里云【推荐】：http://mirrors.aliyun.com/pypi/simple/ 

清华大学：https://pypi.tuna.tsinghua.edu.cn/simple 

豆瓣：http://pypi.douban.com/simple/

官方镜像源

官方：https://pypi.org/simple

### （2）使用示例

#### 1. 获取股票代码信息



#### 2. 获取股票的行情

#### 3. 其它数据使用

请参考下面数据列表和相关字典文档进行使用

## 二、数据列表

整理了最新版本的数据列表和相关使用Api，详细内容和相关使用参数，请参考数据字典文档。

### （1）股票-Stock

#### 	1. 基本信息

| 数据     | API                               | 说明                                | 备注                 |
| -------- | --------------------------------- | ----------------------------------- | -------------------- |
| A股代码  | stock.info.all_code()             | 所有A股代码信息                     |                      |
| 概念代码 | stock.info.all_concept_code_ths() | 所有A股概念代码信息（同花顺）pc+app | 来源：同花顺公开数据 |
|          | stock.info.concept_code_ths_pc()  | A股概念代码信息（同花顺）pc         | 来源：同花顺数据中心 |
|          | stock.info.concept_code_ths_app() | A股概念代码信息（同花顺）app        | 来源：问财           |

#### 	2. 行情信息

| 数据     | API                                  | 说明                                  | 备注                   |
| -------- | ------------------------------------ | ------------------------------------- | ---------------------- |
| 分红信息 | stock.maket.get_dividend()           | 获取单只股票的分红信息                |                        |
| 股票行情 | stock.market.get_market()            | 获取单只股票的行情信息-日、周、月 k线 |                        |
| 概念行情 | stock.maket.get_market_concept_ths() | 获取单个概念的行情信息-日、周、月 k线 | 只有同花顺相关概念行情 |
|          |                                      |                                       |                        |

### （2）ETF

| 项目          | 进度         | 说明                           |
| ------------- | ------------ | ------------------------------ |
| 场内可交易etf | 排期中...... | 若您有相关资源可以一起参与贡献 |

### （3）债券-Bond

| 项目       | 进度         | 说明                           |
| ---------- | ------------ | ------------------------------ |
| 可转换债券 | 排期中...... | 若您有相关资源可以一起参与贡献 |



## 三、数据源

| 数据源     | 板块                                                         | 描述             |
| ---------- | ------------------------------------------------------------ | ---------------- |
| 同花顺     | [数据中心](http://data.10jqka.com.cn/)，[行情中心](http://q.10jqka.com.cn/)，[问财](http://www.iwencai.com/unifiedwap/home/index) | 让投资变的更简单 |
| 百度股市通 | [股市通](https://gushitong.baidu.com/)                       | 科技让投资更简单 |
| 东方财富   | [数据中心](https://data.eastmoney.com/center/)，[行情中心](http://quote.eastmoney.com/center/) | 财经门户         |



## 四、 其它参考

主要记录查阅过的项目和相关平台，并对此项目产生了深远印象，特此鸣谢。

| [akshare](https://gitee.com/mirrors/akshare) | [聚宽量化](https://www.joinquant.com/) | [baostock](http://baostock.com/baostock/index.php/Python%E5%BC%80%E5%8F%91%E8%B5%84%E6%BA%90) | [MyData](http://api.mairui.club/hsdata.html) |
| -------------------------------------------- | -------------------------------------- | ------------------------------------------------------------ | -------------------------------------------- |
|                                              |                                        |                                                              |                                              |
|                                              |                                        |                                                              |                                              |
|                                              |                                        |                                                              |                                              |



## 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


## 特技

1.  使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2.  Gitee 官方博客 [blog.gitee.com](https://blog.gitee.com)
3.  你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解 Gitee 上的优秀开源项目
4.  [GVP](https://gitee.com/gvp) 全称是 Gitee 最有价值开源项目，是综合评定出的优秀开源项目
5.  Gitee 官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6.  Gitee 封面人物是一档用来展示 Gitee 会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)

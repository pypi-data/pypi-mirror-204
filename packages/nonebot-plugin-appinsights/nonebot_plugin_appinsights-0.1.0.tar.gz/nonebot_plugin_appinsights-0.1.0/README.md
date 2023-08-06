<div align="center">

# nonebot-plugin-appinsights
### Nonebot2 Application Insights 日志连接插件

<a href="https://raw.githubusercontent.com/xzhouqd/nonebot-plugin-appinsights/main/LICENSE">
    <img src="https://img.shields.io/github/license/xzhouqd/nonebot-plugin-appinsights?style=for-the-badge" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-appinsights">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-appinsights?color=green&style=for-the-badge" alt="pypi">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-appinsights">
    <img src="https://img.shields.io/pypi/dm/nonebot-plugin-appinsights?style=for-the-badge" alt="pypi download">
</a>
<img src="https://img.shields.io/badge/require_python-3.8+-blue?style=for-the-badge" alt="python">
<br />
<img src="https://img.shields.io/badge/tested_python-3.10.6-blue?style=for-the-badge" alt="python">
<img src="https://img.shields.io/badge/tested_env-go_cqhttp_1.0.0-blue?style=for-the-badge" alt="python">
<img src="https://img.shields.io/badge/tested_Nonebot-2.0.0_rc4-red?style=for-the-badge" alt="nonebot">
</div>

## 配置 Application Insights Connection String
用户需在.env配置文件内通过配置项`applicationinsights_connection_string`进行配置
```
applicationinsights_connection_string = "InstrumentationKey=***"
```


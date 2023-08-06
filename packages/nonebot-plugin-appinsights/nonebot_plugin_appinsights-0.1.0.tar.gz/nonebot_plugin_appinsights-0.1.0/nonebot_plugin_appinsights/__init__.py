import nonebot
from nonebot.log import logger
from opencensus.ext.azure.log_exporter import AzureLogHandler

from .config import Config

config = Config.parse_obj(nonebot.get_driver().config)

appinsights_con_str = config.applicationinsights_connection_string

if appinsights_con_str:
    logger.add(
        AzureLogHandler(connection_string=appinsights_con_str)
    )
else:
    logger.warning("Application insights connection string is not loaded, ignore connecting.")

__plugin_meta__ = nonebot.plugin.PluginMetadata(
    name='Nonebot2 AppInsights',
    description='Nonebot2 Application Insights 日志连接插件',
    usage='在.env内配置applicationinsights_connection_string以使用',
    extra={'version': '0.1.0'}
)
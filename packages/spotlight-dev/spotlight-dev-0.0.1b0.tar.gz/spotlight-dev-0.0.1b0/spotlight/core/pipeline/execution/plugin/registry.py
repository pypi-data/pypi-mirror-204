from typing import List, Set, Optional, Any

from spotlight.core.common.metaclass.singleton import Singleton
from spotlight.core.pipeline.execution.plugin.abstract import AbstractPlugin


class PluginRegistry(metaclass=Singleton):
    """
    Singleton registry used to lookup plugins
    """

    plugins: Set[AbstractPlugin] = set()

    @classmethod
    def register(cls, plugin: AbstractPlugin) -> None:
        """
        Adds a plugin to the registry

        Args:
            plugin (AbstractPlugin): A plugin to add to the registry
        """
        cls.plugins.add(plugin)

    @classmethod
    def get_plugin(cls, data: Any) -> AbstractPlugin:
        """
        Searches the registry for a plugin that works for the data

        Args:
            data (Any): The data being tested

        Returns:
            AbstractPlugin: The plugin that works for the data
        """
        for plugin in cls.plugins:
            if plugin.use_plugin(data):
                return plugin
        raise ValueError(f"There are no plugins that support the data passed in.")

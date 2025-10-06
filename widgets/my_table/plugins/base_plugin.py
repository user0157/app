class BasePlugin:
    def __init__(self):
        self.table = None

    def set_table(self, table):
        self.table = table
        if hasattr(table, 'on'):
            table.on("widgets_created", self._on_widgets_recreated)

    def _on_widgets_recreated(self, *args, **kwargs):
        self.run()

    def run(self):
        raise NotImplementedError("Plugins must implement the run method")

    @property
    def tree(self):
        return self.table.tree if self.table else None

    @property
    def data(self):
        return self.table.data if self.table else None

    @property
    def columns(self):
        return self.table.columns if self.table else None

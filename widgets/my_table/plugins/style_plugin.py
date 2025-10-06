from .base_plugin import BasePlugin

class StylePlugin(BasePlugin):
    def run(self):
        self.table.on("table_refreshed", self.apply_styles)
        self.table.refresh()

    def apply_styles(self):
        children = self.tree.get_children()

        for i, item_id in enumerate(children):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.item(item_id, tags=(tag,))

        self.tree.tag_configure('oddrow', background='#d3d3d3')
        self.tree.tag_configure('evenrow', background='#a9a9a9')
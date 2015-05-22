import os
import sys

import sublime
import sublime_plugin

from .isort import SortImports

sys.path.append(os.path.dirname(__file__))


class IsortCommand(sublime_plugin.TextCommand):
    view = None

    def get_region(self, view):
        return sublime.Region(0, view.size())

    def get_buffer_contents(self, view):
        return view.substr(self.get_region(view))

    def set_view(self):
        self.view = sublime.active_window().active_view()
        return self.view

    def get_view(self):
        if self.view is None:
            return self.set_view()

        return self.view

    def set_cursor_back(self, begin_positions):
        this_view = self.get_view()
        for pos in begin_positions:
            this_view.sel().add(pos)

    def get_positions(self):
        pos = []
        for region in self.get_view().sel():
            pos.append(region)
        return pos

    def get_settings(self):
        profile = sublime.active_window().active_view().settings().get('isort')
        return profile or {}

    def run(self, edit):
        this_view = self.get_view()
        current_positions = self.get_positions()

        this_contents = self.get_buffer_contents(this_view)
        settings = self.get_settings()
        sorted_imports = SortImports(
            file_contents=this_contents,
            **settings
        ).output
        this_view.replace(edit, self.get_region(this_view), sorted_imports)

        # Our sel has moved now..
        remove_sel = this_view.sel()[0]
        this_view.sel().subtract(remove_sel)
        self.set_cursor_back(current_positions)

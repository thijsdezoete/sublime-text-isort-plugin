import sublime
import sublime_plugin
from isort import SortImports


class IsortCommand(sublime_plugin.TextCommand):
	def get_region(self, view):
		return sublime.Region(0, view.size())

	def get_buffer_contents(self, view):
		return view.substr(self.get_region(view))

	def run(self, edit):
		this_view = sublime.active_window().active_view()
		this_contents = self.get_buffer_contents(this_view)
		sorted_imports = SortImports(file_contents=this_contents).output
		this_view.replace(edit, self.get_region(this_view), sorted_imports)
